from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFileDialog, QFormLayout, QLineEdit, QTabWidget, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
                            QSplitter, QGroupBox, QSizePolicy, QSpinBox, QComboBox)
from PyQt5.QtCore import Qt, QMimeData, QUrl, QDate, pyqtSignal
from PyQt5.QtGui import QIcon, QColor, QPixmap, QFont, QPainter, QPainterPath, QLinearGradient

import pandas as pd
import os
from datetime import datetime
import qtawesome as qta

from src.utils.database import DatabaseManager
from src.utils.notification import show_notification

class DropArea(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumHeight(250)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(15, 32, 65, 0.8),
                    stop:1 rgba(10, 25, 50, 0.9));
                border: 2px dashed rgba(52, 152, 219, 0.6);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Create upload icon using qtawesome
        icon_container = QWidget()
        icon_container.setFixedHeight(80)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel()
        icon_label.setFixedSize(80, 80)
        icon_label.setAlignment(Qt.AlignCenter)
        try:
            upload_icon = qta.icon('fa5s.cloud-upload-alt', color='#52a3db', scale_factor=3)
            pixmap = upload_icon.pixmap(64, 64)
            if pixmap.isNull():
                raise Exception('Null pixmap')
            icon_label.setPixmap(pixmap)
        except Exception:
            try:
                upload_icon = qta.icon('fa5s.upload', color='#52a3db', scale_factor=3)
                pixmap = upload_icon.pixmap(64, 64)
                if pixmap.isNull():
                    raise Exception('Null pixmap')
                icon_label.setPixmap(pixmap)
            except Exception:
                icon_label.setText("⬆")
                icon_label.setStyleSheet("font-size: 48px; color: #52a3db;")
        
        # Main text
        text_label = QLabel("Drag & Drop CSV File Here")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 20px;
                font-weight: bold;
                background: transparent;
                border: none;
                margin: 10px 0;
            }
        """)
        
        # Separator text
        subtext_label = QLabel("or")
        subtext_label.setAlignment(Qt.AlignCenter)
        subtext_label.setStyleSheet("""
            QLabel {
                color: #a0a0a0;
                font-size: 14px;
                background: transparent;
                border: none;
                margin: 5px 0;
            }
        """)
        
        # Browse button
        button_container = QWidget()
        button_container.setFixedHeight(60)
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.browse_btn = QPushButton("Browse Files")
        self.browse_btn.setIcon(qta.icon('fa5s.folder-open', color='white'))
        self.browse_btn.setFixedSize(160, 45)
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(52, 152, 219, 0.9),
                    stop:1 rgba(41, 128, 185, 1.0));
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
                border: 1px solid rgba(52, 152, 219, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(65, 165, 235, 1.0),
                    stop:1 rgba(52, 152, 219, 1.0));
                border: 1px solid rgba(65, 165, 235, 0.5);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(41, 128, 185, 1.0),
                    stop:1 rgba(30, 100, 150, 1.0));
                transform: translateY(1px);
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(self.browse_btn)
        button_layout.addStretch()
        
        # File format info
        format_label = QLabel("Required CSV columns: Date Month, Date Year, Male Counts, Female Counts, Population, Observer Name, Latitude, Longitude")
        format_label.setAlignment(Qt.AlignCenter)
        format_label.setStyleSheet("""
            QLabel {
                color: #a0a0a0;
                font-size: 11px;
                background: transparent;
                border: none;
                margin: 15px 10px 5px 10px;
                padding: 10px;
                border-radius: 8px;
                background-color: rgba(10, 25, 50, 0.5);
            }
        """)
        format_label.setWordWrap(True)
        
        layout.addWidget(icon_container)
        layout.addWidget(text_label)
        layout.addWidget(subtext_label)
        layout.addWidget(button_container)
        layout.addWidget(format_label)
        layout.addStretch()
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and event.mimeData().urls()[0].toLocalFile().endswith('.csv'):
            event.acceptProposedAction()
            self.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(52, 152, 219, 0.4),
                        stop:1 rgba(41, 128, 185, 0.5));
                    border: 2px dashed rgba(65, 165, 235, 0.9);
                    border-radius: 20px;
                    padding: 20px;
                }
            """)
    
    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(15, 32, 65, 0.8),
                    stop:1 rgba(10, 25, 50, 0.9));
                border: 2px dashed rgba(52, 152, 219, 0.6);
                border-radius: 20px;
                padding: 20px;
            }
        """)
    
    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.parent().process_csv(file_path)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(15, 32, 65, 0.8),
                    stop:1 rgba(10, 25, 50, 0.9));
                border: 2px dashed rgba(52, 152, 219, 0.6);
                border-radius: 20px;
                padding: 20px;
            }
        """)

