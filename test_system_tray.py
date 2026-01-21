#!/usr/bin/env python3
"""
Simple test script to verify SystemTray functionality.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.system_tray import SystemTray
from ui.main_window import MainWindow


def main():
    """Test system tray integration."""
    print("Creating QApplication...")
    app = QApplication(sys.argv)

    print("Creating SystemTray...")
    system_tray = SystemTray()

    if system_tray.is_available():
        print("✓ System tray is available")
        system_tray.show()
        print("✓ Tray icon shown")

        # Show test message
        system_tray.show_message(
            "Test",
            "System tray is working!",
            SystemTray.MessageIcon.Information
        )
        print("✓ Test message sent")

        # Create main window with tray integration
        print("Creating MainWindow with system tray...")
        window = MainWindow(system_tray=system_tray)
        window.show()
        print("✓ Main window shown")

        print("\n=== System Tray Test Started ===")
        print("Instructions:")
        print("1. Close the main window (X button) - should minimize to tray")
        print("2. Double-click the tray icon - should restore window")
        print("3. Right-click tray icon - should show context menu (Show, Info, Exit)")
        print("4. Click Exit to quit the application")
        print("\nNote: If no custom icon is found, a default Qt icon will be used.")

        # Run event loop
        return app.exec()
    else:
        print("✗ System tray is NOT available on this platform")
        # Still show window for testing
        window = MainWindow(system_tray=system_tray)
        window.show()
        return app.exec()


if __name__ == "__main__":
    sys.exit(main())
