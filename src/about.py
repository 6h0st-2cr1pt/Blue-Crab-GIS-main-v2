from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QTabWidget, QTextBrowser)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QFont, QIcon, QLinearGradient, QColor, QPalette, QBrush

class AboutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with logo and app info
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            background-color: rgba(41, 128, 185, 0.2);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(41, 128, 185, 0.3);
        """)
        
        header_layout = QHBoxLayout(header_frame)
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/icons/blue_crab_logo.png")
        logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # App info
        info_layout = QVBoxLayout()
        
        app_name = QLabel("Blue Crab GIS")
        app_name.setStyleSheet("color: #e0e0e0; font-size: 28px; font-weight: bold;")
        
        app_version = QLabel("Version 1.0.0")
        app_version.setStyleSheet("color: #a0a0a0; font-size: 16px;")
        
        app_desc = QLabel("Geographic Information System for Blue Crab Population Monitoring")
        app_desc.setStyleSheet("color: #c0c0c0; font-size: 14px;")
        app_desc.setWordWrap(True)
        
        info_layout.addWidget(app_name)
        info_layout.addWidget(app_version)
        info_layout.addWidget(app_desc)
        
        header_layout.addWidget(logo_label)
        header_layout.addLayout(info_layout)
        header_layout.setStretchFactor(logo_label, 1)
        header_layout.setStretchFactor(info_layout, 3)
        
        layout.addWidget(header_frame)
        
        # Tab widget for about sections
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(41, 128, 185, 0.3);
                border-radius: 15px;
                padding: 10px;
                background-color: rgba(15, 32, 65, 0.5);
            }
            QTabBar::tab {
                background-color: rgba(15, 32, 65, 0.7);
                border: 1px solid rgba(41, 128, 185, 0.2);
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 16px;
                margin-right: 2px;
                color: #c0c0c0;
            }
            QTabBar::tab:selected {
                background-color: rgba(41, 128, 185, 0.7);
                border-bottom: 1px solid rgba(41, 128, 185, 0.7);
                color: white;
                font-weight: bold;
            }
        """)
        
        # About tab
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        
        about_text = QTextBrowser()
        about_text.setOpenExternalLinks(True)
        about_text.setStyleSheet("""
            QTextBrowser {
                background-color: rgba(10, 25, 50, 0.7);
                border: none;
                border-radius: 10px;
                color: #e0e0e0;
                padding: 15px;
            }
            QScrollBar:vertical {
                background: rgba(10, 25, 50, 0.5);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(41, 128, 185, 0.7);
                border-radius: 5px;
            }
        """)
        
        about_html = """
        <h2 style="color: #3498db;">About Blue Crab GIS</h2>
        <p style="color: #e0e0e0;">Blue Crab GIS is a desktop application designed for monitoring and analyzing blue crab populations in the Negros Island region of the Philippines.</p>
        
        <p style="color: #e0e0e0;">This application provides tools for:</p>
        <ul style="color: #e0e0e0;">
            <li>Visualizing blue crab population data on interactive maps</li>
            <li>Analyzing population trends and distributions</li>
            <li>Managing and importing population datasets</li>
            <li>Generating reports and insights about crab populations</li>
        </ul>
        
        <p style="color: #e0e0e0;">The application is built using PyQt5 and integrates with OpenStreetMap and Leaflet.js for mapping capabilities.</p>
        
        <h3 style="color: #3498db;">System Requirements</h3>
        <ul style="color: #e0e0e0;">
            <li>Operating System: Windows 10/11, macOS 10.14+, or Linux</li>
            <li>RAM: 4GB minimum, 8GB recommended</li>
            <li>Storage: 500MB free space</li>
            <li>Internet connection for map data (optional for cached regions)</li>
        </ul>
        """
        
        about_text.setHtml(about_html)
        about_layout.addWidget(about_text)
        
        # Features tab
        features_tab = QWidget()
        features_layout = QVBoxLayout(features_tab)
        
        features_text = QTextBrowser()
        features_text.setOpenExternalLinks(True)
        features_text.setStyleSheet("""
            QTextBrowser {
                background-color: rgba(10, 25, 50, 0.7);
                border: none;
                border-radius: 10px;
                color: #e0e0e0;
                padding: 15px;
            }
            QScrollBar:vertical {
                background: rgba(10, 25, 50, 0.5);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(41, 128, 185, 0.7);
                border-radius: 5px;
            }
        """)
        
        features_html = """
        <h2 style="color: #3498db;">Key Features</h2>
        
        <h3 style="color: #3498db;">Interactive GIS Map</h3>
        <p style="color: #e0e0e0;">The GIS module provides an interactive map with the following features:</p>
        <ul style="color: #e0e0e0;">
            <li>Standard map with clear visualization of geographic features</li>
            <li>Population density visualization with color-coded markers</li>
            <li>Interactive popups showing detailed information for each location</li>
            <li>Filtering capabilities based on population density</li>
            <li>Floating glass-effect control panel for map navigation</li>
        </ul>
        
        <h3 style="color: #3498db;">Data Management</h3>
        <p style="color: #e0e0e0;">Comprehensive data management tools including:</p>
        <ul style="color: #e0e0e0;">
            <li>CSV file import with drag-and-drop functionality</li>
            <li>Manual data entry form for individual records</li>
            <li>SQLite database integration for reliable data storage</li>
            <li>Data filtering and search capabilities</li>
        </ul>
        
        <h3 style="color: #3498db;">Analytics</h3>
        <p style="color: #e0e0e0;">Advanced analytics features for data insights:</p>
        <ul style="color: #e0e0e0;">
            <li>Population distribution charts</li>
            <li>Density heatmaps showing concentration areas</li>
            <li>Population trend analysis over time</li>
            <li>Interactive visualizations with filtering options</li>
        </ul>
        
        <h3 style="color: #3498db;">Customization</h3>
        <p style="color: #e0e0e0;">Extensive customization options:</p>
        <ul style="color: #e0e0e0;">
            <li>Dark blue gradient theme for reduced eye strain</li>
            <li>Map tile server selection</li>
            <li>Performance optimization settings</li>
            <li>Data management preferences</li>
        </ul>
        """
        
        features_text.setHtml(features_html)
        features_layout.addWidget(features_text)
        
        # Credits tab
        credits_tab = QWidget()
        credits_layout = QVBoxLayout(credits_tab)
        
        credits_text = QTextBrowser()
        credits_text.setOpenExternalLinks(True)
        credits_text.setStyleSheet("""
            QTextBrowser {
                background-color: rgba(10, 25, 50, 0.7);
                border: none;
                border-radius: 10px;
                color: #e0e0e0;
                padding: 15px;
            }
            QScrollBar:vertical {
                background: rgba(10, 25, 50, 0.5);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(41, 128, 185, 0.7);
                border-radius: 5px;
            }
        """)
        
        credits_html = """
        <h2 style="color: #3498db;">Credits & Acknowledgements</h2>
        
        <h3 style="color: #3498db;">Development Team</h3>
        <p style="color: #e0e0e0;">Blue Crab GIS was developed by:</p>
        <ul style="color: #e0e0e0;">
            <li>Project Manager: Jan Lloyd Belonio </li>
            <li>System Analyst: John Norlie Reoner </li>
            <li>Programmer: Jonald Sabordo </li>
        </ul>
        
        <h3 style="color: #3498db;">Technologies Used</h3>
        <ul style="color: #e0e0e0;">
            <li>PyQt5 - Cross-platform GUI framework</li>
            <li>QWebEngineView - Web content rendering</li>
            <li>OpenStreetMap - Map data provider</li>
            <li>Leaflet.js - Interactive map library</li>
            <li>SQLite - Database engine</li>
            <li>Matplotlib & Seaborn - Data visualization</li>
            <li>Pandas - Data analysis and manipulation</li>
        </ul>
        
        <h3 style="color: #3498db;">Map Tiles</h3>
        <p style="color: #e0e0e0;">Map tiles provided by:</p>
        <ul style="color: #e0e0e0;">
            <li>OpenStreetMap - <a href="https://www.openstreetmap.org/copyright" style="color: #3498db;">https://www.openstreetmap.org/copyright</a></li>
            <li>CartoDB - <a href="https://carto.com/attributions" style="color: #3498db;">https://carto.com/attributions</a></li>
        </ul>
        
        <h3 style="color: #3498db;">Icons</h3>
        <p style="color: #e0e0e0;">Icons used in this application are from various sources and have been modified for use in this project.</p>
        
        <h3 style="color: #3498db;">Special Thanks</h3>
        <p style="color: #e0e0e0;">Special thanks to all contributors and testers who helped make this application possible.</p>
        """
        
        credits_text.setHtml(credits_html)
        credits_layout.addWidget(credits_text)
        
        # Add tabs to tab widget
        tab_widget.addTab(about_tab, "About")
        tab_widget.addTab(features_tab, "Features")
        tab_widget.addTab(credits_tab, "Credits")
        
        layout.addWidget(tab_widget)