class UploadDataWidget(QWidget):
    data_changed = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = DatabaseManager()
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Upload Blue Crab Population Data")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #e0e0e0; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Description
        description = QLabel("Upload CSV file or manually enter detailed blue crab population data.")
        description.setStyleSheet("color: #c0c0c0; margin-bottom: 20px; font-size: 16px;")
        layout.addWidget(description)
        
        # Create horizontal layout for side-by-side sections
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # CSV Upload section
        csv_group = QGroupBox("CSV Upload")
        csv_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        csv_group.setStyleSheet("""
            QGroupBox {
                background-color: rgba(15, 32, 65, 0.5);
                border-radius: 15px;
                padding: 15px;
                border: 1px solid rgba(41, 128, 185, 0.3);
                color: #e0e0e0;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        csv_layout = QVBoxLayout(csv_group)
        csv_layout.setContentsMargins(15, 25, 15, 15)
        
        # Drop area for CSV
        self.drop_area = DropArea(self)
        self.drop_area.browse_btn.clicked.connect(self.browse_csv)
        csv_layout.addWidget(self.drop_area)
        
        # Preview area
        self.preview_label = QLabel("CSV Preview:")
        self.preview_label.setStyleSheet("font-weight: bold; margin-top: 20px; color: #e0e0e0;")
        self.preview_label.setVisible(False)
        
        self.preview_table = QTableWidget()
        self.preview_table.setStyleSheet("""
            QTableWidget {
                background-color: rgba(10, 25, 50, 0.7);
                border-radius: 10px;
                color: #e0e0e0;
                gridline-color: rgba(41, 128, 185, 0.3);
                border: 1px solid rgba(41, 128, 185, 0.3);
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
        """)
        self.preview_table.setVisible(False)
        
        self.upload_btn = QPushButton("Upload to Database")
        self.upload_btn.setIcon(qta.icon('fa5s.database', color='white'))
        self.upload_btn.setFixedSize(200, 40)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(41, 128, 185, 0.8);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.9);
            }
            QPushButton:pressed {
                background-color: rgba(41, 128, 185, 1.0);
            }
        """)
        self.upload_btn.setVisible(False)
        self.upload_btn.clicked.connect(self.upload_csv_to_db)
        
        csv_layout.addWidget(self.preview_label)
        csv_layout.addWidget(self.preview_table)
        
        upload_btn_container = QWidget()
        upload_btn_layout = QHBoxLayout(upload_btn_container)
        upload_btn_layout.setContentsMargins(0, 0, 0, 0)
        upload_btn_layout.addStretch()
        upload_btn_layout.addWidget(self.upload_btn)
        upload_btn_layout.addStretch()
        
        csv_layout.addWidget(upload_btn_container)
        
        # Manual Entry section
        manual_group = QGroupBox("Manual Entry")
        manual_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        manual_group.setStyleSheet("""
            QGroupBox {
                background-color: rgba(15, 32, 65, 0.5);
                border-radius: 15px;
                padding: 15px;
                border: 1px solid rgba(41, 128, 185, 0.3);
                color: #e0e0e0;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        manual_layout = QVBoxLayout(manual_group)
        manual_layout.setContentsMargins(15, 25, 15, 15)
        
        form_container = QFrame()
        form_container.setStyleSheet("""
            background-color: rgba(10, 25, 50, 0.7);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(41, 128, 185, 0.3);
        """)
        form_layout = QFormLayout(form_container)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(20)
        
        # Style for labels and inputs
        label_style = "color: #e0e0e0; font-weight: bold;"
        input_style = """
            QLineEdit, QSpinBox, QComboBox {
                background-color: rgba(15, 32, 65, 0.7);
                border: 1px solid rgba(41, 128, 185, 0.5);
                border-radius: 8px;
                padding: 8px;
                color: #e0e0e0;
            }
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 1px solid rgba(52, 152, 219, 0.8);
                background-color: rgba(20, 40, 80, 0.7);
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 16px;
                border-radius: 4px;
                background-color: rgba(41, 128, 185, 0.5);
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: rgba(52, 152, 219, 0.7);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: rgba(15, 32, 65, 0.95);
                color: #e0e0e0;
                selection-background-color: rgba(41, 128, 185, 0.8);
            }
        """
        
        # Date fields
        self.month_input = QComboBox()
        self.month_input.addItems([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        self.month_input.setStyleSheet(input_style)
        month_label = QLabel("Month:")
        month_label.setStyleSheet(label_style)
        
        self.year_input = QSpinBox()
        self.year_input.setRange(1900, datetime.now().year)
        self.year_input.setValue(datetime.now().year)
        self.year_input.setStyleSheet(input_style)
        year_label = QLabel("Year:")
        year_label.setStyleSheet(label_style)
        
        # Count fields
        self.male_input = QSpinBox()
        self.male_input.setRange(0, 999999)
        self.male_input.setStyleSheet(input_style)
        self.male_input.valueChanged.connect(self.update_population)
        male_label = QLabel("Male Counts:")
        male_label.setStyleSheet(label_style)
        
        self.female_input = QSpinBox()
        self.female_input.setRange(0, 999999)
        self.female_input.setStyleSheet(input_style)
        self.female_input.valueChanged.connect(self.update_population)
        female_label = QLabel("Female Counts:")
        female_label.setStyleSheet(label_style)
        
        self.population_input = QLineEdit()
        self.population_input.setReadOnly(True)
        self.population_input.setStyleSheet(input_style + "background-color: rgba(10, 25, 50, 0.5);")
        population_label = QLabel("Total Population:")
        population_label.setStyleSheet(label_style)
        
        # Observer and location fields
        self.observer_input = QLineEdit()
        self.observer_input.setStyleSheet(input_style)
        self.observer_input.textChanged.connect(self.validate_observer_name)
        observer_label = QLabel("Observer Name:")
        observer_label.setStyleSheet(label_style)
        
        self.latitude_input = QLineEdit()
        self.latitude_input.setStyleSheet(input_style)
        self.latitude_input.textChanged.connect(self.validate_coordinates)
        latitude_label = QLabel("Latitude:")
        latitude_label.setStyleSheet(label_style)
        
        self.longitude_input = QLineEdit()
        self.longitude_input.setStyleSheet(input_style)
        self.longitude_input.textChanged.connect(self.validate_coordinates)
        longitude_label = QLabel("Longitude:")
        longitude_label.setStyleSheet(label_style)
        
        # Add fields to form
        form_layout.addRow(month_label, self.month_input)
        form_layout.addRow(year_label, self.year_input)
        form_layout.addRow(male_label, self.male_input)
        form_layout.addRow(female_label, self.female_input)
        form_layout.addRow(population_label, self.population_input)
        form_layout.addRow(observer_label, self.observer_input)
        form_layout.addRow(latitude_label, self.latitude_input)
        form_layout.addRow(longitude_label, self.longitude_input)
        
        self.add_btn = QPushButton("Add Entry")
        self.add_btn.setIcon(qta.icon('fa5s.plus', color='white'))
        self.add_btn.setFixedSize(150, 40)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(41, 128, 185, 0.8);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.9);
            }
            QPushButton:pressed {
                background-color: rgba(41, 128, 185, 1.0);
            }
        """)
        self.add_btn.clicked.connect(self.add_manual_entry)
        
        manual_layout.addWidget(form_container)
        
        add_btn_container = QWidget()
        add_btn_layout = QHBoxLayout(add_btn_container)
        add_btn_layout.setContentsMargins(0, 10, 0, 0)
        add_btn_layout.addStretch()
        add_btn_layout.addWidget(self.add_btn)
        add_btn_layout.addStretch()
        
        manual_layout.addWidget(add_btn_container)
        manual_layout.addStretch()
        
        # Add both sections to the content layout
        content_layout.addWidget(csv_group, 1)
        content_layout.addWidget(manual_group, 1)
        
        layout.addLayout(content_layout)
    
    def update_population(self):
        """Update population based on sex counts"""
        male = self.male_input.value()
        female = self.female_input.value()
        
        population = male + female
        self.population_input.setText(str(population))
        
        if population == 0:
            self.population_input.setStyleSheet("""
                background-color: rgba(220, 38, 38, 0.3);
                border: 1px solid rgba(220, 38, 38, 0.8);
                border-radius: 8px;
                padding: 8px;
                color: #fca5a5;
            """)
        else:
            self.population_input.setStyleSheet("""
                background-color: rgba(10, 25, 50, 0.5);
                border: 1px solid rgba(41, 128, 185, 0.5);
                border-radius: 8px;
                padding: 8px;
                color: #e0e0e0;
            """)
    
    def browse_csv(self):
        """Open file dialog to browse for CSV files"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        
        if file_path:
            self.process_csv(file_path)
    
    def process_csv(self, file_path):
        """Process the selected CSV file"""
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            # Strip spaces from column names
            df.columns = df.columns.str.strip()
            
            # Check if required columns exist
            required_columns = [
                'date_month', 'date_year', 'male_counts', 'female_counts',
                'population', 'observer_name', 'latitude', 'longitude'
            ]
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                show_notification(
                    self.parent, 
                    "Error", 
                    f"CSV is missing required columns: {', '.join(missing_columns)}"
                )
                return
            
            # Convert month names to numbers if needed
            month_map = {
                'jan': 1, 'january': 1,
                'feb': 2, 'february': 2,
                'mar': 3, 'march': 3,
                'apr': 4, 'april': 4,
                'may': 5,
                'jun': 6, 'june': 6,
                'jul': 7, 'july': 7,
                'aug': 8, 'august': 8,
                'sep': 9, 'september': 9,
                'oct': 10, 'october': 10,
                'nov': 11, 'november': 11,
                'dec': 12, 'december': 12
            }
            def month_to_num(val):
                if isinstance(val, str):
                    val_stripped = val.strip().lower()
                    return month_map.get(val_stripped, val)
                return val
            df['date_month'] = df['date_month'].apply(month_to_num)
            
            # Convert numeric columns to appropriate types
            try:
                numeric_columns = [
                    'date_month', 'date_year', 'male_counts', 'female_counts',
                    'population', 'latitude', 'longitude'
                ]
                for col in numeric_columns:
                    for idx, val in enumerate(df[col], start=2):  # start=2 to account for header row
                        try:
                            float(val)
                        except Exception:
                            show_notification(
                                self.parent,
                                "Error",
                                f"Invalid value in row {idx}, column '{col}': '{val}'"
                            )
                            return
                    df[col] = pd.to_numeric(df[col])
            except Exception as e:
                show_notification(
                    self.parent,
                    "Error",
                    f"Invalid numeric data in CSV. Please check that all numeric fields contain valid numbers.\nDetails: {str(e)}"
                )
                return
            
            # Validate data
            validation_errors = []
            for index, row in df.iterrows():
                # Check population totals
                if row['male_counts'] + row['female_counts'] != row['population']:
                    validation_errors.append(f"Row {index + 1}: Male + Female counts don't equal population")
            
                # Check month range
                if not (1 <= row['date_month'] <= 12):
                    validation_errors.append(f"Row {index + 1}: Invalid month value")
            
            if validation_errors:
                show_notification(
                    self.parent, 
                    "Validation Error", 
                    "Data validation failed:\n" + "\n".join(validation_errors[:5]) + 
                    (f"\n... and {len(validation_errors) - 5} more errors" if len(validation_errors) > 5 else "")
                )
                return
            
            # Display preview
            self.preview_label.setVisible(True)
            self.preview_table.setVisible(True)
            self.upload_btn.setVisible(True)
            
            # Set up table
            self.preview_table.setRowCount(min(5, len(df)))
            self.preview_table.setColumnCount(len(df.columns))
            self.preview_table.setHorizontalHeaderLabels(df.columns)
            
            # Fill table with data
            for i in range(min(5, len(df))):
                for j in range(len(df.columns)):
                    item = QTableWidgetItem(str(df.iloc[i, j]))
                    item.setForeground(QColor("#e0e0e0"))
                    self.preview_table.setItem(i, j, item)
            
            # Adjust column widths
            self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            
            # Store the dataframe for later upload
            self.df = df
            
            show_notification(
                self.parent, 
                "Success", 
                f"CSV file loaded successfully. {len(df)} records found."
            )
            
        except Exception as e:
            show_notification(
                self.parent, 
                "Error", 
                f"Failed to process CSV: {str(e)}"
            )
    
    def upload_csv_to_db(self):
        """Upload the CSV data to the database"""
        try:
            # Convert dataframe to records
            records = []
            for _, row in self.df.iterrows():
                record = {
                    'date_month': int(row['date_month']),
                    'date_year': int(row['date_year']),
                    'male_counts': int(row['male_counts']),
                    'female_counts': int(row['female_counts']),
                    'population': int(row['population']),
                    'observer_name': str(row['observer_name']),
                    'latitude': float(row['latitude']),
                    'longitude': float(row['longitude'])
                }
                records.append(record)
            
            # Insert data into database
            self.db_manager.insert_many_crab_data(records)
            
            # Clear preview
            self.preview_label.setVisible(False)
            self.preview_table.setVisible(False)
            self.upload_btn.setVisible(False)
            self.preview_table.setRowCount(0)
            
            show_notification(
                self.parent, 
                "Success", 
                f"{len(records)} records uploaded to database successfully."
            )
            self.data_changed.emit()
            
        except Exception as e:
            show_notification(
                self.parent, 
                "Error", 
                f"Failed to upload data: {str(e)}"
            )
    
    def add_manual_entry(self):
        """Add a manually entered record to the database"""
        try:
            # Get values from inputs
            month_val = self.month_input.currentIndex() + 1
            year_val = self.year_input.value()
            male_val = self.male_input.value()
            female_val = self.female_input.value()
            observer_val = self.observer_input.text().strip()
            latitude_val = self.latitude_input.text().strip()
            longitude_val = self.longitude_input.text().strip()
            
            # Validate inputs
            if not all([observer_val, latitude_val, longitude_val]):
                show_notification(
                    self.parent, 
                    "Error", 
                    "Observer name, latitude, and longitude are required."
                )
                return
            
            try:
                latitude_val = float(latitude_val)
                longitude_val = float(longitude_val)
            except ValueError:
                show_notification(
                    self.parent, 
                    "Error", 
                    "Latitude and Longitude must be decimal numbers."
                )
                return
            
            # Validate population totals
            population = male_val + female_val
        
            if population == 0:
                show_notification(
                    self.parent, 
                    "Error", 
                    "Population must be greater than 0."
                )
                return
            
            # Insert into database
            record = {
                'date_month': month_val,
                'date_year': year_val,
                'male_counts': male_val,
                'female_counts': female_val,
                'population': population,
                'observer_name': observer_val,
                'latitude': latitude_val,
                'longitude': longitude_val
            }
            
            record_id = self.db_manager.insert_crab_data(record)
            
            # Clear inputs
            self.male_input.setValue(0)
            self.female_input.setValue(0)
            self.observer_input.clear()
            self.latitude_input.clear()
            self.longitude_input.clear()
            self.population_input.clear()
            
            show_notification(
                self.parent, 
                "Success", 
                f"Record added to database successfully with ID: {record_id}"
            )
            self.data_changed.emit()
            
        except Exception as e:
            show_notification(
                self.parent, 
                "Error", 
                f"Failed to add record: {str(e)}"
            )

    def validate_observer_name(self):
        """Validate and format observer name to only contain letters and convert to uppercase"""
        text = self.observer_input.text()
        # Remove any non-letter characters
        filtered_text = ''.join(c for c in text if c.isalpha())
        # Convert to uppercase
        filtered_text = filtered_text.upper()
        # Only update if the text has changed
        if filtered_text != text:
            self.observer_input.setText(filtered_text)

    def validate_coordinates(self):
        """Validate and format coordinate inputs to only contain numbers and decimal points"""
        # Get the sender (which input field triggered the validation)
        sender = self.sender()
        if not sender:
            return
            
        text = sender.text()
        # Remove any non-numeric characters except decimal point
        filtered_text = ''.join(c for c in text if c.isdigit() or c == '.')
        
        # Ensure only one decimal point
        if filtered_text.count('.') > 1:
            parts = filtered_text.split('.')
            filtered_text = parts[0] + '.' + ''.join(parts[1:])
            
        # Only update if the text has changed
        if filtered_text != text:
            sender.setText(filtered_text)
