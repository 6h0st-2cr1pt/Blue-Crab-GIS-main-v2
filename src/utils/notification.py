from PyQt5.QtWidgets import QMessageBox

class NotificationManager:
    def __init__(self, parent=None):
        self.parent = parent
    
    def show_notification(self, title, message, icon=QMessageBox.Information):
        """Show a notification message box"""
        msg_box = QMessageBox(self.parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: rgba(10, 25, 50, 0.9);
                color: #e0e0e0;
                border: 1px solid rgba(41, 128, 185, 0.5);
                border-radius: 10px;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                background-color: rgba(41, 128, 185, 0.8);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.9);
            }
        """)
        msg_box.exec_()

def show_notification(parent, title, message, icon=QMessageBox.Information):
    """Utility function to show a notification"""
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(icon)
    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: rgba(10, 25, 50, 0.9);
            color: #e0e0e0;
            border: 1px solid rgba(41, 128, 185, 0.5);
            border-radius: 10px;
        }
        QLabel {
            color: #e0e0e0;
        }
        QPushButton {
            background-color: rgba(41, 128, 185, 0.8);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: rgba(52, 152, 219, 0.9);
        }
    """)
    msg_box.exec_()
