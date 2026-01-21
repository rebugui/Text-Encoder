"""
SystemTray - System tray integration for Text Encoder.

Features:
- Minimize to system tray on close
- Restore window by double-clicking tray icon
- Context menu: Show, Info, Exit
- Cross-platform icon support (Windows .ico, macOS/Linux .png)
- Copyright info in Info dialog
"""

import sys
import threading
from pathlib import Path
from typing import Optional, Callable

import pyperclip


class SystemTray:
    """
    System tray icon handler for Text Encoder.

    Uses pystray for cross-platform system tray support.

    Callbacks:
        show_requested: Called when Show is clicked
        info_requested: Called when Info is clicked
        exit_requested: Called when Exit is clicked
    """

    COPYRIGHT_TEXT = "@Copyright: Copyright (c) 2026 Yang Uhyeok (양우혁). All rights reserved."

    def __init__(self):
        """Initialize system tray."""
        # Callbacks
        self._on_show_requested: Optional[Callable[[], None]] = None
        self._on_exit_requested: Optional[Callable[[], None]] = None
        self._on_info_requested: Optional[Callable[[], None]] = None

        # State
        self.icon = None
        self.running = False

        # Check if we can import pystray
        try:
            import pystray
            self.pystray = pystray
            self._available = True
        except ImportError:
            print("Warning: pystray not available. System tray disabled.")
            self._available = False
            self.pystray = None

    def is_available(self) -> bool:
        """
        Check if system tray is available.

        Returns:
            True if tray is available
        """
        return self._available

    def create_icon(self, icon_path: Path = None):
        """
        Create system tray icon.

        Args:
            icon_path: Optional path to custom icon
        """
        if not self._available:
            return

        from PIL import Image

        # Load or create icon
        if icon_path and icon_path.exists():
            icon_image = Image.open(str(icon_path))
        else:
            # Create simple icon
            icon_image = self._create_default_icon()

        # Create menu
        menu = self.pystray.Menu(
            self.pystray.MenuItem("Show", self._on_show_clicked),
            self.pystray.Menu.SEPARATOR,
            self.pystray.MenuItem("Info", self._on_info_clicked),
            self.pystray.MenuItem("Exit", self._on_exit_clicked)
        )

        # Create icon
        self.icon = self.pystray.Icon(
            "Text Encoder",
            icon_image,
            "Text Encoder",
            menu
        )

    def _create_default_icon(self):
        """
        Create default icon image.

        Returns:
            PIL Image for icon
        """
        from PIL import Image, ImageDraw, ImageFont

        # Create 64x64 image
        size = 64
        image = Image.new("RGB", (size, size), color="#1f6aa5")
        draw = ImageDraw.Draw(image)

        # Draw "TE" text
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()

        text = "TE"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (size - text_width) // 2
        y = (size - text_height) // 2 - 2

        draw.text((x, y), text, fill="white", font=font)

        return image

    def _on_show_clicked(self):
        """Handle Show menu action."""
        if self._on_show_requested:
            self._on_show_requested()

    def _on_info_clicked(self):
        """Handle Info menu action - show about dialog."""
        # Trigger callback to let main window handle the dialog
        if self._on_info_requested:
            self._on_info_requested()
        else:
            # Fallback: print to console
            info_text = f"""Text Encoder

Extended GUI Text Utility Tool
Supports 80+ transformation algorithms

Version: 1.0.0
Platform: Cross-platform (Windows/macOS/Linux)

{self.COPYRIGHT_TEXT}"""
            print(info_text)

    def _on_exit_clicked(self):
        """Handle Exit menu action."""
        if self._on_exit_requested:
            self._on_exit_requested()

    def run_in_thread(self):
        """Run icon in background thread."""
        if not self._available or not self.icon:
            return

        self.running = True
        thread = threading.Thread(target=self.icon.run, daemon=True)
        thread.start()

    def stop(self):
        """Stop system tray icon."""
        if self.icon and self.running:
            self.icon.stop()
            self.running = False

    def show(self):
        """Show the system tray icon."""
        # Icon is shown by default when run() is called
        pass

    def hide(self):
        """Hide the system tray icon."""
        # pystray doesn't have hide, use stop() instead
        pass

    def show_message(self, title: str, message: str):
        """
        Show notification from tray icon.

        Args:
            title: Message title
            message: Message content
        """
        if self.icon:
            self.icon.notify(message, title)

    def set_show_callback(self, callback: Callable[[], None]):
        """
        Set callback for Show action.

        Args:
            callback: Function to call when Show is clicked
        """
        self._on_show_requested = callback

    def set_exit_callback(self, callback: Callable[[], None]):
        """
        Set callback for Exit action.

        Args:
            callback: Function to call when Exit is clicked
        """
        self._on_exit_requested = callback

    def set_info_callback(self, callback: Callable[[], None]):
        """
        Set callback for Info action.

        Args:
            callback: Function to call when Info is clicked
        """
        self._on_info_requested = callback
