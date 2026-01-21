"""
Unit tests for standard encoding algorithms (Base64, URL, Hex).

Tests verify that:
1. Base64Encode/Decode works correctly
2. URLEncode/Decode works correctly
3. HexEncode/Decode works correctly
4. Edge cases (empty string, special characters, unicode)
5. Round-trip encoding/decoding
"""

import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestBase64EncodeDecode:
    """Test suite for Base64Encode and Base64Decode transformers."""

    def test_base64_encode_simple_text(self):
        """Base64Encode encodes simple text correctly."""
        from transformers.encoding import Base64Encode

        transformer = Base64Encode()
        result = transformer.encode("Hello, World!")

        assert result == "SGVsbG8sIFdvcmxkIQ=="

    def test_base64_encode_empty_string(self):
        """Base64Encode handles empty string."""
        from transformers.encoding import Base64Encode

        transformer = Base64Encode()
        result = transformer.encode("")

        assert result == ""

    def test_base64_encode_unicode(self):
        """Base64Encode handles unicode characters."""
        from transformers.encoding import Base64Encode

        transformer = Base64Encode()
        result = transformer.encode("안녕하세요")

        # Base64 of UTF-8 encoded Korean text (without padding)
        assert result == "7JWI64WV7ZWY7IS47JqU"

    def test_base64_decode_simple_text(self):
        """Base64Decode decodes correctly."""
        from transformers.encoding import Base64Decode

        transformer = Base64Decode()
        result = transformer.decode("SGVsbG8sIFdvcmxkIQ==")

        assert result == "Hello, World!"

    def test_base64_decode_empty_string(self):
        """Base64Decode handles empty string."""
        from transformers.encoding import Base64Decode

        transformer = Base64Decode()
        result = transformer.decode("")

        assert result == ""

    def test_base64_roundtrip(self):
        """Base64Encode and Base64Decode are inverse operations."""
        from transformers.encoding import Base64Encode, Base64Decode

        encoder = Base64Encode()
        decoder = Base64Decode()

        original = "Test with special chars: !@#$%^&*()[]{}"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_base64_decode_invalid_raises_error(self):
        """Base64Decode raises error for invalid input."""
        from transformers.encoding import Base64Decode

        transformer = Base64Decode()

        with pytest.raises(Exception):
            transformer.decode("Not valid base64!")

    def test_base64_encode_attributes(self):
        """Base64Encode has correct attributes."""
        from transformers.encoding import Base64Encode

        transformer = Base64Encode()

        assert transformer.name == "base64_encode"
        assert transformer.category == "encoding"
        assert transformer.is_bidirectional is True

    def test_base64_decode_attributes(self):
        """Base64Decode has correct attributes."""
        from transformers.encoding import Base64Decode

        transformer = Base64Decode()

        assert transformer.name == "base64_decode"
        assert transformer.category == "encoding"
        assert transformer.is_bidirectional is True


class TestURLEncodeDecode:
    """Test suite for URLEncode and URLDecode transformers."""

    def test_url_encode_simple_text(self):
        """URLEncode encodes special characters."""
        from transformers.encoding import URLEncode

        transformer = URLEncode()
        result = transformer.encode("Hello World!")

        # urllib.parse.quote uses %20 for spaces
        assert result == "Hello%20World%21"

    def test_url_encode_reserved_characters(self):
        """URLEncode encodes URL reserved characters."""
        from transformers.encoding import URLEncode

        transformer = URLEncode()
        result = transformer.encode("a+b c:d/e?f")

        # Spaces become +, special chars become %XX
        assert "a%2Bb" in result
        assert "c%3Ad" in result

    def test_url_encode_empty_string(self):
        """URLEncode handles empty string."""
        from transformers.encoding import URLEncode

        transformer = URLEncode()
        result = transformer.encode("")

        assert result == ""

    def test_url_decode_simple_text(self):
        """URLDecode decodes correctly."""
        from transformers.encoding import URLDecode

        transformer = URLDecode()
        result = transformer.decode("Hello%20World%21")

        assert result == "Hello World!"

    def test_url_decode_empty_string(self):
        """URLDecode handles empty string."""
        from transformers.encoding import URLDecode

        transformer = URLDecode()
        result = transformer.decode("")

        assert result == ""

    def test_url_roundtrip(self):
        """URLEncode and URLDecode are inverse operations."""
        from transformers.encoding import URLEncode, URLDecode

        encoder = URLEncode()
        decoder = URLDecode()

        original = "test@example.com?query=value&key=data"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_url_encode_attributes(self):
        """URLEncode has correct attributes."""
        from transformers.encoding import URLEncode

        transformer = URLEncode()

        assert transformer.name == "url_encode"
        assert transformer.category == "encoding"
        assert transformer.is_bidirectional is True

    def test_url_decode_attributes(self):
        """URLDecode has correct attributes."""
        from transformers.encoding import URLDecode

        transformer = URLDecode()

        assert transformer.name == "url_decode"
        assert transformer.category == "encoding"
        assert transformer.is_bidirectional is True


class TestHexEncodeDecode:
    """Test suite for HexEncode and HexDecode transformers."""

    def test_hex_encode_simple_text(self):
        """HexEncode encodes to hexadecimal."""
        from transformers.encoding import HexEncode

        transformer = HexEncode()
        result = transformer.encode("Hello")

        # "Hello" in UTF-8 = 48 65 6C 6C 6F
        assert result == "48656c6c6f"

    def test_hex_encode_empty_string(self):
        """HexEncode handles empty string."""
        from transformers.encoding import HexEncode

        transformer = HexEncode()
        result = transformer.encode("")

        assert result == ""

    def test_hex_encode_unicode(self):
        """HexEncode handles unicode characters."""
        from transformers.encoding import HexEncode

        transformer = HexEncode()
        result = transformer.encode("안")

        # Korean character encoded in UTF-8 then hex
        # 안 in UTF-8 = EC 95 88
        assert result == "ec9588"

    def test_hex_decode_simple_text(self):
        """HexDecode decodes hexadecimal to string."""
        from transformers.encoding import HexDecode

        transformer = HexDecode()
        result = transformer.decode("48656c6c6f")

        assert result == "Hello"

    def test_hex_decode_empty_string(self):
        """HexDecode handles empty string."""
        from transformers.encoding import HexDecode

        transformer = HexDecode()
        result = transformer.decode("")

        assert result == ""

    def test_hex_roundtrip(self):
        """HexEncode and HexDecode are inverse operations."""
        from transformers.encoding import HexEncode, HexDecode

        encoder = HexEncode()
        decoder = HexDecode()

        original = "Test with unicode: 😊"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_hex_decode_invalid_raises_error(self):
        """HexDecode raises error for invalid input."""
        from transformers.encoding import HexDecode

        transformer = HexDecode()

        with pytest.raises(Exception):
            transformer.decode("Not valid hex!")

    def test_hex_decode_odd_length_raises_error(self):
        """HexDecode raises error for odd-length input."""
        from transformers.encoding import HexDecode

        transformer = HexDecode()

        with pytest.raises(Exception):
            transformer.decode("abc")

    def test_hex_encode_attributes(self):
        """HexEncode has correct attributes."""
        from transformers.encoding import HexEncode

        transformer = HexEncode()

        assert transformer.name == "hex_encode"
        assert transformer.category == "encoding"
        assert transformer.is_bidirectional is True

    def test_hex_decode_attributes(self):
        """HexDecode has correct attributes."""
        from transformers.encoding import HexDecode

        transformer = HexDecode()

        assert transformer.name == "hex_decode"
        assert transformer.category == "encoding"
        assert transformer.is_bidirectional is True
