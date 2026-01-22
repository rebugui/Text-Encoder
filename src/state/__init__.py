"""
State package for application persistence.

This package provides cross-platform state management with automatic
platform-specific storage locations.
"""

from state.manager import StateManager, get_state, state

__all__ = ['StateManager', 'get_state', 'state']
