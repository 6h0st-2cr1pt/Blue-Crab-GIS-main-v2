from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QFrame, QLabel, QComboBox, QSlider, QGridLayout)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont

import qtawesome as qta

class GlassMapControls(QWidget):
    """Glass-effect map controls widget"""
    
    # Signals
    zoom_in_clicked = pyqtSignal()
    zoom_out_clicked = pyqtSignal()
    home_clicked = pyqtSignal()
    layers_clicked = pyqtSignal()
    satellite_clicked = pyqtSignal()
    fullscreen_clicked = pyqtSignal()
    refresh_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set up the widget
        self.setObjectName("glassMapControls")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #glassMapControls {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(15, 32, 65, 0.85),
                    stop:0.5 rgba(25, 52, 95, 0.75),
                    stop:1 rgba(15, 32, 65, 0.85));
                border-radius: 20px;
                border: 1px solid rgba(52, 152, 219, 0.3);
                backdrop-filter: blur(10px);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(52, 152, 219, 0.6),
                    stop:1 rgba(41, 128, 185, 0.8));
                border: 1px solid rgba(52, 152, 219, 0.4);
                border-radius: 12px;
                padding: 8px;
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(65, 165, 235, 0.8),
                    stop:1 rgba(52, 152, 219, 1.0));
                border: 1px solid rgba(65, 165, 235, 0.6);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(41, 128, 185, 1.0),
                    stop:1 rgba(30, 100, 150, 1.0));
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("Controls")
        title.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-weight: bold;
                font-size: 12px;
                background: transparent;
                border: none;
                margin-bottom: 5px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Create control buttons
        self.zoom_in_btn = self.create_control_button("fa5s.search-plus", "Zoom In")
        self.zoom_out_btn = self.create_control_button("fa5s.search-minus", "Zoom Out")
        self.home_btn = self.create_control_button("fa5s.home", "Reset View")
        self.layers_btn = self.create_control_button("fa5s.layer-group", "Toggle Layers")
        self.satellite_btn = self.create_control_button("fa5s.satellite", "Satellite View")
        self.fullscreen_btn = self.create_control_button("fa5s.expand", "Fullscreen")
        self.refresh_btn = self.create_control_button("fa5s.sync-alt", "Refresh")
        
        # Connect signals
        self.zoom_in_btn.clicked.connect(self.zoom_in_clicked.emit)
        self.zoom_out_btn.clicked.connect(self.zoom_out_clicked.emit)
        self.home_btn.clicked.connect(self.home_clicked.emit)
        self.layers_btn.clicked.connect(self.layers_clicked.emit)
        self.satellite_btn.clicked.connect(self.satellite_clicked.emit)
        self.fullscreen_btn.clicked.connect(self.fullscreen_clicked.emit)
        self.refresh_btn.clicked.connect(self.refresh_clicked.emit)
        
        # Add buttons to layout
        layout.addWidget(self.zoom_in_btn)
        layout.addWidget(self.zoom_out_btn)
        layout.addWidget(self.home_btn)
        layout.addWidget(self.layers_btn)
        layout.addWidget(self.satellite_btn)
        layout.addWidget(self.fullscreen_btn)
        layout.addWidget(self.refresh_btn)
        
        # Set fixed size
        self.setFixedSize(80, 400)
    
    def create_control_button(self, icon_name, tooltip):
        """Create a control button with glass effect"""
        button = QPushButton()
        
        # Create icon using qtawesome
        icon = qta.icon(icon_name, color='white')
        button.setIcon(icon)
        button.setIconSize(QSize(18, 18))
        button.setToolTip(tooltip)
        button.setFixedSize(56, 40)
        
        return button

class GlassFilterControls(QWidget):
    """Glass-effect filter controls widget"""
    
    # Signals
    filter_changed = pyqtSignal(str)
    sex_filter_changed = pyqtSignal(str)
    year_filter_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set up the widget
        self.setObjectName("glassFilterControls")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #glassFilterControls {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(15, 32, 65, 0.85),
                    stop:0.5 rgba(25, 52, 95, 0.75),
                    stop:1 rgba(15, 32, 65, 0.85));
                border-radius: 20px;
                border: 1px solid rgba(52, 152, 219, 0.3);
                backdrop-filter: blur(10px);
            }
            QLabel {
                color: #e0e0e0;
                font-weight: normal;
                font-size: 11px;
                background: transparent;
                border: none;
                margin: 0px 0;
            }
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(20, 40, 80, 0.8),
                    stop:1 rgba(15, 32, 65, 0.9));
                color: #e0e0e0;
                border: 0px solid rgba(52, 152, 219, 0.4);
                border-radius: 20px;
                padding: 0px 0px;
                min-width: 120px;
                font-size: 11px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #e0e0e0;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(15, 32, 65, 0.95),
                    stop:1 rgba(10, 25, 50, 0.98));
                color: #e0e0e0;
                selection-background-color: rgba(52, 152, 219, 0.6);
                border: 1px solid rgba(52, 152, 219, 0.4);
                border-radius: 8px;
            }
            QComboBox:hover {
                border: 1px solid rgba(65, 165, 235, 0.6);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(25, 50, 90, 0.8),
                    stop:1 rgba(20, 40, 80, 0.9));
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("Filters")
        title.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-weight: normal;
                font-size: 13px;
                background: transparent;
                border: none;
                margin-bottom: 0px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Population filter
        pop_label = QLabel("Population:")
        self.population_filter = QComboBox()
        self.population_filter.addItems([
            "All Populations", 
            "Low (<100)", 
            "Medium (100-500)", 
            "High (>500)"
        ])
        self.population_filter.currentTextChanged.connect(self.filter_changed.emit)
        
        layout.addWidget(pop_label)
        layout.addWidget(self.population_filter)
        
        # Sex distribution filter
        sex_label = QLabel("Sex Distribution:")
        self.sex_filter = QComboBox()
        self.sex_filter.addItems([
            "All", 
            "Male Dominant", 
            "Female Dominant", 
            "Balanced"
        ])
        self.sex_filter.currentTextChanged.connect(self.sex_filter_changed.emit)
        
        layout.addWidget(sex_label)
        layout.addWidget(self.sex_filter)
        
        # Year filter
        year_label = QLabel("Year:")
        self.year_filter = QComboBox()
        self.year_filter.addItem("All Years")  # Default, populate externally
        self.year_filter.currentTextChanged.connect(self.year_filter_changed.emit)
        layout.addWidget(year_label)
        layout.addWidget(self.year_filter)
        
        # Set fixed size (increase height for new filter)
        self.setFixedSize(190, 220)
    
    def set_years(self, years):
        """Set the available years in the year filter."""
        self.year_filter.clear()
        self.year_filter.addItem("All Years")
        for year in sorted(years):
            self.year_filter.addItem(str(year))
    
    def get_selected_year(self):
        """Get the currently selected year (or None for all)."""
        text = self.year_filter.currentText()
        return None if text == "All Years" else int(text)

