import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QStackedWidget, QLabel, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QLinearGradient, QColor, QPalette, QBrush

from src.sidebar import Sidebar
from src.dashboard import DashboardWidget
from src.gis_map import GISMapWidget
from src.analytics import AnalyticsWidget
from src.datasets import DatasetsWidget
from src.upload_data import UploadDataWidget
from src.about import AboutWidget
from src.utils.notification import NotificationManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blue Crab GIS")
        self.setMinimumSize(1200, 800)
        
        # Set dark blue gradient background for the entire application
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(15, 32, 65))  # Darker blue at top
        gradient.setColorAt(1, QColor(5, 15, 40))   # Even darker blue at bottom
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        
        # Global stylesheet for the application
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a1428;
            }
            QWidget {
                font-family: Arial;
                color: #e0e0e0;
            }
            QFrame {
                border-radius: 15px;
                background-color: rgba(20, 40, 80, 0.6);
                border: 1px solid rgba(30, 60, 120, 0.5);
            }
            QGroupBox {
                border-radius: 15px;
                background-color: rgba(20, 40, 80, 0.6);
                color: #e0e0e0;
                border: 1px solid rgba(30, 60, 120, 0.5);
            }
            QPushButton {
                border-radius: 8px;
                background-color: rgba(41, 128, 185, 0.8);
                color: white;
                border: none;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.9);
            }
            QComboBox {
                border-radius: 8px;
                background-color: rgba(20, 40, 80, 0.8);
                color: #e0e0e0;
                border: 1px solid rgba(41, 128, 185, 0.5);
                padding: 3px 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: rgba(15, 32, 65, 0.95);
                color: #e0e0e0;
                selection-background-color: rgba(41, 128, 185, 0.8);
            }
            QLineEdit {
                border-radius: 8px;
                background-color: rgba(20, 40, 80, 0.8);
                color: #e0e0e0;
                border: 1px solid rgba(41, 128, 185, 0.5);
                padding: 5px;
            }
            QLabel {
                color: #e0e0e0;
            }
            QTabWidget::pane {
                border: 1px solid rgba(41, 128, 185, 0.5);
                border-radius: 15px;
                background-color: rgba(20, 40, 80, 0.6);
            }
            QTabBar::tab {
                background-color: rgba(15, 32, 65, 0.8);
                color: #e0e0e0;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: rgba(41, 128, 185, 0.8);
                color: white;
            }
            QScrollBar:vertical {
                background: rgba(15, 32, 65, 0.5);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(41, 128, 185, 0.7);
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                background: rgba(15, 32, 65, 0.5);
                height: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(41, 128, 185, 0.7);
                border-radius: 5px;
                min-width: 20px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QTableWidget {
                background-color: rgba(15, 32, 65, 0.7);
                color: #e0e0e0;
                gridline-color: rgba(41, 128, 185, 0.3);
                border-radius: 10px;
                border: 1px solid rgba(41, 128, 185, 0.5);
            }
            QHeaderView::section {
                background-color: rgba(41, 128, 185, 0.7);
                color: white;
                border: none;
                padding: 5px;
                font-weight: bold;
            }
            QTableWidget::item {
                border-bottom: 1px solid rgba(41, 128, 185, 0.3);
            }
            QTableWidget::item:selected {
                background-color: rgba(41, 128, 185, 0.5);
            }
            QTextBrowser {
                background-color: rgba(15, 32, 65, 0.7);
                color: #e0e0e0;
                border: 1px solid rgba(41, 128, 185, 0.5);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        # Initialize notification manager
        self.notification_manager = NotificationManager(self)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)
        
        # Create stacked widget for content
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: transparent;
                border: none;
            }
        """)
        main_layout.addWidget(self.content_stack)
        
        # Set stretch factors
        main_layout.setStretchFactor(self.sidebar, 0)
        main_layout.setStretchFactor(self.content_stack, 1)
        
        # Create and add all page widgets
        self.dashboard_widget = DashboardWidget(self)
        self.gis_widget = GISMapWidget(self)
        self.analytics_widget = AnalyticsWidget(self)
        self.datasets_widget = DatasetsWidget(self)
        self.upload_widget = UploadDataWidget(self)
        self.about_widget = AboutWidget(self)
        
        self.content_stack.addWidget(self.dashboard_widget)
        self.content_stack.addWidget(self.gis_widget)
        self.content_stack.addWidget(self.analytics_widget)
        self.content_stack.addWidget(self.datasets_widget)
        self.content_stack.addWidget(self.upload_widget)
        self.content_stack.addWidget(self.about_widget)
        
        # Connect sidebar signals
        self.sidebar.page_changed.connect(self.change_page)
        
        # Connect upload data signal to auto-refresh dashboard, datasets, and map
        self.upload_widget.data_changed.connect(self.dashboard_widget.refresh_data)
        self.upload_widget.data_changed.connect(self.datasets_widget.load_data)
        self.upload_widget.data_changed.connect(self.gis_widget.reload_years_and_refresh)
        
        # Set default page
        self.content_stack.setCurrentIndex(0)
    
    def resizeEvent(self, event):
        """Update gradient on resize"""
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(15, 32, 65))  # Darker blue at top
        gradient.setColorAt(1, QColor(5, 15, 40))   # Even darker blue at bottom
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        super().resizeEvent(event)
        
    def change_page(self, index):
        self.content_stack.setCurrentIndex(index)
