"""
Unit tests for GlobalHotkey.

Tests global hotkey registration, signal emission, and error handling.
"""

import sys
import time
import threading
from unittest.mock import Mock, patch

import pytest
from PySide6.QtCore import QObject, Signal

from src.hotkey.global_hotkey import GlobalHotkey


class TestGlobalHotkey:
    """Test suite for GlobalHotkey class."""

    def test_initialization(self):
        """Test that GlobalHotkey initializes correctly."""
        hotkey_manager = GlobalHotkey()

        assert hotkey_manager._is_running is False
        assert hotkey_manager._hotkey_listener is None
        assert hasattr(hotkey_manager, 'hotkey_activated')

    def test_default_hotkey_platform_detection(self):
        """Test that default hotkey is correctly set based on platform."""
        hotkey_manager = GlobalHotkey()

        if sys.platform == 'darwin':
            assert hotkey_manager.default_hotkey == '<cmd>+<period>'
        else:
            # Windows, Linux, and others
            assert hotkey_manager.default_hotkey == '<ctrl>+<period>'

    @patch('src.hotkey.global_hotkey.keyboard.GlobalHotKeys')
    def test_register_default_hotkey(self, mock_global_hotkeys):
        """Test registering the default platform hotkey."""
        # Setup mock
        mock_listener = Mock()
        mock_global_hotkeys.return_value = mock_listener

        hotkey_manager = GlobalHotkey()
        success = hotkey_manager.register()

        assert success is True
        assert hotkey_manager._is_running is True

        # Verify listener was created with correct hotkey
        expected_hotkey = hotkey_manager.default_hotkey
        mock_global_hotkeys.assert_called_once()
        hotkeys_arg = mock_global_hotkeys.call_args[0][0]
        assert expected_hotkey in hotkeys_arg

        # Verify listener was started
        mock_listener.start.assert_called_once()

    @patch('src.hotkey.global_hotkey.keyboard.GlobalHotKeys')
    def test_register_custom_hotkey(self, mock_global_hotkeys):
        """Test registering a custom hotkey combination."""
        mock_listener = Mock()
        mock_global_hotkeys.return_value = mock_listener

        hotkey_manager = GlobalHotkey()
        custom_hotkey = '<ctrl>+<shift>+h'
        success = hotkey_manager.register(hotkey=custom_hotkey)

        assert success is True
        assert hotkey_manager._is_running is True

        # Verify custom hotkey was used
        hotkeys_arg = mock_global_hotkeys.call_args[0][0]
        assert custom_hotkey in hotkeys_arg

    @patch('src.hotkey.global_hotkey.keyboard.GlobalHotKeys')
    def test_register_custom_callback(self, mock_global_hotkeys):
        """Test registering with a custom callback function."""
        mock_listener = Mock()
        mock_global_hotkeys.return_value = mock_listener

        hotkey_manager = GlobalHotkey()
        custom_callback = Mock()
        success = hotkey_manager.register(callback=custom_callback)

        assert success is True

        # Verify custom callback was used
        hotkeys_arg = mock_global_hotkeys.call_args[0][0]
        registered_callback = hotkeys_arg[hotkey_manager.default_hotkey]
        assert registered_callback == custom_callback

    @patch('src.hotkey.global_hotkey.keyboard.GlobalHotKeys')
    def test_register_already_registered(self, mock_global_hotkeys):
        """Test that registering twice returns False."""
        mock_listener = Mock()
        mock_global_hotkeys.return_value = mock_listener

        hotkey_manager = GlobalHotkey()
        first_success = hotkey_manager.register()
        second_success = hotkey_manager.register()

        assert first_success is True
        assert second_success is False

    @patch('src.hotkey.global_hotkey.keyboard.GlobalHotKeys')
    def test_register_duplicate_hotkey_error(self, mock_global_hotkeys):
        """Test that duplicate hotkey registration raises an exception."""
        # Simulate pynput raising an exception for duplicate hotkey
        mock_global_hotkeys.side_effect = Exception("Hotkey already in use")

        hotkey_manager = GlobalHotkey()

        with pytest.raises(Exception) as exc_info:
            hotkey_manager.register()

        assert "Failed to register hotkey" in str(exc_info.value)
        assert "already in use" in str(exc_info.value)

    @patch('src.hotkey.global_hotkey.keyboard.GlobalHotKeys')
    def test_unregister(self, mock_global_hotkeys):
        """Test unregistering a hotkey."""
        mock_listener = Mock()
        mock_global_hotkeys.return_value = mock_listener

        hotkey_manager = GlobalHotkey()
        hotkey_manager.register()
        success = hotkey_manager.unregister()

        assert success is True
        assert hotkey_manager._is_running is False
        assert hotkey_manager._hotkey_listener is None

        # Verify listener was stopped
        mock_listener.stop.assert_called_once()

    def test_unregister_when_not_registered(self):
        """Test unregistering when no hotkey is registered."""
        hotkey_manager = GlobalHotkey()
        success = hotkey_manager.unregister()

        assert success is False

    @patch('src.hotkey.global_hotkey.keyboard.GlobalHotKeys')
    def test_is_registered(self, mock_global_hotkeys):
        """Test checking if hotkey is registered."""
        mock_listener = Mock()
        mock_global_hotkeys.return_value = mock_listener

        hotkey_manager = GlobalHotkey()

        # Initially not registered
        assert hotkey_manager.is_registered() is False

        # After registration
        hotkey_manager.register()
        assert hotkey_manager.is_registered() is True

        # After unregistration
        hotkey_manager.unregister()
        assert hotkey_manager.is_registered() is False

    @patch('src.hotkey.global_hotkey.keyboard.GlobalHotKeys')
    def test_signal_emission_on_hotkey(self, mock_global_hotkeys, qtbot):
        """Test that hotkey_activated signal is emitted when hotkey is pressed."""
        mock_listener = Mock()
        mock_global_hotkeys.return_value = mock_listener

        hotkey_manager = GlobalHotkey()
        hotkey_manager.register()

        # Track signal emissions
        signal_emitted = False

        def on_hotkey_activated():
            nonlocal signal_emitted
            signal_emitted = True

        hotkey_manager.hotkey_activated.connect(on_hotkey_activated)

        # Simulate hotkey press by calling the registered callback
        hotkeys_arg = mock_global_hotkeys.call_args[0][0]
        registered_callback = hotkeys_arg[hotkey_manager.default_hotkey]
        registered_callback()

        # Give Qt event loop time to process
        qtbot.wait(100)

        assert signal_emitted is True

    @patch('src.hotkey.global_hotkey.keyboard.GlobalHotKeys')
    def test_multiple_hotkeys_sequentially(self, mock_global_hotkeys):
        """Test registering and unregistering multiple hotkeys sequentially."""
        mock_listener = Mock()
        mock_global_hotkeys.return_value = mock_listener

        hotkey_manager = GlobalHotkey()

        # First hotkey
        first_success = hotkey_manager.register(hotkey='<ctrl>+<a>')
        assert first_success is True

        hotkey_manager.unregister()

        # Second hotkey
        second_success = hotkey_manager.register(hotkey='<ctrl>+<b>')
        assert second_success is True

        hotkey_manager.unregister()

        # Verify listener was created and stopped twice
        assert mock_global_hotkeys.call_count == 2
        assert mock_listener.start.call_count == 2
        assert mock_listener.stop.call_count == 2

    @patch('src.hotkey.global_hotkey.keyboard.GlobalHotKeys')
    def test_cleanup_on_deletion(self, mock_global_hotkeys):
        """Test that hotkey is cleaned up when object is deleted."""
        mock_listener = Mock()
        mock_global_hotkeys.return_value = mock_listener

        hotkey_manager = GlobalHotkey()
        hotkey_manager.register()

        # Explicitly call __del__ to test cleanup logic
        # Note: In production, Python's GC calls this automatically
        hotkey_manager.__del__()

        # Verify cleanup happened
        mock_listener.stop.assert_called_once()

    @patch('src.hotkey.global_hotkey.keyboard.GlobalHotKeys')
    def test_unregister_error_handling(self, mock_global_hotkeys):
        """Test that unregister handles errors gracefully."""
        mock_listener = Mock()
        mock_listener.stop.side_effect = Exception("Stop failed")
        mock_global_hotkeys.return_value = mock_listener

        hotkey_manager = GlobalHotkey()
        hotkey_manager.register()

        # Should return False on error
        success = hotkey_manager.unregister()
        assert success is False

    def test_signal_thread_safety(self, qtbot):
        """
        Test that signal emission is thread-safe.

        This test verifies that signals emitted from background threads
        are properly delivered to Qt's main thread.
        """
        hotkey_manager = GlobalHotkey()

        emissions = []

        def on_hotkey_activated():
            emissions.append(True)

        hotkey_manager.hotkey_activated.connect(on_hotkey_activated)

        # Simulate background thread emission
        def emit_from_background():
            hotkey_manager._emit_signal()

        thread = threading.Thread(target=emit_from_background)
        thread.start()
        thread.join()

        # Give Qt time to process
        qtbot.wait(100)

        assert len(emissions) == 1
