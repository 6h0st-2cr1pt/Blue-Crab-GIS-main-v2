from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QRadioButton, 
                            QButtonGroup, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPoint
from PyQt5.QtGui import QIcon, QFont, QPixmap, QLinearGradient, QColor, QPalette, QBrush, QPainter

import os
import qtawesome as qta

class SidebarButton(QRadioButton):
    def __init__(self, text, icon_name, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", 10))
        
        # Use qtawesome for icons
        icon = self.get_icon_for_name(icon_name)
        self.setIcon(icon)
        self.setIconSize(QSize(24, 24))
        self.setStyleSheet("""
            QRadioButton {
                color: #e0e0e0;
                background-color: transparent;
                border: none;
                border-radius: 12px;
                padding: 12px;
                padding-left: 15px;
                text-align: left;
                spacing: 10px;
            }
            QRadioButton:hover {
                background-color: rgba(41, 128, 185, 0.3);
            }
            QRadioButton:checked {
                background-color: rgba(41, 128, 185, 0.8);
                font-weight: bold;
                color: white;
            }
            QRadioButton::indicator {
                width: 0px;
                height: 0px;
            }
        """)
    
    def get_icon_for_name(self, icon_name):
        """Map icon names to qtawesome icons"""
        icon_map = {
            "dashboard": "fa5s.tachometer-alt",
            "map": "fa5s.map-marked-alt",
            "analytics": "fa5s.chart-bar",
            "database": "fa5s.database",
            "upload": "fa5s.upload",
            "info": "fa5s.info-circle",
            "blue_crab_logo": "fa5s.water"
        }
        
        # Get the corresponding qtawesome icon name or use a default
        qta_icon_name = icon_map.get(icon_name, "fa5s.question-circle")
        
        # Create and return the icon with blue color
        return qta.icon(qta_icon_name, color="#3b82f6")

class Sidebar(QWidget):
    page_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(220)
        
        # Set gradient background
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(10, 25, 50))  # Dark blue at top
        gradient.setColorAt(1, QColor(5, 15, 35))   # Darker blue at bottom
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        
        self.setStyleSheet("""
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
            border-right: 1px solid rgba(41, 128, 185, 0.3);
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # App title
        title_container = QWidget()
        title_container.setStyleSheet("""
            background-color: rgba(41, 128, 185, 0.3); 
            padding: 15px;
            border-radius: 15px;
            border: 1px solid rgba(41, 128, 185, 0.5);
        """)
        title_layout = QVBoxLayout(title_container)
        
        # Create logo using qtawesome
        logo_label = QLabel()
        logo_icon = qta.icon('fa5s.water', color="#3b82f6", scale_factor=2)
        logo_pixmap = logo_icon.pixmap(40, 40)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel("Blue Crab")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #e0e0e0;")
        title_label.setAlignment(Qt.AlignCenter)
        
        title_layout.addWidget(logo_label)
        title_layout.addWidget(title_label)
        layout.addWidget(title_container)
        
        # Navigation buttons
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        # Create buttons with icons
        self.dashboard_btn = SidebarButton("Dashboard", "dashboard")
        self.gis_btn = SidebarButton("GIS Map", "map")
        self.analytics_btn = SidebarButton("Analytics", "analytics")
        self.datasets_btn = SidebarButton("Datasets", "database")
        self.upload_btn = SidebarButton("Upload Data", "upload")
        self.about_btn = SidebarButton("About", "info")
        
        # Add buttons to group and layout
        buttons = [
            self.dashboard_btn, self.gis_btn, self.analytics_btn,
            self.datasets_btn, self.upload_btn, self.about_btn
        ]
        
        for i, button in enumerate(buttons):
            self.button_group.addButton(button, i)
            layout.addWidget(button)
        
        # Add spacer at the bottom
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Set default selection
        self.dashboard_btn.setChecked(True)
        
        # Connect signals
        self.button_group.buttonClicked[int].connect(self.page_changed)
    
    def resizeEvent(self, event):
        """Update gradient on resize"""
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(10, 25, 50))  # Dark blue at top
        gradient.setColorAt(1, QColor(5, 15, 35))   # Darker blue at bottom
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        super().resizeEvent(event)
