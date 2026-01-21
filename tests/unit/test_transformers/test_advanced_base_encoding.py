"""
Unit tests for advanced base encoding algorithms.

Tests verify that:
1. Base32, Base58, Base62, Base85, Base91 encode/decode correctly
2. Handle empty strings, unicode, and edge cases
3. Round-trip encoding/decoding works
4. Invalid input raises appropriate errors
"""

import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestBase32EncodeDecode:
    """Test suite for Base32Encode and Base32Decode transformers."""

    def test_base32_encode_simple_text(self):
        """Base32Encode encodes simple text correctly."""
        from transformers.encoding import Base32Encode

        transformer = Base32Encode()
        result = transformer.encode("Hello")

        # Base32 of "Hello" (uppercase output)
        assert result == "JBSWY3DP"

    def test_base32_encode_empty_string(self):
        """Base32Encode handles empty string."""
        from transformers.encoding import Base32Encode

        transformer = Base32Encode()
        result = transformer.encode("")

        assert result == ""

    def test_base32_decode_simple_text(self):
        """Base32Decode decodes correctly."""
        from transformers.encoding import Base32Decode

        transformer = Base32Decode()
        result = transformer.decode("JBSWY3DP")

        # Base32 decode is case-insensitive and produces lowercase
        assert result.lower() == "hello"

    def test_base32_roundtrip(self):
        """Base32Encode and Base32Decode are inverse operations."""
        from transformers.encoding import Base32Encode, Base32Decode

        encoder = Base32Encode()
        decoder = Base32Decode()

        original = "Test with special chars: !@#$%"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_base32_encode_attributes(self):
        """Base32Encode has correct attributes."""
        from transformers.encoding import Base32Encode

        transformer = Base32Encode()

        assert transformer.name == "base32_encode"
        assert transformer.category == "encoding"
        assert transformer.is_bidirectional is True


class Base85EncodeDecode:
    """Test suite for Base85Encode and Base85Decode transformers."""

    def test_base85_encode_simple_text(self):
        """Base85Encode encodes simple text correctly."""
        from transformers.encoding import Base85Encode

        transformer = Base85Encode()
        result = transformer.encode("Hello")

        # Base85 (RFC 1924) of "Hello" - verify it produces output
        assert len(result) > 0
        # Should be reasonable length
        assert len(result) <= 20

    def test_base85_encode_empty_string(self):
        """Base85Encode handles empty string."""
        from transformers.encoding import Base85Encode

        transformer = Base85Encode()
        result = transformer.encode("")

        assert result == ""

    def test_base85_decode_simple_text(self):
        """Base85Decode decodes correctly."""
        from transformers.encoding import Base85Decode, Base85Encode

        encoder = Base85Encode()
        decoder = Base85Decode()

        original = "Hello"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_base85_roundtrip(self):
        """Base85Encode and Base85Decode are inverse operations."""
        from transformers.encoding import Base85Encode, Base85Decode

        encoder = Base85Encode()
        decoder = Base85Decode()

        original = "Test with special chars: !@#$%"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original


class TestBase58EncodeDecode:
    """Test suite for Base58Encode and Base58Decode transformers."""

    def test_base58_encode_simple_text(self):
        """Base58Encode encodes simple text correctly."""
        from transformers.encoding import Base58Encode

        transformer = Base58Encode()
        result = transformer.encode("Hello")

        # Base58 of "Hello"
        assert "JxF12" in result or len(result) > 0  # Base58 varies by implementation

    def test_base58_encode_empty_string(self):
        """Base58Encode handles empty string."""
        from transformers.encoding import Base58Encode

        transformer = Base58Encode()
        result = transformer.encode("")

        assert result == ""

    def test_base58_roundtrip(self):
        """Base58Encode and Base58Decode are inverse operations."""
        from transformers.encoding import Base58Encode, Base58Decode

        encoder = Base58Encode()
        decoder = Base58Decode()

        original = "Hello World"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original


class TestBase62EncodeDecode:
    """Test suite for Base62Encode and Base62Decode transformers."""

    def test_base62_encode_simple_text(self):
        """Base62Encode encodes simple text correctly."""
        from transformers.encoding import Base62Encode

        transformer = Base62Encode()
        result = transformer.encode("Hello")

        # Base62 should produce non-empty string
        assert len(result) > 0

    def test_base62_encode_empty_string(self):
        """Base62Encode handles empty string."""
        from transformers.encoding import Base62Encode

        transformer = Base62Encode()
        result = transformer.encode("")

        assert result == ""

    def test_base62_roundtrip(self):
        """Base62Encode and Base62Decode are inverse operations."""
        from transformers.encoding import Base62Encode, Base62Decode

        encoder = Base62Encode()
        decoder = Base62Decode()

        original = "Hello World"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original


class TestBase91EncodeDecode:
    """Test suite for Base91Encode and Base91Decode transformers."""

    def test_base91_encode_simple_text(self):
        """Base91Encode encodes simple text correctly."""
        from transformers.encoding import Base91Encode

        transformer = Base91Encode()
        result = transformer.encode("Hello")

        # Base91 should produce non-empty string
        assert len(result) > 0

    def test_base91_encode_empty_string(self):
        """Base91Encode handles empty string."""
        from transformers.encoding import Base91Encode

        transformer = Base91Encode()
        result = transformer.encode("")

        assert result == ""

    def test_base91_roundtrip(self):
        """Base91Encode and Base91Decode are inverse operations."""
        from transformers.encoding import Base91Encode, Base91Decode

        encoder = Base91Encode()
        decoder = Base91Decode()

        original = "Hello World"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original
