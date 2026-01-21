"""
AlgorithmRegistry singleton for managing transformers.

Provides centralized registration and lookup of all transformation algorithms.
Used by sidebar to populate categories and search functionality.
"""

from typing import List, Optional


class AlgorithmRegistry:
    """
    Singleton registry for all transformation algorithms.

    Usage:
        registry = AlgorithmRegistry()
        registry.register(Base64Encode())
        registry.register(Base64Decode())

        # Search by keyword in name or category
        results = registry.search("base64")

        # Get all transformers
        all_transformers = registry.get_all()

        # Get transformers by category
        encoding_transformers = registry.get_by_category("encoding")
    """

    _instance: Optional['AlgorithmRegistry'] = None
    _transformers: dict = {}

    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._transformers = {}
        return cls._instance

    def register(self, transformer) -> None:
        """
        Register a transformer instance.

        Args:
            transformer: Instance of TransformerInterface subclass

        Raises:
            ValueError: If transformer name is already registered
        """
        name = transformer.name

        if name in self._transformers:
            raise ValueError(f"Transformer '{name}' is already registered")

        self._transformers[name] = transformer

    def search(self, keyword: str) -> List:
        """
        Search transformers by name or category keyword.

        Args:
            keyword: Search term (case-insensitive)

        Returns:
            List of matching transformer instances
        """
        if not keyword:
            return list(self._transformers.values())

        keyword_lower = keyword.lower()
        results = []

        for transformer in self._transformers.values():
            if (keyword_lower in transformer.name.lower() or
                keyword_lower in transformer.category.lower()):
                results.append(transformer)

        return results

    def get_all(self) -> List:
        """
        Get all registered transformers.

        Returns:
            List of all transformer instances
        """
        return list(self._transformers.values())

    def get_by_category(self, category: str) -> List:
        """
        Get all transformers in a specific category.

        Args:
            category: Category name (encoding, hashing, text_processing, special, ciphers)

        Returns:
            List of transformer instances in the category
        """
        return [
            t for t in self._transformers.values()
            if t.category.lower() == category.lower()
        ]
