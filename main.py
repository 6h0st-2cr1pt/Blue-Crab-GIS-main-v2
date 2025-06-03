import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

from src.splash_screen import SplashScreen
from src.main_window import MainWindow

if __name__ == "__main__":
    # Enable hardware acceleration
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-gpu --ignore-gpu-blacklist"
    
    app = QApplication(sys.argv)
    
    # Show splash screen
    splash = SplashScreen()
    splash.show()
    
    # Create main window but don't show it yet
    main_window = MainWindow()
    
    # Function to close splash and show main window
    def show_main():
        splash.close()
        main_window.show()
    
    # Close splash and show main after 2.5 seconds
    QTimer.singleShot(2500, show_main)
    
    sys.exit(app.exec_())
