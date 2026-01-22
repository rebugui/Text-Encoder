"""
State Manager - Cross-platform application state persistence.

Provides simple key-value storage with platform-specific config locations:
- Windows: %APPDATA%/Text Encoder/
- macOS: ~/Library/Application Support/Text Encoder/
- Linux: ~/.config/text-encoder/
"""

import sys
import json
from pathlib import Path
from typing import Any, Optional
import threading


class StateManager:
    """
    Cross-platform application state persistence manager.

    Features:
    - Platform-specific config directory locations
    - Thread-safe operations
    - Auto-save on modification
    - Simple dict-like interface
    """

    _instance: Optional['StateManager'] = None
    _lock = threading.Lock()

    def __new__(cls) -> 'StateManager':
        """Singleton pattern to ensure only one instance exists."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the state manager (only once)."""
        if self._initialized:
            return

        self._config_dir = self._get_config_dir()
        self._config_file = self._config_dir / "state.json"
        self._state: dict[str, Any] = {}
        self._lock = threading.Lock()

        # Ensure config directory exists
        self._config_dir.mkdir(parents=True, exist_ok=True)

        # Load existing state
        self._load()

        self._initialized = True

    def _get_config_dir(self) -> Path:
        """
        Get platform-specific config directory.

        Returns:
            Path to config directory
        """
        if sys.platform == "win32":
            # Windows: %APPDATA%/Text Encoder/
            appdata = Path.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')
            config_dir = appdata / "Text Encoder"
        elif sys.platform == "darwin":
            # macOS: ~/Library/Application Support/Text Encoder/
            config_dir = Path.home() / "Library" / "Application Support" / "Text Encoder"
        else:
            # Linux: ~/.config/text-encoder/
            config_dir = Path.home() / ".config" / "text-encoder"

        return config_dir

    def _load(self):
        """Load state from config file."""
        try:
            if self._config_file.exists():
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    self._state = json.load(f)
                    print(f"State loaded from: {self._config_file}")
            else:
                self._state = {}
                print(f"No existing state file, starting fresh: {self._config_file}")
        except Exception as e:
            print(f"Error loading state: {e}")
            self._state = {}

    def _save(self):
        """Save state to config file."""
        try:
            with self._lock:
                # Ensure directory exists
                self._config_dir.mkdir(parents=True, exist_ok=True)

                # Write to temporary file first (atomic write)
                temp_file = self._config_file.with_suffix('.tmp')
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(self._state, f, indent=2, ensure_ascii=False)

                # Replace old file with new file
                temp_file.replace(self._config_file)

        except Exception as e:
            print(f"Error saving state: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from state.

        Args:
            key: State key
            default: Default value if key doesn't exist

        Returns:
            Stored value or default
        """
        with self._lock:
            return self._state.get(key, default)

    def set(self, key: str, value: Any, save: bool = True):
        """
        Set a value in state.

        Args:
            key: State key
            value: Value to store
            save: Whether to save immediately (default: True)
        """
        with self._lock:
            self._state[key] = value

        if save:
            self._save()

    def delete(self, key: str, save: bool = True):
        """
        Delete a key from state.

        Args:
            key: State key to delete
            save: Whether to save immediately (default: True)
        """
        with self._lock:
            if key in self._state:
                del self._state[key]

        if save:
            self._save()

    def clear(self, save: bool = True):
        """
        Clear all state.

        Args:
            save: Whether to save immediately (default: True)
        """
        with self._lock:
            self._state.clear()

        if save:
            self._save()

    def save(self):
        """Manually save state to disk."""
        self._save()

    def get_all(self) -> dict[str, Any]:
        """
        Get all state as a dictionary.

        Returns:
            Copy of all state data
        """
        with self._lock:
            return self._state.copy()

    @property
    def config_file(self) -> Path:
        """Get the config file path."""
        return self._config_file

    @property
    def config_dir(self) -> Path:
        """Get the config directory path."""
        return self._config_dir


# Convenience instance
state = StateManager()


def get_state() -> StateManager:
    """
    Get the singleton StateManager instance.

    Returns:
        StateManager instance
    """
    return state
