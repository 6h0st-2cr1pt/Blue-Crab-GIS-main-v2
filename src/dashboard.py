from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QSizePolicy, QPushButton)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPainter, QColor, QLinearGradient, QBrush
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
import qtawesome as qta

from src.utils.database import DatabaseManager

class StatCard(QFrame):
    def __init__(self, title, value, icon_name, color="#3498DB", parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            background-color: rgba(15, 32, 65, 0.7);
            border-radius: 15px;
            border-left: 4px solid {color};
            padding: 15px;
        """)
        
        layout = QHBoxLayout(self)
        
        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color=color).pixmap(32, 32))
        
        # Text content
        text_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #a0a0a0; font-size: 14px;")
        
        self.value_label = QLabel(self.format_number_with_space(value))
        self.value_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(self.value_label)
        
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        layout.addStretch()

    @staticmethod
    def format_number_with_space(value):
        try:
            return f"{int(value):,}".replace(",", " ")
        except Exception:
            return str(value)

    def update_value(self, value, color=None):
        self.value_label.setText(self.format_number_with_space(value))
        if color:
            self.value_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        self.value_label.update()

class ChartCard(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            background-color: rgba(15, 32, 65, 0.7);
            border-radius: 15px;
            padding: 15px;
            border: 1px solid rgba(41, 128, 185, 0.3);
        """)
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #3498DB; font-size: 16px; font-weight: bold;")
        
        layout.addWidget(title_label)
        
        # Chart will be added by child classes
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = DatabaseManager()
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title with refresh button
        title_bar = QHBoxLayout()
        title = QLabel("Blue Crab GIS Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498DB;")
        title_bar.addWidget(title)
        title_bar.addStretch()
        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(qta.icon('fa5s.sync-alt', color='#3498DB'))
        self.refresh_btn.setToolTip("Refresh Dashboard Data")
        self.refresh_btn.setFixedSize(40, 32)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
                color: #3498DB;
            }
            QPushButton:hover {
                background: rgba(52, 152, 219, 0.1);
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_data)
        title_bar.addWidget(self.refresh_btn)
        layout.addLayout(title_bar)
        
        # Stats cards
        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)
        
        # Get data for stats
        all_crab_data = self.db_manager.get_all_crab_data()
        # Find the latest year
        years = [d['date_year'] for d in all_crab_data if d.get('date_year')]
        latest_year = max(years) if years else None
        crab_data = [d for d in all_crab_data if d.get('date_year') == latest_year] if latest_year else all_crab_data
        total_locations = len(crab_data)
        total_population = sum(d['population'] for d in crab_data) if crab_data else 0
        total_females = sum(d['female_counts'] for d in crab_data) if crab_data else 0
        total_males = sum(d['male_counts'] for d in crab_data) if crab_data else 0
        
        # Create stat cards
        self.locations_card = StatCard(
            "Total Locations", 
            total_locations, 
            "fa5s.map-marker-alt", 
            "#3498DB"
        )
        
        self.population_card = StatCard(
            "Total Population", 
            total_population, 
            "fa5s.users", 
            "#2E86C1"
        )
        
        self.female_card = StatCard(
            "Female Population",
            total_females,
            "fa5s.venus",
            "#ec4899"
        )
        self.male_card = StatCard(
            "Male Population",
            total_males,
            "fa5s.mars",
            "#06b6d4"
        )
        
        # Add cards to layout
        stats_layout.addWidget(self.locations_card, 0, 0)
        stats_layout.addWidget(self.population_card, 0, 1)
        stats_layout.addWidget(self.female_card, 1, 0)
        stats_layout.addWidget(self.male_card, 1, 1)
        
        layout.addLayout(stats_layout)
        
        # Charts
        charts_layout = QHBoxLayout()
        
        # Create distribution chart
        self.distribution_chart = self.create_distribution_chart(crab_data)
        charts_layout.addWidget(self.distribution_chart)
        
        # Create male/female ratio pie chart ONCE
        self.ratio_chart_card = ChartCard("Male/Female Ratio")
        ratio_chart_layout = self.ratio_chart_card.layout()
        self.ratio_chart = QChart()
        self.ratio_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.ratio_chart.setBackgroundBrush(QBrush(QColor(15, 32, 65)))
        self.ratio_chart.setTitleBrush(QBrush(QColor("#e0e0e0")))
        self.ratio_chart.setTitleFont(QFont("Arial", 12, QFont.Bold))
        self.ratio_series = QPieSeries()
        self.ratio_chart.addSeries(self.ratio_series)
        self.ratio_chart.legend().setVisible(True)
        self.ratio_chart.legend().setAlignment(Qt.AlignBottom)
        self.ratio_chart.legend().setLabelColor(QColor("#e0e0e0"))
        self.ratio_chart_view = QChartView(self.ratio_chart)
        self.ratio_chart_view.setRenderHint(QPainter.Antialiasing)
        ratio_chart_layout.addWidget(self.ratio_chart_view)
        charts_layout.addWidget(self.ratio_chart_card)
        
        layout.addLayout(charts_layout)
        
        # Set stretch factors
        layout.setStretchFactor(stats_layout, 1)
        layout.setStretchFactor(charts_layout, 2)
        
        # Initial pie chart data
        self.update_ratio_chart(crab_data)
    
    def create_distribution_chart(self, crab_data):
        """Create a chart showing population distribution"""
        chart_card = ChartCard("Population Distribution")
        chart_layout = chart_card.layout()
        
        # Create chart
        chart = QChart()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Set dark theme for chart
        chart.setBackgroundBrush(QBrush(QColor(15, 32, 65)))
        chart.setTitleBrush(QBrush(QColor("#e0e0e0")))
        chart.setTitleFont(QFont("Arial", 12, QFont.Bold))
        
        # Create pie series
        series = QPieSeries()
        
        if crab_data:
            # Count populations in each category
            low = sum(1 for d in crab_data if d['population'] < 100)
            medium = sum(1 for d in crab_data if 100 <= d['population'] <= 500)
            high = sum(1 for d in crab_data if d['population'] > 500)
            
            # Add slices
            if low > 0:
                slice_low = series.append("Low (<100)", low)
                slice_low.setBrush(QColor("#3498DB"))
                slice_low.setLabelVisible(True)
                slice_low.setLabelColor(QColor("#e0e0e0"))
            
            if medium > 0:
                slice_med = series.append("Medium (100-500)", medium)
                slice_med.setBrush(QColor("#2E86C1"))
                slice_med.setLabelVisible(True)
                slice_med.setLabelColor(QColor("#e0e0e0"))
            
            if high > 0:
                slice_high = series.append("High (>500)", high)
                slice_high.setBrush(QColor("#1B4F72"))
                slice_high.setLabelVisible(True)
                slice_high.setLabelColor(QColor("#e0e0e0"))
        else:
            no_data = series.append("No Data", 1)
            no_data.setBrush(QColor("#3498DB"))
            no_data.setLabelVisible(True)
            no_data.setLabelColor(QColor("#e0e0e0"))
        
        chart.addSeries(series)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setLabelColor(QColor("#e0e0e0"))
        
        # Create chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        
        chart_layout.addWidget(chart_view)
        
        return chart_card
    
    def update_ratio_chart(self, crab_data):
        self.ratio_series.clear()
        total_males = sum(d['male_counts'] for d in crab_data) if crab_data else 0
        total_females = sum(d['female_counts'] for d in crab_data) if crab_data else 0
        if total_males > 0:
            slice_male = self.ratio_series.append(f"Males: {total_males:,}", total_males)
            slice_male.setBrush(QColor("#06b6d4"))
            slice_male.setLabelVisible(True)
            slice_male.setLabelColor(QColor("#e0e0e0"))
        if total_females > 0:
            slice_female = self.ratio_series.append(f"Females: {total_females:,}", total_females)
            slice_female.setBrush(QColor("#ec4899"))
            slice_female.setLabelVisible(True)
            slice_female.setLabelColor(QColor("#e0e0e0"))
        if total_males == 0 and total_females == 0:
            no_data = self.ratio_series.append("No Data", 1)
            no_data.setBrush(QColor("#3498DB"))
            no_data.setLabelVisible(True)
            no_data.setLabelColor(QColor("#e0e0e0"))

    def refresh_data(self):
        """Refresh dashboard data from the database and update UI."""
        all_crab_data = self.db_manager.get_all_crab_data()
        years = [d['date_year'] for d in all_crab_data if d.get('date_year')]
        latest_year = max(years) if years else None
        crab_data = [d for d in all_crab_data if d.get('date_year') == latest_year] if latest_year else all_crab_data
        total_locations = len(crab_data)
        total_population = sum(d['population'] for d in crab_data) if crab_data else 0
        total_females = sum(d['female_counts'] for d in crab_data) if crab_data else 0
        total_males = sum(d['male_counts'] for d in crab_data) if crab_data else 0

        # Update stat cards
        self.locations_card.update_value(total_locations)
        self.population_card.update_value(total_population)
        self.female_card.update_value(total_females)
        self.male_card.update_value(total_males)
        self.locations_card.update()
        self.population_card.update()
        self.female_card.update()
        self.male_card.update()

        # Update charts (do not recreate widgets)
        parent_layout = self.layout()
        charts_layout = parent_layout.itemAt(2).layout()
        # Update distribution chart (recreate for now)
        for i in reversed(range(charts_layout.count())):
            widget = charts_layout.itemAt(i).widget()
            if widget and widget is not self.ratio_chart_card:
                widget.setParent(None)
        charts_layout.insertWidget(0, self.create_distribution_chart(crab_data))
        # Update ratio chart data only
        self.update_ratio_chart(crab_data)
        self.update()
