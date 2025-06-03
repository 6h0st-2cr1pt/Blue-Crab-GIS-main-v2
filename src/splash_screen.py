from PyQt5.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QWidget, QApplication
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPixmap, QFont, QColor, QPainter, QPainterPath, QLinearGradient, QPen

import qtawesome as qta

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        
        # Create a pixmap for the splash screen
        pixmap = QPixmap(500, 300)
        pixmap.fill(Qt.transparent)  # Make transparent for rounded corners
        
        # Add content to the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw rounded rectangle background
        path = QPainterPath()
        path.addRoundedRect(0, 0, 500, 300, 20, 20)
        
        # Create a dark blue gradient
        gradient = QLinearGradient(0, 0, 0, 300)
        gradient.setColorAt(0, QColor(15, 32, 65))  # Dark blue at top
        gradient.setColorAt(1, QColor(5, 15, 40))   # Even darker blue at bottom
        painter.fillPath(path, gradient)
        
        # Draw a subtle pattern overlay
        pen = QPen(QColor(41, 128, 185, 30))
        pen.setWidth(1)
        painter.setPen(pen)
        for i in range(0, 500, 20):
            painter.drawLine(i, 0, i + 100, 300)
        
        # Draw logo using qtawesome
        water_icon = qta.icon('fa5s.water', color='#3b82f6', scale_factor=4)
        water_pixmap = water_icon.pixmap(80, 80)
        painter.drawPixmap(210, 60, water_pixmap)
        
        # Draw text
        painter.setPen(QColor(41, 128, 185))
        painter.setFont(QFont("Arial", 28, QFont.Bold))
        painter.drawText(pixmap.rect().adjusted(0, 50, 0, 0), Qt.AlignCenter, "Blue Crab GIS")
        
        painter.setPen(QColor("#e0e0e0"))
        painter.setFont(QFont("Arial", 14))
        painter.drawText(pixmap.rect().adjusted(0, 180, 0, 0), Qt.AlignCenter, "Loading...")
        
        # Draw a progress bar
        progress_rect = QRect(100, 200, 300, 10)
        painter.setBrush(QColor(10, 25, 50))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(progress_rect, 5, 5)
        
        progress_fill = QRect(100, 200, 150, 10)
        painter.setBrush(QColor(41, 128, 185))
        painter.drawRoundedRect(progress_fill, 5, 5)
        
        # Draw version
        painter.setPen(QColor("#a0a0a0"))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(QRect(0, 260, 480, 30), Qt.AlignRight, "Version 1.0.0")
        
        painter.end()
        
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())
        
        # Center on screen
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - pixmap.width()) // 2
        y = (screen_geometry.height() - pixmap.height()) // 2
        self.move(x, y)