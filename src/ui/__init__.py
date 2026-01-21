"""
UI package.

Contains all user interface components (CustomTkinter-based):
- main_window: Main application window
- sidebar: Algorithm categories and search with CTkComboBox
- content_area: Input/output fields with separate Encode/Decode buttons
- system_tray: System tray integration with pystray
"""

from ui.main_window import MainWindow
from ui.sidebar import Sidebar
from ui.content_area import ContentArea
from ui.system_tray import SystemTray

__all__ = ['MainWindow', 'Sidebar', 'ContentArea', 'SystemTray']