class GlassAnalyticsCards(QWidget):
    """Glass-effect analytics cards widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set up the widget
        self.setObjectName("glassAnalyticsCards")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #glassAnalyticsCards {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(15, 32, 65, 0.85),
                    stop:0.5 rgba(25, 52, 95, 0.75),
                    stop:1 rgba(15, 32, 65, 0.85));
                border-radius: 20px;
                border: 1px solid rgba(52, 152, 219, 0.3);
                backdrop-filter: blur(10px);
            }
            QLabel {
                color: #e0e0e0;
                background: transparent;
                border: none;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Analytics")
        title.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-weight: bold;
                font-size: 25px;
                background: transparent;
                border: none;
                margin-bottom: 18px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Create analytics cards in a grid
        cards_layout = QVBoxLayout()
        cards_layout.setSpacing(8)
        # Total Population Card
        self.total_pop_card = self.create_stat_card("Total Population", "0", "#3498db")
        cards_layout.addWidget(self.total_pop_card)
        # Total Locations Card
        self.total_locations_card = self.create_stat_card("Locations", "0", "#2ecc71")
        cards_layout.addWidget(self.total_locations_card)
        # Male Count Card
        self.male_count_card = self.create_stat_card("Males", "0", "#06b6d4")
        cards_layout.addWidget(self.male_count_card)
        # Female Count Card
        self.female_count_card = self.create_stat_card("Females", "0", "#ec4899")
        cards_layout.addWidget(self.female_count_card)
        # Average Population Card
        self.avg_pop_card = self.create_stat_card("Avg Population", "0", "#f59e0b")
        cards_layout.addWidget(self.avg_pop_card)
        # Max Population Card
        self.max_pop_card = self.create_stat_card("Max Population", "0", "#e74c3c")
        cards_layout.addWidget(self.max_pop_card)
        layout.addLayout(cards_layout)
        
        # Set fixed size
        self.setFixedSize(230, 650)
    
    def create_stat_card(self, title, value, color):
        """Create a small stat card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(10, 25, 50, 0.6),
                    stop:1 rgba(5, 15, 35, 0.8));
                border-radius: 16px;
                border: 1px solid rgba(52, 152, 219, 0.2);
                padding: 18px;
            }}
        """)
        card.setFixedSize(200, 90)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: #a0a0a0;
                font-size: 15px;
                font-weight: normal;
                letter-spacing: 0px;
                background: transparent;
                border: none;
            }}
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 15px;
                font-weight: normal;
                letter-spacing: 0px;
                background: transparent;
                border: none;

            }}
        """)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setObjectName("value_label")  # For easy access
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return card
    
    def update_analytics(self, analytics_data):
        """Update the analytics cards with new data"""
        try:
            # Update total population
            total_pop = analytics_data.get('total_population', 0)
            self.total_pop_card.findChild(QLabel, "value_label").setText(f"{total_pop:,}")
            
            # Update total locations
            total_locations = analytics_data.get('total_records', 0)
            self.total_locations_card.findChild(QLabel, "value_label").setText(str(total_locations))
            
            # Update male count
            total_males = analytics_data.get('total_males', 0)
            self.male_count_card.findChild(QLabel, "value_label").setText(f"{total_males:,}")
            
            # Update female count
            total_females = analytics_data.get('total_females', 0)
            self.female_count_card.findChild(QLabel, "value_label").setText(f"{total_females:,}")
            
            # Update average population
            avg_pop = round(total_pop / total_locations) if total_locations > 0 else 0
            self.avg_pop_card.findChild(QLabel, "value_label").setText(f"{avg_pop:,}")
            
            # Update max population (we'll calculate this from the data)
            max_pop = analytics_data.get('max_population', 0)
            self.max_pop_card.findChild(QLabel, "value_label").setText(f"{max_pop:,}")
            
        except Exception as e:
            print(f"Error updating analytics: {e}")
