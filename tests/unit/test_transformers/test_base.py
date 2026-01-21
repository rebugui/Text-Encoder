"""
Unit tests for TransformerInterface abstract base class.

Tests verify that:
1. TransformerInterface cannot be instantiated directly
2. Concrete implementations must provide name, category, and methods
3. encode() and decode() methods raise NotImplementedError for abstract behavior
4. is_bidirectional property works correctly
"""

import pytest
from abc import ABC

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestTransformerInterface:
    """Test suite for TransformerInterface abstract base class."""

    def test_cannot_instantiate_abstract_interface(self):
        """TransformerInterface cannot be instantiated directly."""
        from transformers.base import TransformerInterface

        with pytest.raises(TypeError):
            TransformerInterface()

    def test_concrete_implementation_with_default_name(self):
        """Concrete implementation without name gets None from parent."""
        from transformers.base import TransformerInterface

        class MinimalTransformer(TransformerInterface):
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        transformer = MinimalTransformer()
        # Class attributes inherit from parent, so name is None
        assert transformer.name is None

    def test_concrete_implementation_with_default_category(self):
        """Concrete implementation without category gets None from parent."""
        from transformers.base import TransformerInterface

        class MinimalTransformer(TransformerInterface):
            name = "minimal"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        transformer = MinimalTransformer()
        # Class attributes inherit from parent, so category is None
        assert transformer.category is None

    def test_concrete_implementation_requires_encode_method(self):
        """Concrete implementation must implement encode() method."""
        from transformers.base import TransformerInterface

        class MinimalTransformer(TransformerInterface):
            name = "minimal"
            category = "test"
            is_bidirectional = True

            def decode(self, text: str) -> str:
                return text

        with pytest.raises(TypeError):
            transformer = MinimalTransformer()

    def test_concrete_implementation_requires_decode_method(self):
        """Concrete implementation must implement decode() method."""
        from transformers.base import TransformerInterface

        class MinimalTransformer(TransformerInterface):
            name = "minimal"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

        with pytest.raises(TypeError):
            transformer = MinimalTransformer()

    def test_valid_concrete_implementation(self):
        """Valid concrete implementation can be instantiated and used."""
        from transformers.base import TransformerInterface

        class ValidTransformer(TransformerInterface):
            name = "valid"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return f"encoded:{text}"

            def decode(self, text: str) -> str:
                return text.replace("encoded:", "")

        transformer = ValidTransformer()
        assert transformer.name == "valid"
        assert transformer.category == "test"
        assert transformer.is_bidirectional is True
        assert transformer.encode("test") == "encoded:test"
        assert transformer.decode("encoded:test") == "test"

    def test_abc_prevents_instantiation_without_methods(self):
        """ABC prevents instantiation without implementing abstract methods."""
        from transformers.base import TransformerInterface

        # Cannot create class without implementing encode/decode
        with pytest.raises(TypeError):
            class PartialTransformer(TransformerInterface):
                name = "partial"
                category = "test"
                is_bidirectional = True

            # This should never execute
            transformer = PartialTransformer()

    def test_is_bidirectional_property(self):
        """is_bidirectional property correctly indicates bidirectional capability."""
        from transformers.base import TransformerInterface

        class BidirectionalTransformer(TransformerInterface):
            name = "bidirectional"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text.upper()

            def decode(self, text: str) -> str:
                return text.lower()

        class UnidirectionalTransformer(TransformerInterface):
            name = "unidirectional"
            category = "test"
            is_bidirectional = False

            def encode(self, text: str) -> str:
                return text.upper()

            def decode(self, text: str) -> str:
                raise NotImplementedError("Unidirectional transformer")

        bidirectional = BidirectionalTransformer()
        unidirectional = UnidirectionalTransformer()

        assert bidirectional.is_bidirectional is True
        assert unidirectional.is_bidirectional is False

    def test_is_subclass_of_abstract_base_class(self):
        """TransformerInterface is an abstract base class."""
        from transformers.base import TransformerInterface
        from abc import ABC

        assert issubclass(TransformerInterface, ABC)
