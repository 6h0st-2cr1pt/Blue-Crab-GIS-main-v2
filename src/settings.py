from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QCheckBox, QSlider, QPushButton,
                            QGroupBox, QFormLayout, QSpinBox, QTabWidget,
                            QColorDialog, QFrame, QFileDialog, QLineEdit)
from PyQt5.QtCore import Qt, QSettings, QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

import os

class ColorButton(QPushButton):
    def __init__(self, color=QColor("#3b82f6"), parent=None):
        super().__init__(parent)
        self.setColor(color)
        self.clicked.connect(self.choose_color)
        self.setFixedSize(32, 32)
    
    def setColor(self, color):
        self.color = color
        self.setStyleSheet(f"""
            background-color: {color.name()};
            border: 1px solid #e2e8f0;
            border-radius: 4px;
        """)
    
    def choose_color(self):
        color = QColorDialog.getColor(self.color, self.parent(), "Choose Color")
        if color.isValid():
            self.setColor(color)

class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.settings = QSettings("BlueCrabGIS", "App")
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1e3a8a; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Description
        description = QLabel("Customize the application to suit your preferences.")
        description.setStyleSheet("color: #64748b; margin-bottom: 20px;")
        layout.addWidget(description)
        
        # Tab widget for settings categories
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                padding: 10px;
            }
            QTabBar::tab {
                background-color: #f1f5f9;
                border: 1px solid #e2e8f0;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
        """)
        
        # General settings tab
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        # Theme settings
        theme_group = QGroupBox("Theme")
        theme_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        theme_layout = QFormLayout(theme_group)
        theme_layout.setLabelAlignment(Qt.AlignRight)
        
        # Color theme
        color_label = QLabel("Primary Color:")
        self.color_btn = ColorButton(QColor(self.settings.value("theme/primary_color", "#3b82f6")))
        
        # Dark mode
        dark_mode_label = QLabel("Dark Mode:")
        self.dark_mode_check = QCheckBox()
        self.dark_mode_check.setChecked(self.settings.value("theme/dark_mode", "false") == "true")
        
        theme_layout.addRow(color_label, self.color_btn)
        theme_layout.addRow(dark_mode_label, self.dark_mode_check)
        
        # Map settings
        map_group = QGroupBox("Map")
        map_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        map_layout = QFormLayout(map_group)
        
        # Default zoom
        zoom_label = QLabel("Default Zoom Level:")
        self.zoom_spin = QSpinBox()
        self.zoom_spin.setRange(1, 18)
        self.zoom_spin.setValue(int(self.settings.value("map/default_zoom", 8)))
        
        # Tile server
        tile_label = QLabel("Map Tile Server:")
        self.tile_combo = QComboBox()
        self.tile_combo.addItems(["Dark Mode (CartoDB)", "Light Mode (CartoDB)", "OpenStreetMap", "Satellite"])
        self.tile_combo.setCurrentText(self.settings.value("map/tile_server", "Dark Mode (CartoDB)"))
        
        # Cache tiles
        cache_label = QLabel("Cache Map Tiles:")
        self.cache_check = QCheckBox()
        self.cache_check.setChecked(self.settings.value("map/cache_tiles", "true") == "true")
        
        map_layout.addRow(zoom_label, self.zoom_spin)
        map_layout.addRow(tile_label, self.tile_combo)
        map_layout.addRow(cache_label, self.cache_check)
        
        # Add groups to general tab
        general_layout.addWidget(theme_group)
        general_layout.addWidget(map_group)
        general_layout.addStretch()
        
        # Performance tab
        performance_tab = QWidget()
        performance_layout = QVBoxLayout(performance_tab)
        
        # Hardware acceleration
        accel_group = QGroupBox("Hardware Acceleration")
        accel_layout = QFormLayout(accel_group)
        
        accel_label = QLabel("Enable Hardware Acceleration:")
        self.accel_check = QCheckBox()
        self.accel_check.setChecked(self.settings.value("performance/hardware_accel", "true") == "true")
        
        accel_layout.addRow(accel_label, self.accel_check)
        
        # Map optimization
        map_opt_group = QGroupBox("Map Optimization")
        map_opt_layout = QFormLayout(map_opt_group)
        
        # Vector tiles
        vector_label = QLabel("Use Vector Tiles:")
        self.vector_check = QCheckBox()
        self.vector_check.setChecked(self.settings.value("performance/vector_tiles", "true") == "true")
        
        # Limit map area
        limit_label = QLabel("Limit Map to Negros Island:")
        self.limit_check = QCheckBox()
        self.limit_check.setChecked(self.settings.value("performance/limit_map", "true") == "true")
        
        # Animation quality
        anim_label = QLabel("Animation Quality:")
        self.anim_combo = QComboBox()
        self.anim_combo.addItems(["High", "Medium", "Low"])
        self.anim_combo.setCurrentText(self.settings.value("performance/animation_quality", "Medium"))
        
        map_opt_layout.addRow(vector_label, self.vector_check)
        map_opt_layout.addRow(limit_label, self.limit_check)
        map_opt_layout.addRow(anim_label, self.anim_combo)
        
        # Add groups to performance tab
        performance_layout.addWidget(accel_group)
        performance_layout.addWidget(map_opt_group)
        performance_layout.addStretch()
        
        # Data tab
        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)
        
        # Database settings
        db_group = QGroupBox("Database")
        db_layout = QFormLayout(db_group)
        
        # Database location
        db_path_label = QLabel("Database Location:")
        
        db_path_container = QFrame()
        db_path_layout = QHBoxLayout(db_path_container)
        db_path_layout.setContentsMargins(0, 0, 0, 0)
        
        self.db_path_input = QLineEdit()
        self.db_path_input.setText(self.settings.value("data/db_path", "data/blue_crab.db"))
        self.db_path_input.setReadOnly(True)
        
        self.db_path_btn = QPushButton("Browse")
        self.db_path_btn.clicked.connect(self.browse_db_path)
        
        db_path_layout.addWidget(self.db_path_input)
        db_path_layout.addWidget(self.db_path_btn)
        
        # Auto backup
        backup_label = QLabel("Auto Backup:")
        self.backup_check = QCheckBox()
        self.backup_check.setChecked(self.settings.value("data/auto_backup", "true") == "true")
        
        db_layout.addRow(db_path_label, db_path_container)
        db_layout.addRow(backup_label, self.backup_check)
        
        # Add groups to data tab
        data_layout.addWidget(db_group)
        data_layout.addStretch()
        
        # Add tabs to tab widget
        tab_widget.addTab(general_tab, "General")
        tab_widget.addTab(performance_tab, "Performance")
        tab_widget.addTab(data_tab, "Data")
        
        layout.addWidget(tab_widget)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.reset_btn = QPushButton("Reset to Defaults")
        self.reset_btn.clicked.connect(self.reset_settings)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """)
        
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self.save_settings)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_btn)
        
        layout.addLayout(buttons_layout)
    
    def browse_db_path(self):
        """Open file dialog to browse for database location"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Select Database Location", "", "SQLite Database (*.db)"
        )
        
        if file_path:
            self.db_path_input.setText(file_path)
    
    def save_settings(self):
        """Save settings to QSettings and apply changes where possible"""
        # Theme settings
        self.settings.setValue("theme/primary_color", self.color_btn.color.name())
        self.settings.setValue("theme/dark_mode", str(self.dark_mode_check.isChecked()).lower())
        
        # Map settings
        self.settings.setValue("map/default_zoom", self.zoom_spin.value())
        self.settings.setValue("map/tile_server", self.tile_combo.currentText())
        self.settings.setValue("map/cache_tiles", str(self.cache_check.isChecked()).lower())
        
        # Performance settings
        self.settings.setValue("performance/hardware_accel", str(self.accel_check.isChecked()).lower())
        self.settings.setValue("performance/vector_tiles", str(self.vector_check.isChecked()).lower())
        self.settings.setValue("performance/limit_map", str(self.limit_check.isChecked()).lower())
        self.settings.setValue("performance/animation_quality", self.anim_combo.currentText())
        
        # Data settings
        self.settings.setValue("data/db_path", self.db_path_input.text())
        self.settings.setValue("data/auto_backup", str(self.backup_check.isChecked()).lower())
        
        # Apply changes immediately where possible
        self.apply_settings()
        
        # Show notification
        from src.utils.notification import show_notification
        show_notification(self.parent, "Success", "Settings saved successfully. Some changes may require a restart.")

    def apply_settings(self):
        """Apply settings immediately where possible"""
        # Apply dark mode if changed
        dark_mode = self.dark_mode_check.isChecked()
        if dark_mode:
            self.parent.setStyleSheet("""
                QMainWindow {
                    background-color: #1e293b;
                }
                QWidget {
                    font-family: Arial;
                    color: #e2e8f0;
                }
                QFrame {
                    border-radius: 15px;
                    background-color: #334155;
                }
                QGroupBox {
                    border-radius: 15px;
                    background-color: #334155;
                }
                QPushButton {
                    border-radius: 8px;
                    background-color: #3b82f6;
                    color: white;
                }
                QComboBox {
                    border-radius: 8px;
                    background-color: #475569;
                    color: white;
                }
                QLineEdit {
                    border-radius: 8px;
                    background-color: #475569;
                    color: white;
                }
                QTabWidget::pane {
                    border: none;
                    background-color: #334155;
                    border-radius: 15px;
                }
                QTabBar::tab {
                    background-color: #475569;
                    color: #e2e8f0;
                }
                QTabBar::tab:selected {
                    background-color: #3b82f6;
                    color: white;
                }
            """)
        else:
            self.parent.setStyleSheet("""
                QMainWindow {
                    background-color: #f8fafc;
                }
                QWidget {
                    font-family: Arial;
                }
                QFrame {
                    border-radius: 15px;
                }
                QGroupBox {
                    border-radius: 15px;
                }
                QPushButton {
                    border-radius: 8px;
                }
                QComboBox {
                    border-radius: 8px;
                }
                QLineEdit {
                    border-radius: 8px;
                }
            """)
        
        # Apply hardware acceleration setting
        if hasattr(self.parent, 'gis_widget') and hasattr(self.parent.gis_widget, 'web_view'):
            settings = self.parent.gis_widget.web_view.settings()
            settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, self.accel_check.isChecked())
            settings.setAttribute(QWebEngineSettings.WebGLEnabled, self.accel_check.isChecked())
        
        # Apply primary color to buttons
        primary_color = self.color_btn.color.name()
        for widget in self.parent.findChildren(QPushButton):
            if "background-color: #2563eb" in widget.styleSheet() or "background-color: #3b82f6" in widget.styleSheet():
                widget.setStyleSheet(widget.styleSheet().replace("#2563eb", primary_color).replace("#3b82f6", primary_color))
        
        # Apply map settings if GIS widget exists
        if hasattr(self.parent, 'gis_widget'):
            # Update map tile server
            tile_server = self.tile_combo.currentText()
            js_code = ""
            if tile_server == "Dark Mode (CartoDB)":
                js_code = """
                map.eachLayer(function(layer) {
                    if (layer instanceof L.TileLayer) {
                        map.removeLayer(layer);
                    }
                });
                L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                    subdomains: 'abcd',
                    maxZoom: 19
                }).addTo(map);
                """
            elif tile_server == "Light Mode (CartoDB)":
                js_code = """
                map.eachLayer(function(layer) {
                    if (layer instanceof L.TileLayer) {
                        map.removeLayer(layer);
                    }
                });
                L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                    subdomains: 'abcd',
                    maxZoom: 19
                }).addTo(map);
                """
            elif tile_server == "OpenStreetMap":
                js_code = """
                map.eachLayer(function(layer) {
                    if (layer instanceof L.TileLayer) {
                        map.removeLayer(layer);
                    }
                });
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    maxZoom: 19
                }).addTo(map);
                """
            elif tile_server == "Satellite":
                js_code = """
                map.eachLayer(function(layer) {
                    if (layer instanceof L.TileLayer) {
                        map.removeLayer(layer);
                    }
                });
                L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
                    maxZoom: 19
                }).addTo(map);
                """
            
            if js_code:
                self.parent.gis_widget.web_view.page().runJavaScript(js_code)
            
            # Update default zoom
            zoom_level = self.zoom_spin.value()
            self.parent.gis_widget.web_view.page().runJavaScript(f"map.setZoom({zoom_level});")
            
            # Update map caching
            cache_enabled = self.cache_check.isChecked()
            settings = self.parent.gis_widget.web_view.settings()
            settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, cache_enabled)
    
    def reset_settings(self):
        """Reset settings to defaults"""
        # Theme settings
        self.color_btn.setColor(QColor("#3b82f6"))
        self.dark_mode_check.setChecked(False)
        
        # Map settings
        self.zoom_spin.setValue(8)
        self.tile_combo.setCurrentText("Dark Mode (CartoDB)")
        self.cache_check.setChecked(True)
        
        # Performance settings
        self.accel_check.setChecked(True)
        self.vector_check.setChecked(True)
        self.limit_check.setChecked(True)
        self.anim_combo.setCurrentText("Medium")
        
        # Data settings
        self.db_path_input.setText("data/blue_crab.db")
        self.backup_check.setChecked(True)
