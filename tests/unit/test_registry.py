"""
Unit tests for AlgorithmRegistry singleton.

Tests verify that:
1. AlgorithmRegistry is a singleton (only one instance exists)
2. Transformers can be registered by category
3. search() finds transformers by name/category keyword
4. get_all() returns all registered transformers
5. get_by_category() returns transformers for specific category
6. Cannot register duplicate transformer names
"""

import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestAlgorithmRegistry:
    """Test suite for AlgorithmRegistry singleton."""

    def setup_method(self):
        """Reset registry before each test."""
        from registry import AlgorithmRegistry
        AlgorithmRegistry._instance = None
        AlgorithmRegistry._transformers = {}

    def test_singleton_pattern(self):
        """AlgorithmRegistry implements singleton pattern."""
        from registry import AlgorithmRegistry

        registry1 = AlgorithmRegistry()
        registry2 = AlgorithmRegistry()

        assert registry1 is registry2
        assert id(registry1) == id(registry2)

    def test_register_transformer(self):
        """Can register a transformer instance."""
        from registry import AlgorithmRegistry
        from transformers.base import TransformerInterface

        class MockTransformer(TransformerInterface):
            name = "mock_transformer"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        registry = AlgorithmRegistry()
        registry.register(MockTransformer())

        assert "mock_transformer" in registry._transformers
        assert registry._transformers["mock_transformer"].name == "mock_transformer"

    def test_register_multiple_transformers(self):
        """Can register multiple transformers."""
        from registry import AlgorithmRegistry
        from transformers.base import TransformerInterface

        class TransformerA(TransformerInterface):
            name = "transformer_a"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text + "_a"

            def decode(self, text: str) -> str:
                return text.replace("_a", "")

        class TransformerB(TransformerInterface):
            name = "transformer_b"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text + "_b"

            def decode(self, text: str) -> str:
                return text.replace("_b", "")

        registry = AlgorithmRegistry()
        registry.register(TransformerA())
        registry.register(TransformerB())

        assert len(registry._transformers) == 2
        assert "transformer_a" in registry._transformers
        assert "transformer_b" in registry._transformers

    def test_register_duplicate_name_raises_error(self):
        """Cannot register two transformers with the same name."""
        from registry import AlgorithmRegistry
        from transformers.base import TransformerInterface

        class Transformer1(TransformerInterface):
            name = "duplicate"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        class Transformer2(TransformerInterface):
            name = "duplicate"  # Same name
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        registry = AlgorithmRegistry()
        registry.register(Transformer1())

        with pytest.raises(ValueError, match="already registered"):
            registry.register(Transformer2())

    def test_search_by_name(self):
        """search() finds transformers by name keyword."""
        from registry import AlgorithmRegistry
        from transformers.base import TransformerInterface

        class Base64Encode(TransformerInterface):
            name = "base64_encode"
            category = "encoding"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        class Base64Decode(TransformerInterface):
            name = "base64_decode"
            category = "encoding"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        registry = AlgorithmRegistry()
        registry.register(Base64Encode())
        registry.register(Base64Decode())

        results = registry.search("base64")
        assert len(results) == 2

        results = registry.search("encode")
        assert len(results) == 1
        assert results[0].name == "base64_encode"

    def test_search_by_category(self):
        """search() finds transformers by category keyword."""
        from registry import AlgorithmRegistry
        from transformers.base import TransformerInterface

        class Transformer1(TransformerInterface):
            name = "transformer1"
            category = "encoding"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        class Transformer2(TransformerInterface):
            name = "transformer2"
            category = "hashing"
            is_bidirectional = False

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                raise NotImplementedError()

        registry = AlgorithmRegistry()
        registry.register(Transformer1())
        registry.register(Transformer2())

        results = registry.search("encoding")
        assert len(results) == 1
        assert results[0].category == "encoding"

    def test_search_case_insensitive(self):
        """search() is case-insensitive."""
        from registry import AlgorithmRegistry
        from transformers.base import TransformerInterface

        class Transformer(TransformerInterface):
            name = "Base64_Encode"
            category = "Encoding"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        registry = AlgorithmRegistry()
        registry.register(Transformer())

        assert len(registry.search("base64")) == 1
        assert len(registry.search("BASE64")) == 1
        assert len(registry.search("encoding")) == 1
        assert len(registry.search("ENCODING")) == 1

    def test_search_empty_string_returns_all(self):
        """search('') returns all transformers."""
        from registry import AlgorithmRegistry
        from transformers.base import TransformerInterface

        class Transformer(TransformerInterface):
            name = "test"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        registry = AlgorithmRegistry()
        registry.register(Transformer())

        results = registry.search("")
        assert len(results) == 1

    def test_get_all_returns_all_transformers(self):
        """get_all() returns list of all registered transformers."""
        from registry import AlgorithmRegistry
        from transformers.base import TransformerInterface

        class Transformer1(TransformerInterface):
            name = "t1"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        class Transformer2(TransformerInterface):
            name = "t2"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        registry = AlgorithmRegistry()
        registry.register(Transformer1())
        registry.register(Transformer2())

        all_transformers = registry.get_all()
        assert len(all_transformers) == 2
        assert any(t.name == "t1" for t in all_transformers)
        assert any(t.name == "t2" for t in all_transformers)

    def test_get_by_category(self):
        """get_by_category() returns transformers for specific category."""
        from registry import AlgorithmRegistry
        from transformers.base import TransformerInterface

        class EncodingTransformer(TransformerInterface):
            name = "encoding_test"
            category = "encoding"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        class HashingTransformer(TransformerInterface):
            name = "hashing_test"
            category = "hashing"
            is_bidirectional = False

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                raise NotImplementedError()

        registry = AlgorithmRegistry()
        registry.register(EncodingTransformer())
        registry.register(HashingTransformer())

        encoding_transformers = registry.get_by_category("encoding")
        hashing_transformers = registry.get_by_category("hashing")

        assert len(encoding_transformers) == 1
        assert encoding_transformers[0].name == "encoding_test"

        assert len(hashing_transformers) == 1
        assert hashing_transformers[0].name == "hashing_test"

    def test_get_by_nonexistent_category(self):
        """get_by_category() returns empty list for non-existent category."""
        from registry import AlgorithmRegistry

        registry = AlgorithmRegistry()
        results = registry.get_by_category("nonexistent")

        assert results == []
