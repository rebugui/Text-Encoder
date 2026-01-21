"""
TransformerInterface abstract base class.

All transformers must inherit from this interface and implement:
- name: Unique algorithm identifier
- category: One of 'encoding', 'hashing', 'text_processing', 'special', 'ciphers'
- is_bidirectional: Whether decode() is supported
- encode(text: str) -> str: Transform input text
- decode(text: str) -> str: Reverse transformation (if bidirectional)
"""

from abc import ABC, abstractmethod
from typing import Protocol


class TransformerInterface(ABC):
    """
    Abstract base class for all transformation algorithms.

    Attributes:
        name: Unique algorithm identifier (e.g., 'base64_encode', 'sha256')
        category: Algorithm category for sidebar organization
        is_bidirectional: True if decode() is supported, False otherwise

    Example:
        class Base64Encode(TransformerInterface):
            name = "base64_encode"
            category = "encoding"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                import base64
                return base64.b64encode(text.encode()).decode()

            def decode(self, text: str) -> str:
                import base64
                return base64.b64decode(text.encode()).decode()
    """

    # Class attributes (must be overridden by subclasses)
    name: str = None
    category: str = None
    is_bidirectional: bool = True

    @abstractmethod
    def encode(self, text: str) -> str:
        """
        Transform input text using the algorithm.

        Args:
            text: Input string to transform

        Returns:
            Transformed string

        Raises:
            Exception: Algorithm-specific errors during transformation
        """
        raise NotImplementedError(f"{self.__class__.__name__}.encode() not implemented")

    @abstractmethod
    def decode(self, text: str) -> str:
        """
        Reverse transformation (only if is_bidirectional=True).

        Args:
            text: Encoded string to decode

        Returns:
            Decoded original string

        Raises:
            NotImplementedError: If transformer is unidirectional
            Exception: Algorithm-specific errors during transformation
        """
        raise NotImplementedError(f"{self.__class__.__name__}.decode() not implemented")

    def __repr__(self) -> str:
        """String representation of transformer."""
        return f"{self.__class__.__name__}(name='{self.name}', category='{self.category}')"
