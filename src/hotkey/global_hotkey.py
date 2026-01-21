"""
Global Hotkey Manager - Cross-platform global hotkey support.

Provides global hotkey functionality using pynput library.
Supports Windows, macOS, and Linux with platform-specific hotkey combinations.
"""

import sys
import threading
from typing import Callable, Optional

from pynput import keyboard


class HotkeySignal:
    """Simple signal replacement for cross-platform hotkey callbacks."""

    def __init__(self):
        self._callbacks = []
        self._lock = threading.Lock()

    def connect(self, callback: Callable):
        """Connect a callback to this signal."""
        with self._lock:
            self._callbacks.append(callback)

    def emit(self):
        """Emit the signal (call all connected callbacks)."""
        with self._lock:
            for callback in self._callbacks:
                try:
                    callback()
                except Exception as e:
                    print(f"Error in hotkey callback: {e}")


class GlobalHotkey:
    """
    Cross-platform global hotkey manager.

    Features:
    - Platform-specific hotkeys (Ctrl+Alt+T for Windows/Linux, Cmd+Alt+T for macOS)
    - Thread-safe signal emission
    - Automatic cleanup on destruction
    - Support for multiple hotkeys
    """

    # Signal emitted when the hotkey is activated
    hotkey_activated = HotkeySignal()

    def __init__(self):
        """Initialize the global hotkey manager."""
        self._hotkey_listener: Optional[keyboard.GlobalHotKeys] = None
        self._is_running = False
        self._platform = sys.platform

    @property
    def default_hotkey(self) -> str:
        """
        Get the default hotkey combination for the current platform.

        Returns:
            str: Platform-specific hotkey combination
                - Windows/Linux: '<ctrl>+<alt>+t'
                - macOS: '<cmd>+<alt>+t'
        """
        if self._platform == 'darwin':
            return '<cmd>+<alt>+t'
        else:
            return '<ctrl>+<alt>+t'

    def register(self, hotkey: Optional[str] = None, callback: Optional[Callable] = None) -> bool:
        """
        Register a global hotkey.

        Args:
            hotkey: Hotkey combination string (e.g., '<ctrl>+<alt>+t').
                   If None, uses the platform default.
            callback: Optional callback function. If None, uses the hotkey_activated signal.

        Returns:
            bool: True if registration successful, False otherwise

        Raises:
            Exception: If hotkey registration fails (e.g., hotkey already in use)
        """
        if self._is_running:
            return False

        # Use default hotkey if none provided
        if hotkey is None:
            hotkey = self.default_hotkey

        # Prepare callback
        if callback is None:
            callback = self._emit_signal

        try:
            # Create hotkey map
            hotkeys = {hotkey: callback}

            # Create and start the listener
            self._hotkey_listener = keyboard.GlobalHotKeys(hotkeys)
            self._hotkey_listener.start()
            self._is_running = True

            print(f"Global hotkey registered successfully: {hotkey}")
            return True

        except Exception as e:
            # Re-raise with more context
            print(f"Failed to register hotkey '{hotkey}': {str(e)}")
            return False

    def unregister(self) -> bool:
        """
        Unregister the global hotkey.

        Returns:
            bool: True if unregistration successful, False if not registered
        """
        if not self._is_running or self._hotkey_listener is None:
            return False

        try:
            self._hotkey_listener.stop()
            self._hotkey_listener = None
            self._is_running = False
            return True

        except Exception:
            return False

    def is_registered(self) -> bool:
        """
        Check if a hotkey is currently registered.

        Returns:
            bool: True if hotkey is registered and active
        """
        return self._is_running

    def _emit_signal(self):
        """
        Internal callback to emit the hotkey_activated signal.

        This method is called in a background thread by pynput.
        """
        self.hotkey_activated.emit()

    def __del__(self):
        """Cleanup: unregister hotkey when object is destroyed."""
        self.unregister()

