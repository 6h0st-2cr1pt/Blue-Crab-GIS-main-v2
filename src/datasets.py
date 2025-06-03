from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTableWidget, QTableWidgetItem, QHeaderView,
                            QPushButton, QLineEdit, QComboBox, QFrame, QDialog,
                            QFormLayout, QSpinBox, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QColor, QFont

import qtawesome as qta
from datetime import datetime

from src.utils.database import DatabaseManager
from src.utils.notification import show_notification

class EditDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Crab Data")
        self.setModal(True)
        self.setFixedSize(400, 400)  # Reduced height
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: rgba(15, 32, 65, 0.95);
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
                font-weight: bold;
            }
            QLineEdit, QSpinBox, QComboBox {
                background-color: rgba(10, 25, 50, 0.7);
                border: 1px solid rgba(41, 128, 185, 0.5);
                border-radius: 8px;
                padding: 8px;
                color: #e0e0e0;
            }
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 1px solid rgba(52, 152, 219, 0.8);
                background-color: rgba(20, 40, 80, 0.7);
            }
            QPushButton {
                background-color: rgba(41, 128, 185, 0.8);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.9);
            }
            QComboBox QAbstractItemView {
                background-color: rgba(15, 32, 65, 0.95);
                color: #e0e0e0;
                selection-background-color: rgba(41, 128, 185, 0.8);
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Form
        form_layout = QFormLayout()
        
        # Month
        self.month_combo = QComboBox()
        self.month_combo.addItems([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        self.month_combo.setCurrentIndex(data['date_month'] - 1)
        form_layout.addRow("Month:", self.month_combo)
        
        # Year
        self.year_spin = QSpinBox()
        self.year_spin.setRange(1900, datetime.now().year)
        self.year_spin.setValue(data['date_year'])
        form_layout.addRow("Year:", self.year_spin)
        
        # Only keep male and female counts
        self.male_spin = QSpinBox()
        self.male_spin.setRange(0, 999999)
        self.male_spin.setValue(data['male_counts'])
        self.male_spin.valueChanged.connect(self.update_population)
        form_layout.addRow("Male Counts:", self.male_spin)
        
        self.female_spin = QSpinBox()
        self.female_spin.setRange(0, 999999)
        self.female_spin.setValue(data['female_counts'])
        self.female_spin.valueChanged.connect(self.update_population)
        form_layout.addRow("Female Counts:", self.female_spin)
        
        self.population_line = QLineEdit()
        self.population_line.setReadOnly(True)
        self.population_line.setText(str(data['population']))
        form_layout.addRow("Total Population:", self.population_line)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def update_population(self):
        """Update population based on counts"""
        male = self.male_spin.value()
        female = self.female_spin.value()
        
        population = male + female
        self.population_line.setText(str(population))
        
        if population == 0:
            self.population_line.setStyleSheet("""
                background-color: rgba(220, 38, 38, 0.3);
                border: 1px solid rgba(220, 38, 38, 0.8);
                border-radius: 8px;
                padding: 8px;
                color: #fca5a5;
            """)
        else:
            self.population_line.setStyleSheet("""
                background-color: rgba(10, 25, 50, 0.5);
                border: 1px solid rgba(41, 128, 185, 0.5);
                border-radius: 8px;
                padding: 8px;
                color: #e0e0e0;
            """)

    
    def get_data(self):
        """Get the edited data"""
        male = self.male_spin.value()
        female = self.female_spin.value()
        
        population = male + female
        
        if population == 0:
            raise ValueError("Population must be greater than 0")
        
        return {
            'date_month': self.month_combo.currentIndex() + 1,
            'date_year': self.year_spin.value(),
            'male_counts': male,
            'female_counts': female,
            'population': population
        }

class DatasetsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = DatabaseManager()
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Blue Crab Population Datasets")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #3498DB; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Description
        description = QLabel("View, search, edit, and manage blue crab population data.")
        description.setStyleSheet("color: #c0c0c0; margin-bottom: 20px;")
        layout.addWidget(description)
        
        # Search and filter controls
        controls_layout = QHBoxLayout()
        
        # Search
        search_container = QFrame()
        search_container.setStyleSheet("""
            background-color: rgba(15, 32, 65, 0.7);
            border-radius: 8px;
            border: 1px solid rgba(41, 128, 185, 0.5);
        """)
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(10, 5, 10, 5)
        
        search_icon = QLabel()
        search_icon_qta = qta.icon('fa5s.search', color='white')
        search_icon.setPixmap(search_icon_qta.pixmap(16, 16))
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID or Observer...")
        self.search_input.setStyleSheet("""
            border: none;
            padding: 5px;
            background-color: transparent;
            color: #e0e0e0;
        """)
        self.search_input.textChanged.connect(self.filter_data)
        
        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input)
        
        # Filters
        filter_label = QLabel("Population:")
        filter_label.setStyleSheet("margin-left: 10px; color: #e0e0e0;")
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Low (<100)", "Medium (100-500)", "High (>500)"])
        self.filter_combo.setStyleSheet("""
            background-color: rgba(15, 32, 65, 0.7);
            border: 1px solid rgba(41, 128, 185, 0.5);
            border-radius: 8px;
            padding: 5px;
            color: #e0e0e0;
        """)
        self.filter_combo.currentIndexChanged.connect(self.filter_data)
        
        year_label = QLabel("Year:")
        year_label.setStyleSheet("margin-left: 10px; color: #e0e0e0;")
        
        self.year_combo = QComboBox()
        self.year_combo.addItem("All Years")
        self.year_combo.setStyleSheet("""
            background-color: rgba(15, 32, 65, 0.7);
            border: 1px solid rgba(41, 128, 185, 0.5);
            border-radius: 8px;
            padding: 5px;
            color: #e0e0e0;
        """)
        self.year_combo.currentIndexChanged.connect(self.filter_data)
        
        # Action buttons
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setIcon(qta.icon('fa5s.sync-alt', color='white'))
        self.refresh_btn.clicked.connect(self.load_data)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(41, 128, 185, 0.8);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.9);
            }
        """)
        self.delete_selected_btn = QPushButton("Delete Selected")
        self.delete_selected_btn.setIcon(qta.icon('fa5s.trash', color='white'))
        self.delete_selected_btn.clicked.connect(self.delete_selected_records)
        self.delete_selected_btn.setStyleSheet(self.refresh_btn.styleSheet())
        self.delete_all_btn = QPushButton("Delete All")
        self.delete_all_btn.setIcon(qta.icon('fa5s.trash-alt', color='white'))
        self.delete_all_btn.clicked.connect(self.delete_all_records)
        self.delete_all_btn.setStyleSheet(self.refresh_btn.styleSheet())
        
        controls_layout.addWidget(search_container)
        controls_layout.addWidget(filter_label)
        controls_layout.addWidget(self.filter_combo)
        controls_layout.addWidget(year_label)
        controls_layout.addWidget(self.year_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(self.refresh_btn)
        controls_layout.addWidget(self.delete_selected_btn)
        controls_layout.addWidget(self.delete_all_btn)
        
        layout.addLayout(controls_layout)
        
        # Data table
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: rgba(15, 32, 65, 0.7);
                border: 1px solid rgba(41, 128, 185, 0.5);
                border-radius: 8px;
                color: #e0e0e0;
                gridline-color: rgba(41, 128, 185, 0.3);
            }
            QTableWidget::item {
                padding: 1px;
                border-bottom: 1px solid rgba(41, 128, 185, 0.3);
            }
            QTableWidget::item:selected {
                background-color: rgba(41, 128, 185, 0.5);
                color: white;
            }
            QHeaderView::section {
                background-color: rgba(41, 128, 185, 0.7);
                padding: 5px;
                border: none;
                border-right: 1px solid rgba(41, 128, 185, 0.5);
                border-bottom: 1px solid rgba(41, 128, 185, 0.5);
                font-weight: bold;
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
        """)
        
        # Set up table columns
        self.table.setColumnCount(11)  # Add checkbox column
        self.table.setHorizontalHeaderLabels([
            "", "ID", "Month", "Year", "Males", "Females", 
            "Population", "Observer", "Location", "Actions", "Created"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.table)
        
        # Load initial data
        self.load_data()
    
    def load_data(self):
        """Load data from database into table"""
        self.table.setRowCount(0)
        
        crab_data = self.db_manager.get_all_crab_data()
        
        if not crab_data:
            return
        
        # Populate year filter
        self.year_combo.clear()
        self.year_combo.addItem("All Years")
        years = sorted(set(data['date_year'] for data in crab_data))
        for year in years:
            self.year_combo.addItem(str(year))
        
        # Fill table
        self.table.setRowCount(len(crab_data))
        
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        for i, data in enumerate(crab_data):
            # Checkbox
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.table.setItem(i, 0, checkbox_item)
            
            # ID
            id_item = QTableWidgetItem(data['id'])
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            id_item.setForeground(QColor("#e0e0e0"))
            self.table.setItem(i, 1, id_item)
            
            # Month
            month_item = QTableWidgetItem(month_names[data['date_month'] - 1])
            month_item.setTextAlignment(Qt.AlignCenter)
            month_item.setForeground(QColor("#e0e0e0"))
            self.table.setItem(i, 2, month_item)
            
            # Year
            year_item = QTableWidgetItem(str(data['date_year']))
            year_item.setTextAlignment(Qt.AlignCenter)
            year_item.setForeground(QColor("#e0e0e0"))
            self.table.setItem(i, 3, year_item)
            
            # Only keep male and female counts
            male_item = QTableWidgetItem(str(data['male_counts']))
            male_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            male_item.setForeground(QColor("#06b6d4"))
            self.table.setItem(i, 4, male_item)
            
            female_item = QTableWidgetItem(str(data['female_counts']))
            female_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            female_item.setForeground(QColor("#ec4899"))
            self.table.setItem(i, 5, female_item)
            
            # Population
            pop_item = QTableWidgetItem(str(data['population']))
            pop_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            pop_item.setForeground(QColor("#f59e0b"))
            pop_item.setFont(QFont("Arial", 10, QFont.Bold))
            self.table.setItem(i, 6, pop_item)
            
            # Observer
            obs_item = QTableWidgetItem(data['observer_name'] or 'Unknown')
            obs_item.setForeground(QColor("#e0e0e0"))
            self.table.setItem(i, 7, obs_item)
            
            # Location
            loc_item = QTableWidgetItem(data['location_name'] or f"{data['latitude']:.3f}, {data['longitude']:.3f}")
            loc_item.setForeground(QColor("#e0e0e0"))
            self.table.setItem(i, 8, loc_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setSpacing(5)
            
            edit_btn = QPushButton()
            edit_btn.setIcon(qta.icon('fa5s.edit', color='#3b82f6'))
            edit_btn.setFixedSize(30, 25)
            edit_btn.setToolTip("Edit")
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(59, 130, 246, 0.2);
                    border: 1px solid rgba(59, 130, 246, 0.5);
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: rgba(59, 130, 246, 0.4);
                }
            """)
            edit_btn.clicked.connect(lambda checked, row=i: self.edit_record(row))
            
            delete_btn = QPushButton()
            delete_btn.setIcon(qta.icon('fa5s.trash', color='#ef4444'))
            delete_btn.setFixedSize(30, 25)
            delete_btn.setToolTip("Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(239, 68, 68, 0.2);
                    border: 1px solid rgba(239, 68, 68, 0.5);
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: rgba(239, 68, 68, 0.4);
                }
            """)
            delete_btn.clicked.connect(lambda checked, row=i: self.delete_record(row))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            
            self.table.setCellWidget(i, 9, actions_widget)
            
            # Created timestamp
            created_item = QTableWidgetItem(data['created_at'][:10] if data['created_at'] else '')
            created_item.setTextAlignment(Qt.AlignCenter)
            created_item.setForeground(QColor("#a0a0a0"))
            self.table.setItem(i, 10, created_item)
            
            # Color rows based on population
            if data['population'] < 100:
                row_color = QColor(59, 130, 246, 30)
            elif data['population'] <= 500:
                row_color = QColor(16, 185, 129, 30)
            else:
                row_color = QColor(239, 68, 68, 30)
            
            for j in range(10):
                if j != 9:  # Skip actions column (now at 9)
                    item = self.table.item(i, j)
                    if item:
                        item.setBackground(row_color)
    
    def filter_data(self):
        """Filter table data based on search and filter criteria"""
        search_text = self.search_input.text().lower()
        filter_idx = self.filter_combo.currentIndex()
        year_filter = self.year_combo.currentText()
        
        # Show all rows first
        for i in range(self.table.rowCount()):
            self.table.setRowHidden(i, False)
        
        # Apply filters
        for i in range(self.table.rowCount()):
            id_item = self.table.item(i, 1)
            pop_item = self.table.item(i, 6)
            year_item = self.table.item(i, 3)
            obs_item = self.table.item(i, 7)
            
            # Search filter
            search_match = (search_text == "" or 
                           search_text in id_item.text().lower() or
                           search_text in obs_item.text().lower())
            
            # Population filter
            pop_match = True
            if filter_idx > 0:
                population = int(pop_item.text())
                if filter_idx == 1:  # Low
                    pop_match = population < 100
                elif filter_idx == 2:  # Medium
                    pop_match = 100 <= population <= 500
                elif filter_idx == 3:  # High
                    pop_match = population > 500
            
            # Year filter
            year_match = True
            if year_filter != "All Years":
                year_match = year_item.text() == year_filter
            
            self.table.setRowHidden(i, not (search_match and pop_match and year_match))
    
    def edit_record(self, row):
        """Edit a record"""
        try:
            # Get record ID
            record_id = self.table.item(row, 1).text()
            
            # Get current data
            data = self.db_manager.get_crab_data_by_id(record_id)
            if not data:
                show_notification(self.parent, "Error", "Record not found")
                return
            
            # Open edit dialog
            dialog = EditDialog(data, self)
            if dialog.exec_() == QDialog.Accepted:
                try:
                    updated_data = dialog.get_data()
                    self.db_manager.update_crab_data(record_id, updated_data)
                    
                    show_notification(self.parent, "Success", "Record updated successfully")
                    self.load_data()  # Reload data
                    
                except ValueError as e:
                    show_notification(self.parent, "Validation Error", str(e))
                except Exception as e:
                    show_notification(self.parent, "Error", f"Failed to update record: {str(e)}")
                    
        except Exception as e:
            show_notification(self.parent, "Error", f"Failed to edit record: {str(e)}")
    
    def delete_record(self, row):
        """Delete a record"""
        try:
            # Get record ID
            record_id = self.table.item(row, 1).text()
            
            # Confirm deletion
            reply = QMessageBox.question(
                self, 
                "Confirm Deletion",
                f"Are you sure you want to delete record {record_id}?\n\nThis action cannot be undone.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.db_manager.delete_crab_data(record_id)
                show_notification(self.parent, "Success", "Record deleted successfully")
                self.load_data()  # Reload data
                
        except Exception as e:
            show_notification(self.parent, "Error", f"Failed to delete record: {str(e)}")

    def delete_selected_records(self):
        """Delete all selected records (checked checkboxes)"""
        rows_to_delete = []
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if item and item.checkState() == Qt.Checked:
                rows_to_delete.append(i)
        if not rows_to_delete:
            show_notification(self.parent, "No Selection", "No records selected for deletion.")
            return
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete {len(rows_to_delete)} selected records?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            for row in sorted(rows_to_delete, reverse=True):
                record_id = self.table.item(row, 1).text()
                self.db_manager.delete_crab_data(record_id)
            show_notification(self.parent, "Success", f"Deleted {len(rows_to_delete)} records.")
            self.load_data()

    def delete_all_records(self):
        """Delete all records from the database"""
        reply = QMessageBox.question(
            self, "Confirm Delete All",
            "Are you sure you want to delete ALL records?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db_manager.delete_all_crab_data()
            show_notification(self.parent, "Success", "All records deleted.")
            self.load_data()
