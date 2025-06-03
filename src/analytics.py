from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QPushButton, QFrame, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPainter, QColor, QLinearGradient, QBrush
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QPieSeries

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import calendar

from src.utils.database import DatabaseManager

class MplCanvas(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor('#0f2041')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#0f2041')
        self.axes.tick_params(colors='#e0e0e0')
        self.axes.xaxis.label.set_color('#e0e0e0')
        self.axes.yaxis.label.set_color('#e0e0e0')
        self.axes.title.set_color('#3498DB')
        super(MplCanvas, self).__init__(self.fig)
        self.fig.tight_layout()

class AnalyticsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = DatabaseManager()
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Blue Crab Population Analytics")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #3498DB; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Description
        description = QLabel("Analyze blue crab population data with interactive charts and graphs.")
        description.setStyleSheet("color: #c0c0c0; margin-bottom: 20px;")
        layout.addWidget(description)
        
        # Controls
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            background-color: rgba(15, 32, 65, 0.7);
            border-radius: 15px;
            padding: 10px;
            border: 1px solid rgba(41, 128, 185, 0.3);
        """)
        controls_layout = QHBoxLayout(controls_frame)
        
        chart_type_label = QLabel("Chart Type:")
        chart_type_label.setStyleSheet("font-weight: bold; color: #e0e0e0;")
        
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems([
            "Population Distribution", 
            "Population Density Heatmap", 
            "Population Trends",
            "Population Size Breakdown",
            "Monthly Trends",
            "Male/Female Ratio"
        ])
        self.chart_type_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid rgba(41, 128, 185, 0.5);
                border-radius: 8px;
                padding: 5px;
                background-color: rgba(10, 25, 50, 0.7);
                color: #e0e0e0;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox::down-arrow {
                image: url(assets/icons/dropdown.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: rgba(15, 32, 65, 0.95);
                color: #e0e0e0;
                selection-background-color: rgba(41, 128, 185, 0.8);
            }
        """)
        self.chart_type_combo.currentIndexChanged.connect(self.update_chart)
        
        # Year and Month filters
        self.year_combo = QComboBox()
        self.year_combo.setStyleSheet(self.chart_type_combo.styleSheet())
        self.year_combo.setMinimumWidth(90)
        self.year_combo.currentIndexChanged.connect(self.update_chart)
        self.month_combo = QComboBox()
        self.month_combo.setStyleSheet(self.chart_type_combo.styleSheet())
        self.month_combo.setMinimumWidth(120)
        self.month_combo.currentIndexChanged.connect(self.update_chart)
        
        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.setIcon(QIcon("assets/icons/refresh.png"))
        self.refresh_btn.clicked.connect(self.update_chart)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(41, 128, 185, 0.8);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.9);
            }
        """)
        
        controls_layout.addWidget(chart_type_label)
        controls_layout.addWidget(self.chart_type_combo)
        controls_layout.addWidget(QLabel("Year:"))
        controls_layout.addWidget(self.year_combo)
        controls_layout.addWidget(QLabel("Month:"))
        controls_layout.addWidget(self.month_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(self.refresh_btn)
        
        layout.addWidget(controls_frame)
        
        # Chart container
        self.chart_container = QFrame()
        self.chart_container.setFrameShape(QFrame.StyledPanel)
        self.chart_container.setStyleSheet("""
            background-color: rgba(15, 32, 65, 0.7);
            border-radius: 15px;
            padding: 15px;
            border: 1px solid rgba(41, 128, 185, 0.3);
        """)
        chart_layout = QVBoxLayout(self.chart_container)
        
        # Create tab widget for different visualizations
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: rgba(15, 32, 65, 0.7);
                border-radius: 15px;
            }
            QTabBar::tab {
                background-color: rgba(10, 25, 50, 0.7);
                border: 1px solid rgba(41, 128, 185, 0.3);
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 16px;
                margin-right: 2px;
                color: #c0c0c0;
            }
            QTabBar::tab:selected {
                background-color: rgba(41, 128, 185, 0.8);
                color: white;
            }
        """)
        
        # Create tabs for different chart types
        self.distribution_tab = QWidget()
        self.heatmap_tab = QWidget()
        self.trends_tab = QWidget()
        self.size_tab = QWidget()
        self.monthly_tab = QWidget()
        self.ratio_tab = QWidget()
        self.tab_widget.addTab(self.distribution_tab, "Distribution")
        self.tab_widget.addTab(self.heatmap_tab, "Heatmap")
        self.tab_widget.addTab(self.trends_tab, "Trends")
        self.tab_widget.addTab(self.size_tab, "Size Breakdown")
        self.tab_widget.addTab(self.monthly_tab, "Monthly")
        self.tab_widget.addTab(self.ratio_tab, "Male/Female Ratio")
        
        # Set up layouts for each tab
        self.distribution_layout = QVBoxLayout(self.distribution_tab)
        self.heatmap_layout = QVBoxLayout(self.heatmap_tab)
        self.trends_layout = QVBoxLayout(self.trends_tab)
        self.size_layout = QVBoxLayout(self.size_tab)
        self.monthly_layout = QVBoxLayout(self.monthly_tab)
        self.ratio_layout = QVBoxLayout(self.ratio_tab)
        
        chart_layout.addWidget(self.tab_widget)
        layout.addWidget(self.chart_container)
        
        # Initialize charts
        self.initialize_charts()
        
        # Update chart with initial data
        self.update_chart()
    
    def initialize_charts(self):
        """Initialize chart widgets"""
        # Distribution chart (Qt Charts)
        self.distribution_chart = QChart()
        self.distribution_chart.setTitle("Blue Crab Population Distribution")
        self.distribution_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.distribution_chart.setBackgroundBrush(QBrush(QColor(15, 32, 65)))
        self.distribution_chart.setTitleBrush(QBrush(QColor("#e0e0e0")))
        self.distribution_chart.setTitleFont(QFont("Arial", 12, QFont.Bold))
        
        self.distribution_view = QChartView(self.distribution_chart)
        self.distribution_view.setRenderHint(QPainter.Antialiasing)
        
        self.distribution_layout.addWidget(self.distribution_view)
        
        # Heatmap (Matplotlib)
        self.heatmap_canvas = MplCanvas(width=5, height=4, dpi=100)
        self.heatmap_layout.addWidget(self.heatmap_canvas)
        
        # Trends chart (Matplotlib)
        self.trends_canvas = MplCanvas(width=5, height=4, dpi=100)
        self.trends_layout.addWidget(self.trends_canvas)
        
        # Size breakdown chart (Matplotlib)
        self.size_canvas = MplCanvas(width=5, height=4, dpi=100)
        self.size_layout.addWidget(self.size_canvas)
        
        # Monthly trends chart (Matplotlib)
        self.monthly_canvas = MplCanvas(width=5, height=4, dpi=100)
        self.monthly_layout.addWidget(self.monthly_canvas)
        
        # Male/Female Ratio pie chart (Qt Charts)
        self.ratio_chart = QChart()
        self.ratio_chart.setTitle("Male/Female Ratio")
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
        self.ratio_layout.addWidget(self.ratio_chart_view)
    
    def update_chart(self):
        """Update the chart based on selected type"""
        chart_type = self.chart_type_combo.currentText()
        crab_data = self.db_manager.get_all_crab_data()
        # Populate year/month combos
        years = sorted(set(str(d['date_year']) for d in crab_data if d.get('date_year')))
        # Use month numbers for sorting, but display names
        month_nums = sorted(set(int(d['date_month']) for d in crab_data if d.get('date_month')))
        month_names = [calendar.month_name[m] for m in month_nums]
        num_to_name = {m: calendar.month_name[m] for m in month_nums}
        name_to_num = {calendar.month_name[m]: m for m in month_nums}
        current_year = self.year_combo.currentText()
        current_month = self.month_combo.currentText()
        self.year_combo.blockSignals(True)
        self.month_combo.blockSignals(True)
        self.year_combo.clear()
        self.year_combo.addItem("All Years")
        self.year_combo.addItems(years)
        if current_year in years:
            self.year_combo.setCurrentText(current_year)
        self.month_combo.clear()
        self.month_combo.addItem("All Months")
        self.month_combo.addItems(month_names)
        if current_month in month_names:
            self.month_combo.setCurrentText(current_month)
        self.year_combo.blockSignals(False)
        self.month_combo.blockSignals(False)
        # Filter data
        year = self.year_combo.currentText()
        month = self.month_combo.currentText()
        filtered_data = crab_data
        if year != "All Years":
            filtered_data = [d for d in filtered_data if str(d.get('date_year')) == year]
        if month != "All Months":
            # Convert month name to number for filtering
            month_num = name_to_num.get(month)
            filtered_data = [d for d in filtered_data if int(d.get('date_month', 0)) == month_num]
        if not filtered_data:
            self.clear_all_charts()
            self.update_stat_cards_empty()
            return
        populations = np.array([d['population'] for d in filtered_data])
        latitudes = np.array([d['latitude'] for d in filtered_data])
        longitudes = np.array([d['longitude'] for d in filtered_data])
        if chart_type == "Population Distribution":
            self.tab_widget.setCurrentIndex(0)
            self.update_distribution_chart(populations)
        elif chart_type == "Population Density Heatmap":
            self.tab_widget.setCurrentIndex(1)
            self.update_heatmap_chart(latitudes, longitudes, populations)
        elif chart_type == "Population Trends":
            self.tab_widget.setCurrentIndex(2)
            self.update_trends_chart(filtered_data)
        elif chart_type == "Population Size Breakdown":
            self.tab_widget.setCurrentIndex(3)
            self.update_size_breakdown_chart(populations)
        elif chart_type == "Monthly Trends":
            self.tab_widget.setCurrentIndex(4)
            self.update_monthly_chart(filtered_data)
        elif chart_type == "Male/Female Ratio":
            self.tab_widget.setCurrentIndex(5)
            self.update_ratio_chart(filtered_data)
    
    def update_distribution_chart(self, populations):
        """Update the population distribution chart"""
        # Clear previous series
        self.distribution_chart.removeAllSeries()
        
        # Safely remove existing axes if they exist
        for axis in self.distribution_chart.axes():
            self.distribution_chart.removeAxis(axis)
        
        # Create bar series
        bar_set = QBarSet("Population")
        bar_set.setColor(QColor("#3498DB"))
        bar_set.setLabelColor(QColor("#e0e0e0"))
        
        # Create categories based on population ranges
        categories = ["0-100", "101-200", "201-300", "301-400", "401-500", "500+"]
        
        # Count populations in each category
        counts = [
            sum(1 for p in populations if p <= 100),
            sum(1 for p in populations if 100 < p <= 200),
            sum(1 for p in populations if 200 < p <= 300),
            sum(1 for p in populations if 300 < p <= 400),
            sum(1 for p in populations if 400 < p <= 500),
            sum(1 for p in populations if p > 500)
        ]
        
        # Add data to bar set
        for count in counts:
            bar_set.append(count)
        
        # Create series and add to chart
        series = QBarSeries()
        series.append(bar_set)
        self.distribution_chart.addSeries(series)
        
        # Set up axes
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(QColor("#e0e0e0"))
        self.distribution_chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(0, max(counts) + 1)
        axis_y.setLabelsColor(QColor("#e0e0e0"))
        self.distribution_chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        # Set labels
        self.distribution_chart.setTitle("Blue Crab Population Distribution")
        axis_x.setTitleText("Population Range")
        axis_x.setTitleBrush(QBrush(QColor("#e0e0e0")))
        axis_y.setTitleText("Number of Locations")
        axis_y.setTitleBrush(QBrush(QColor("#e0e0e0")))
        
        # Update legend
        self.distribution_chart.legend().setVisible(True)
        self.distribution_chart.legend().setAlignment(Qt.AlignBottom)
        self.distribution_chart.legend().setLabelColor(QColor("#e0e0e0"))
    
    def update_heatmap_chart(self, latitudes, longitudes, populations):
        """Update the population density heatmap"""
        # Clear previous plot and reset the figure
        self.heatmap_canvas.axes.clear()
        self.heatmap_canvas.fig.clear()
        self.heatmap_canvas.axes = self.heatmap_canvas.fig.add_subplot(111)
        
        # Create heatmap using Seaborn
        sns.set_style("dark")
        
        # Create a 2D histogram
        heatmap, xedges, yedges = np.histogram2d(
            longitudes, latitudes, bins=20, weights=populations
        )
        
        # Create a meshgrid
        x_centers = (xedges[:-1] + xedges[1:]) / 2
        y_centers = (yedges[:-1] + yedges[1:]) / 2
        X, Y = np.meshgrid(x_centers, y_centers)
        
        # Plot heatmap
        im = self.heatmap_canvas.axes.pcolormesh(
            X, Y, heatmap.T, cmap='Blues', shading='auto'
        )
        
        # Add colorbar
        cbar = self.heatmap_canvas.fig.colorbar(im, ax=self.heatmap_canvas.axes)
        cbar.set_label('Population Density', color='#e0e0e0')
        cbar.ax.yaxis.set_tick_params(color='#e0e0e0')
        cbar.outline.set_edgecolor('#e0e0e0')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#e0e0e0')
        
        # Set labels and title
        self.heatmap_canvas.axes.set_title('Blue Crab Population Density Heatmap', color='#3498DB')
        self.heatmap_canvas.axes.set_xlabel('Longitude', color='#e0e0e0')
        self.heatmap_canvas.axes.set_ylabel('Latitude', color='#e0e0e0')
        self.heatmap_canvas.axes.tick_params(colors='#e0e0e0')
        
        # Set background color
        self.heatmap_canvas.axes.set_facecolor('#0f2041')
        
        # Update canvas
        self.heatmap_canvas.fig.tight_layout()
        self.heatmap_canvas.draw()
    
    def update_trends_chart(self, crab_data):
        """Update the population trends chart"""
        # Clear previous plot
        self.trends_canvas.axes.clear()
        
        # Sort data by ID (assuming ID might have some chronological meaning)
        sorted_data = sorted(crab_data, key=lambda x: x['id'])
        
        # Extract data
        ids = [d['id'] for d in sorted_data]
        populations = [d['population'] for d in sorted_data]
        
        # Create line plot
        self.trends_canvas.axes.plot(ids, populations, marker='o', linestyle='-', color='#3498DB')
        
        # Calculate moving average if enough data points
        if len(populations) >= 3:
            window_size = 3
            moving_avg = np.convolve(populations, np.ones(window_size)/window_size, mode='valid')
            self.trends_canvas.axes.plot(
                ids[window_size-1:], moving_avg, 
                linestyle='--', color='#ef4444', label='Moving Avg (3)'
            )
        
        # Set labels and title
        self.trends_canvas.axes.set_title('Blue Crab Population Trends', color='#3498DB')
        self.trends_canvas.axes.set_xlabel('Sample ID', color='#e0e0e0')
        self.trends_canvas.axes.set_ylabel('Population', color='#e0e0e0')
        
        # Add grid and legend
        self.trends_canvas.axes.grid(True, linestyle='--', alpha=0.3, color='#4a5568')
        self.trends_canvas.axes.legend(facecolor='#0f2041', edgecolor='#3498DB', labelcolor='#e0e0e0')
        
        # Set background color
        self.trends_canvas.axes.set_facecolor('#0f2041')
        
        # Update canvas
        self.trends_canvas.fig.tight_layout()
        self.trends_canvas.draw()
    
    def update_size_breakdown_chart(self, populations):
        """Update the population size breakdown chart"""
        # Clear previous plot
        self.size_canvas.axes.clear()
        
        # Define size categories
        size_categories = {
            'Small (<100)': sum(1 for p in populations if p < 100),
            'Medium (100-300)': sum(1 for p in populations if 100 <= p < 300),
            'Large (300-500)': sum(1 for p in populations if 300 <= p < 500),
            'Very Large (500+)': sum(1 for p in populations if p >= 500)
        }
        
        # Create pie chart
        labels = list(size_categories.keys())
        sizes = list(size_categories.values())
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
        explode = (0.1, 0, 0, 0)  # explode the 1st slice (Small)
        
        # Plot pie chart
        wedges, texts, autotexts = self.size_canvas.axes.pie(
            sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90,
            textprops={'color': '#e0e0e0'}
        )
        
        # Set properties for better visibility
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
        
        self.size_canvas.axes.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Set title
        self.size_canvas.axes.set_title('Blue Crab Population Size Breakdown', color='#3498DB')
        
        # Set background color
        self.size_canvas.fig.patch.set_facecolor('#0f2041')
        
        # Update canvas
        self.size_canvas.fig.tight_layout()
        self.size_canvas.draw()
    
    def update_monthly_chart(self, crab_data):
        """Update the monthly trends chart using real data"""
        # Clear previous plot
        self.monthly_canvas.axes.clear()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        # Aggregate real data by month
        month_totals = [0] * 12
        month_counts = [0] * 12
        for d in crab_data:
            m = int(d['date_month']) - 1
            if 0 <= m < 12:
                month_totals[m] += d['population']
                month_counts[m] += 1
        # Calculate average population per month
        monthly_avg = [month_totals[i] // month_counts[i] if month_counts[i] > 0 else 0 for i in range(12)]
        # Create line plot
        self.monthly_canvas.axes.plot(months, monthly_avg, marker='o', linestyle='-', color='#3498DB', linewidth=2)
        # Fill area under the line
        self.monthly_canvas.axes.fill_between(months, monthly_avg, color='#3498DB', alpha=0.2)
        # Set labels and title
        self.monthly_canvas.axes.set_title('Monthly Blue Crab Population Trends', color='#3498DB')
        self.monthly_canvas.axes.set_xlabel('Month', color='#e0e0e0')
        self.monthly_canvas.axes.set_ylabel('Average Population', color='#e0e0e0')
        # Add grid
        self.monthly_canvas.axes.grid(True, linestyle='--', alpha=0.3, color='#4a5568')
        # Rotate x-axis labels for better readability
        self.monthly_canvas.axes.set_xticklabels(months, rotation=45, color='#e0e0e0')
        # Set background color
        self.monthly_canvas.axes.set_facecolor('#0f2041')
        # Update canvas
        self.monthly_canvas.fig.tight_layout()
        self.monthly_canvas.draw()

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

    def clear_all_charts(self):
        # Clear all chart canvases and show 'No Data' message
        self.distribution_chart.removeAllSeries()
        for axis in self.distribution_chart.axes():
            self.distribution_chart.removeAxis(axis)
        self.distribution_chart.setTitle("No Data")
        self.heatmap_canvas.axes.clear()
        self.heatmap_canvas.axes.text(0.5, 0.5, 'No Data', color='#e0e0e0', ha='center', va='center', fontsize=16)
        self.heatmap_canvas.draw()
        self.trends_canvas.axes.clear()
        self.trends_canvas.axes.text(0.5, 0.5, 'No Data', color='#e0e0e0', ha='center', va='center', fontsize=16)
        self.trends_canvas.draw()
        self.size_canvas.axes.clear()
        self.size_canvas.axes.text(0.5, 0.5, 'No Data', color='#e0e0e0', ha='center', va='center', fontsize=16)
        self.size_canvas.draw()
        self.monthly_canvas.axes.clear()
        self.monthly_canvas.axes.text(0.5, 0.5, 'No Data', color='#e0e0e0', ha='center', va='center', fontsize=16)
        self.monthly_canvas.draw()
        self.ratio_series.clear()
        self.ratio_chart.setTitle("No Data")

    def update_stat_cards_empty(self):
        # Set all stat cards to 0 or None
        self.distribution_chart.setTitle("No Data")
        if hasattr(self, 'parent') and hasattr(self.parent, 'analytics_cards'):
            self.parent.analytics_cards.update_analytics({
                'total_population': 0,
                'total_records': 0,
                'total_males': 0,
                'total_females': 0,
                'max_population': 0
            })
