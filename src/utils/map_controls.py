from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont

import os
import qtawesome as qta

class MapControlsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set up the widget
        self.setObjectName("mapControls")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #mapControls {
                background-color: rgba(25, 52, 95, 0.7);
                border-radius: 15px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(52, 152, 219, 0.5);
            }
            QPushButton {
                background-color: rgba(52, 152, 219, 0.8);
                border: none;
                border-radius: 10px;
                padding: 8px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(41, 128, 185, 1.0);
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Create control buttons with qtawesome icons
        self.zoom_in_btn = self.create_control_button("fa5s.search-plus", "Zoom In")
        self.zoom_out_btn = self.create_control_button("fa5s.search-minus", "Zoom Out")
        self.home_btn = self.create_control_button("fa5s.home", "Reset View")
        self.layers_btn = self.create_control_button("fa5s.layer-group", "Toggle Layers")
        self.measure_btn = self.create_control_button("fa5s.ruler", "Measure Distance")
        self.fullscreen_btn = self.create_control_button("fa5s.expand", "Fullscreen")
        
        # Add buttons to layout
        layout.addWidget(self.zoom_in_btn)
        layout.addWidget(self.zoom_out_btn)
        layout.addWidget(self.home_btn)
        layout.addWidget(self.layers_btn)
        layout.addWidget(self.measure_btn)
        layout.addWidget(self.fullscreen_btn)
        
        # Set fixed size
        self.setFixedSize(50, 300)
    
    def create_control_button(self, icon_name, tooltip):
        """Create a control button with qtawesome icon and tooltip"""
        button = QPushButton()
        
        # Create icon using qtawesome
        icon = qta.icon(icon_name, color='white')
        button.setIcon(icon)
        button.setIconSize(QSize(20, 20))
        button.setToolTip(tooltip)
        button.setFixedSize(34, 34)
        button.clicked.connect(lambda: self.handle_button_click(tooltip))
        return button
    
    def handle_button_click(self, action):
        """Handle button clicks based on action"""
        parent = self.parent()
        if hasattr(parent, "web_view"):
            if action == "Zoom In":
                parent.web_view.page().runJavaScript("map.zoomIn();")
            elif action == "Zoom Out":
                parent.web_view.page().runJavaScript("map.zoomOut();")
            elif action == "Reset View":
                parent.web_view.page().runJavaScript("map.setView([10.0, 123.0], 8);")
            elif action == "Toggle Layers":
                js_code = """
                if (!window.layerControl) {
                    // Create base layers
                    const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    });
                    
                    const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
                    });
                    
                    const topoLayer = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
                        attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
                    });
                    
                    const baseLayers = {
                        "OpenStreetMap": osmLayer,
                        "Satellite": satelliteLayer,
                        "Topographic": topoLayer
                    };
                    
                    // Add layer control
                    window.layerControl = L.control.layers(baseLayers).addTo(map);
                    osmLayer.addTo(map);
                } else {
                    // Toggle layer control visibility
                    const controlContainer = window.layerControl._container;
                    if (controlContainer.style.display === 'none') {
                        controlContainer.style.display = 'block';
                    } else {
                        controlContainer.style.display = 'none';
                    }
                }
                """
                parent.web_view.page().runJavaScript(js_code)
            elif action == "Measure Distance":
                js_code = """
                if (!window.measureControl) {
                    // Add measure control
                    window.measureControl = L.control.measure({
                        position: 'topleft',
                        primaryLengthUnit: 'kilometers',
                        secondaryLengthUnit: 'miles',
                        primaryAreaUnit: 'sqkilometers',
                        secondaryAreaUnit: 'acres'
                    }).addTo(map);
                    
                    // Add CSS for measure control
                    const style = document.createElement('style');
                    style.textContent = `
                        .leaflet-control-measure {
                            background-color: rgba(25, 52, 95, 0.8) !important;
                            color: white !important;
                            border-radius: 10px !important;
                        }
                        .leaflet-control-measure a {
                            color: white !important;
                        }
                    `;
                    document.head.appendChild(style);
                    
                    // Trigger measure tool
                    document.querySelector('.leaflet-control-measure a').click();
                } else {
                    // Toggle measure control
                    const measureButton = document.querySelector('.leaflet-control-measure a');
                    if (measureButton) {
                        measureButton.click();
                    }
                }
                """
                parent.web_view.page().runJavaScript(js_code)
            elif action == "Fullscreen":
                js_code = """
                if (!document.fullscreenElement) {
                    document.getElementById('map').requestFullscreen();
                } else {
                    document.exitFullscreen();
                }
                """
                parent.web_view.page().runJavaScript(js_code)
