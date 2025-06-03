from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QComboBox, QPushButton, QSlider, QCheckBox)
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtGui import QFont

import json
import os
import qtawesome as qta

from src.utils.database import DatabaseManager
from src.utils.map_controls import MapControlsWidget
from src.utils.glass_controls import GlassMapControls, GlassFilterControls, GlassAnalyticsCards

class GISMapWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = DatabaseManager()
        self.selected_year = None  # Track selected year
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Map container (full height)
        map_container = QFrame()
        map_container.setStyleSheet("background-color: transparent;")
        map_layout = QVBoxLayout(map_container)
        map_layout.setContentsMargins(0, 0, 0, 0)
        
        # Web view for map
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("border: none;")
        
        # Enable hardware acceleration
        self.web_view.settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        
        # Set page load strategy to eager
        self.web_view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)
        self.web_view.settings().setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, False)
        
        # Load the map
        self.load_map()
        
        map_layout.addWidget(self.web_view)
        
        # Add glass controls overlay
        self.setup_glass_controls()
        
        layout.addWidget(map_container)
        
        # Movement throttling
        self.last_move_time = 0
        self.move_throttle = 100  # milliseconds between move events
        
        # Connect map movement events
        self.web_view.page().runJavaScript("""
            map.on('moveend', function() {
                // Throttle move events
                var now = Date.now();
                if (now - window.lastMoveTime < 100) {
                    return;
                }
                window.lastMoveTime = now;
                
                // Update markers only if they're in view
                var bounds = map.getBounds();
                window.markers.forEach(function(marker) {
                    if (bounds.contains(marker.getLatLng())) {
                        if (!window.markerClusterGroup.hasLayer(marker)) {
                            window.markerClusterGroup.addLayer(marker);
                        }
                    } else {
                        if (window.markerClusterGroup.hasLayer(marker)) {
                            window.markerClusterGroup.removeLayer(marker);
                        }
                    }
                });
            });
        """)
    
    def load_map(self):
        """Load the Leaflet map"""
        # Create the HTML content for the map
        html_content = self.create_map_html()
        
        # Save to temporary file and load
        map_file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'map', 'gis_map.html')
        os.makedirs(os.path.dirname(map_file_path), exist_ok=True)
        
        with open(map_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Load the map
        self.web_view.load(QUrl.fromLocalFile(os.path.abspath(map_file_path)))
        
        # Wait for page to load, then add data
        self.web_view.loadFinished.connect(self.on_map_loaded)
    
    def create_map_html(self):
        """Create the HTML content for the map"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Blue Crab GIS Map</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            
            <!-- Leaflet CSS -->
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css" />
            <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css" />
            
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    background-color: #0a1428;
                }
                #map {
                    height: 100vh;
                    width: 100%;
                }
                .custom-popup {
                    background-color: rgba(15, 32, 65, 0.95);
                    color: #e0e0e0;
                    border-radius: 8px;
                    border: 1px solid rgba(41, 128, 185, 0.5);
                }
                .popup-title {
                    color: #3498db;
                    font-weight: bold;
                    font-size: 14px;
                    margin-bottom: 8px;
                }
                .popup-content {
                    font-size: 12px;
                    line-height: 1.4;
                }
                .popup-stat {
                    margin: 3px 0;
                }
                .stat-label {
                    color: #c0c0c0;
                }
                .stat-value {
                    color: #e0e0e0;
                    font-weight: bold;
                }
                .male-count { color: #06b6d4; }
                .female-count { color: #ec4899; }
                .total-count { color: #f59e0b; }
            </style>
        </head>
        <body>
            <div id="map"></div>
            
            <!-- Leaflet JavaScript -->
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"></script>
            
            <script>
                // Initialize map centered on Negros Island, Philippines
                var map = L.map('map', {
                    zoomControl: false,
                    attributionControl: false,
                    preferCanvas: true,  // Use Canvas renderer for better performance
                    maxZoom: 19,
                    minZoom: 5
                }).setView([10.7, 122.9], 9);  // Adjusted center and zoom level
                
                // Add dark tile layer with caching
                var tileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                    subdomains: 'abcd',
                    maxZoom: 19,
                    crossOrigin: true,
                    updateWhenIdle: true,  // Only update tiles when map is idle
                    updateWhenZooming: false,  // Don't update tiles during zoom
                    keepBuffer: 2  // Keep 2 zoom levels of tiles in buffer
                }).addTo(map);
                
                // Store markers for filtering
                window.markers = [];
                window.markersLayer = L.layerGroup().addTo(map);
                window.lastMoveTime = 0;
                
                // Function to add crab data markers with clustering (only one per location, most recent year)
                function addCrabMarkers(data) {
                    if (window.markerClusterGroup) {
                        window.markerClusterGroup.clearLayers();
                    }
                    window.markers = [];
                    if (!data || data.length === 0) {
                        console.log('No data to display');
                        return;
                    }
                    if (!window.markerClusterGroup) {
                        window.markerClusterGroup = L.markerClusterGroup({
                            maxClusterRadius: 50,
                            spiderfyOnMaxZoom: true,
                            showCoverageOnHover: false,
                            zoomToBoundsOnClick: true,
                            disableClusteringAtZoom: 15,
                            chunkedLoading: true,
                            chunkInterval: 200,
                            chunkDelay: 50
                        });
                        window.markersLayer.addLayer(window.markerClusterGroup);
                    }
                    var bounds = L.latLngBounds([]);
                    data.forEach(function(item) {
                        var color = '#3498db';
                        if (item.population < 100) {
                            color = '#3498db';
                        } else if (item.population <= 500) {
                            color = '#2ecc71';
                        } else {
                            color = '#e74c3c';
                        }
                        var marker = L.circleMarker([item.latitude, item.longitude], {
                            radius: Math.max(5, Math.min(15, item.population / 50)),
                            fillColor: color,
                            color: color,
                            weight: 0,
                            opacity: 1,
                            fillOpacity: 0.8
                        });
                        var popupContent = `
                            <div class="custom-popup">
                                <div class="popup-title">Blue Crab Population Data</div>
                                <div class="popup-content">
                                    <div class="popup-stat">
                                        <span class="stat-label">Coordinates:</span>
                                        <span class="stat-value">${item.latitude.toFixed(4)}, ${item.longitude.toFixed(4)}</span>
                                    </div>
                                    <div class="popup-stat">
                                        <span class="stat-label">Year:</span>
                                        <span class="stat-value">${item.date_year}</span>
                                    </div>
                                    <div class="popup-stat">
                                        <span class="stat-label">Male Count:</span>
                                        <span class="stat-value male-count">${item.male_counts}</span>
                                    </div>
                                    <div class="popup-stat">
                                        <span class="stat-label">Female Count:</span>
                                        <span class="stat-value female-count">${item.female_counts}</span>
                                    </div>
                                    <div class="popup-stat">
                                        <span class="stat-label">Total Population:</span>
                                        <span class="stat-value total-count">${item.population}</span>
                                    </div>
                                    <div class="popup-stat">
                                        <span class="stat-label">Observer:</span>
                                        <span class="stat-value">${item.observer_name || 'Unknown'}</span>
                                    </div>
                                </div>
                            </div>
                        `;
                        marker.bindPopup(popupContent);
                        marker.crabData = item;
                        window.markers.push(marker);
                        window.markerClusterGroup.addLayer(marker);
                        bounds.extend([item.latitude, item.longitude]);
                    });
                    // Always fit map to show all markers with padding
                    if (bounds.isValid()) {
                        map.fitBounds(bounds, {
                            padding: [50, 50],
                            maxZoom: 12
                        });
                    }
                }
                
                // Helper function to get month name
                function getMonthName(month) {
                    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                    return months[month - 1] || 'Unknown';
                }
                
                // Function to filter markers
                function filterMarkers(filterType) {
                    if (!window.markerClusterGroup) return;
                    
                    window.markerClusterGroup.clearLayers();
                    
                    window.markers.forEach(function(marker) {
                        var show = true;
                        var population = marker.crabData.population;
                        
                        switch(filterType) {
                            case 1: // Low (<100)
                                show = population < 100;
                                break;
                            case 2: // Medium (100-500)
                                show = population >= 100 && population <= 500;
                                break;
                            case 3: // High (>500)
                                show = population > 500;
                                break;
                            default: // All
                                show = true;
                        }
                        
                        if (show) {
                            window.markerClusterGroup.addLayer(marker);
                        }
                    });
                }
                
                // Function to update analytics display
                function updateAnalytics(analytics) {
                    // This function can be called from Python to update analytics
                    console.log('Analytics updated:', analytics);
                }
                
                // Function to filter markers by year (show all records for that year)
                function filterMarkersByYear(year) {
                    if (!window.markerClusterGroup) return;
                    window.markerClusterGroup.clearLayers();
                    window.markers.forEach(function(marker) {
                        var show = true;
                        if (year !== null && year !== undefined) {
                            show = marker.crabData.date_year == year;
                        }
                        if (show) {
                            window.markerClusterGroup.addLayer(marker);
                        }
                    });
                }
                
                // Make functions available globally
                window.addCrabMarkers = addCrabMarkers;
                window.filterMarkers = filterMarkers;
                window.updateAnalytics = updateAnalytics;
            </script>
        </body>
        </html>
        """
    
    def on_map_loaded(self):
        """Called when the map finishes loading"""
        # Load initial data
        self.refresh_map_data(self.selected_year)
    
    def refresh_map_data(self, year=None):
        """Refresh the map with current data, filtered by year if given"""
        try:
            crab_data = self.db_manager.get_all_crab_data()
            # Filter by year if specified
            if year is not None:
                crab_data = [item for item in crab_data if item['date_year'] == year]
            # Grouping logic: always show all records for each (lat, lon, year)
            grouped = {}
            for item in crab_data:
                key = (item['latitude'], item['longitude'], item['date_year'])
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append(item)
            all_years_records = [rec for records in grouped.values() for rec in records]
            print(f"Loaded {len(crab_data)} records from database (filtered by year={year})")
            print(f"Unique (lat,lon,year) groups: {len(grouped)}")
            if all_years_records:
                print("Sample data:", all_years_records[0])
            data_json = json.dumps(all_years_records)
            js_code = f"""
            console.log('Adding {len(all_years_records)} markers to map');
            addCrabMarkers({data_json});
            """
            self.web_view.page().runJavaScript(js_code)
            self.refresh_analytics(all_years_records, year)
        except Exception as e:
            print(f"Error refreshing map data: {e}")
            import traceback
            traceback.print_exc()
    
    def refresh_analytics(self, crab_data, year=None):
        """Refresh analytics data, filtered by year if given"""
        try:
            analytics_data = self.db_manager.get_analytics_data()
            # If year is set, filter analytics_data['monthly'] to that year
            if year is not None:
                analytics_data['monthly'] = [m for m in analytics_data['monthly'] if m['date_year'] == year]
            total_population = sum(item['total_population'] for item in analytics_data['monthly'])
            total_males = sum(item['total_males'] for item in analytics_data['monthly'])
            total_females = sum(item['total_females'] for item in analytics_data['monthly'])
            max_population = max(item['population'] for item in crab_data) if crab_data else 0
            analytics_summary = {
                'total_population': total_population,
                'total_males': total_males,
                'total_females': total_females,
                'male_percentage': round((total_males / total_population * 100) if total_population > 0 else 0, 1),
                'female_percentage': round((total_females / total_population * 100) if total_population > 0 else 0, 1),
                'total_records': len(crab_data),
                'regions': len(analytics_data['regional']),
                'max_population': max_population,
                'year': year
            }
            if hasattr(self, 'analytics_cards'):
                self.analytics_cards.update_analytics(analytics_summary)
            analytics_json = json.dumps(analytics_summary)
            js_code = f"updateAnalytics({analytics_json});"
            self.web_view.page().runJavaScript(js_code)
        except Exception as e:
            print(f"Error refreshing analytics: {e}")
    
    def apply_filters(self):
        """Apply population filters to the map"""
        filter_index = self.population_filter.currentIndex()
        js_code = f"filterMarkers({filter_index});"
        self.web_view.page().runJavaScript(js_code)
    
    def zoom_to_negros(self):
        """Zoom to Negros Island"""
        js_code = "map.setView([10.0, 123.0], 8);"
        self.web_view.page().runJavaScript(js_code)
    
    def toggle_satellite_view(self):
        """Toggle between map and satellite view"""
        js_code = """
        if (!window.satelliteLayer) {
            window.satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                attribution: 'Tiles &copy; Esri'
            });
        }
        
        if (map.hasLayer(window.satelliteLayer)) {
            map.removeLayer(window.satelliteLayer);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
                subdomains: 'abcd',
                maxZoom: 19
            }).addTo(map);
        } else {
            map.eachLayer(function(layer) {
                if (layer instanceof L.TileLayer && layer !== window.satelliteLayer) {
                    map.removeLayer(layer);
                }
            });
            map.addLayer(window.satelliteLayer);
        }
        """
        self.web_view.page().runJavaScript(js_code)

    def setup_glass_controls(self):
        """Setup glass-effect overlay controls"""
        # Map controls (right side center)
        self.map_controls = GlassMapControls(self.web_view)
        
        # Filter controls (top left)
        self.filter_controls = GlassFilterControls(self.web_view)
        
        # Populate year filter
        crab_data = self.db_manager.get_all_crab_data()
        years = sorted(set(item['date_year'] for item in crab_data))
        self.filter_controls.set_years(years)
        
        # Analytics cards (bottom left)
        self.analytics_cards = GlassAnalyticsCards(self.web_view)
        
        # Connect map control signals
        self.map_controls.zoom_in_clicked.connect(self.zoom_in)
        self.map_controls.zoom_out_clicked.connect(self.zoom_out)
        self.map_controls.home_clicked.connect(self.zoom_to_negros)
        self.map_controls.layers_clicked.connect(self.toggle_layers)
        self.map_controls.satellite_clicked.connect(self.toggle_satellite_view)
        self.map_controls.fullscreen_clicked.connect(self.toggle_fullscreen)
        self.map_controls.refresh_clicked.connect(lambda: self.refresh_map_data(self.selected_year))
        
        # Connect filter control signals
        self.filter_controls.filter_changed.connect(self.apply_population_filter)
        self.filter_controls.sex_filter_changed.connect(self.apply_sex_filter)
        self.filter_controls.year_filter_changed.connect(self.apply_year_filter)
        
        # Position controls initially
        self.position_controls()
        
        # Make sure controls are visible
        self.map_controls.show()
        self.filter_controls.show()
        self.analytics_cards.show()
    
    def position_controls(self):
        """Position the glass controls"""
        if hasattr(self, 'web_view'):
            web_view_width = self.web_view.width()
            web_view_height = self.web_view.height()

            # Map controls - left side center
            map_controls_x = 20
            map_controls_y = (web_view_height - self.map_controls.height()) // 2
            self.map_controls.move(map_controls_x, map_controls_y)

            # Analytics cards - bottom right
            analytics_x = web_view_width - self.analytics_cards.width() - 20
            analytics_y = web_view_height - self.analytics_cards.height() - 20
            self.analytics_cards.move(analytics_x, analytics_y)

            # Filter controls - above analytics cards
            filter_controls_x = web_view_width - self.filter_controls.width() - 20
            filter_controls_y = analytics_y - self.filter_controls.height() - 20
            self.filter_controls.move(filter_controls_x, filter_controls_y)
    
    def resizeEvent(self, event):
        """Handle resize events to reposition controls"""
        super().resizeEvent(event)
        if hasattr(self, 'map_controls') and hasattr(self, 'filter_controls') and hasattr(self, 'analytics_cards'):
            # Reposition controls after a short delay to ensure web view is resized
            QTimer.singleShot(100, self.position_controls)
    
    def zoom_in(self):
        """Zoom in on the map"""
        self.web_view.page().runJavaScript("map.zoomIn();")
    
    def zoom_out(self):
        """Zoom out on the map"""
        self.web_view.page().runJavaScript("map.zoomOut();")
    
    def toggle_layers(self):
        """Toggle map layers"""
        js_code = """
        if (!window.layerControl) {
            const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            });
            
            const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                attribution: 'Tiles &copy; Esri'
            });
            
            const darkLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
            });
            
            const baseLayers = {
                "Dark Mode": darkLayer,
                "Standard": osmLayer,
                "Satellite": satelliteLayer
            };
            
            window.layerControl = L.control.layers(baseLayers).addTo(map);
        } else {
            const controlContainer = window.layerControl._container;
            controlContainer.style.display = controlContainer.style.display === 'none' ? 'block' : 'none';
        }
        """
        self.web_view.page().runJavaScript(js_code)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        js_code = """
        if (!document.fullscreenElement) {
            document.getElementById('map').requestFullscreen();
        } else {
            document.exitFullscreen();
        }
        """
        self.web_view.page().runJavaScript(js_code)
    
    def apply_population_filter(self, filter_text):
        """Apply population filter"""
        filter_map = {
            "All Populations": 0,
            "Low (<100)": 1,
            "Medium (100-500)": 2,
            "High (>500)": 3
        }
        filter_index = filter_map.get(filter_text, 0)
        js_code = f"filterMarkers({filter_index});"
        self.web_view.page().runJavaScript(js_code)
    
    def apply_sex_filter(self, filter_text):
        """Apply sex distribution filter"""
        js_code = f"""
        window.markersLayer.clearLayers();
        
        window.markers.forEach(function(marker) {{
            var show = true;
            var data = marker.crabData;
            var maleRatio = data.male_counts / data.population;
            
            switch('{filter_text}') {{
                case 'Male Dominant':
                    show = maleRatio > 0.6;
                    break;
                case 'Female Dominant':
                    show = maleRatio < 0.4;
                    break;
                case 'Balanced':
                    show = maleRatio >= 0.4 && maleRatio <= 0.6;
                    break;
                default: // All
                    show = true;
            }}
            
            if (show) {{
                window.markersLayer.addLayer(marker);
            }}
        }});
        """
        self.web_view.page().runJavaScript(js_code)
    
    def apply_year_filter(self, year_text):
        """Apply year filter to the map and analytics"""
        try:
            if year_text and year_text != "All Years":
                self.selected_year = int(year_text)
            else:
                self.selected_year = None
        except ValueError:
            self.selected_year = None
        self.refresh_map_data(self.selected_year)

    def reload_years_and_refresh(self):
        """Reload year filter options and refresh map/analytics after data upload."""
        crab_data = self.db_manager.get_all_crab_data()
        years = sorted(set(item['date_year'] for item in crab_data))
        self.filter_controls.set_years(years)
        # Try to re-select the current year if it still exists
        if self.selected_year and self.selected_year in years:
            self.filter_controls.year_filter.setCurrentText(str(self.selected_year))
        else:
            self.selected_year = None
            self.filter_controls.year_filter.setCurrentText("All Years")
        self.refresh_map_data(self.selected_year)
