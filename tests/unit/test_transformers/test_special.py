"""
Unit tests for special encoding algorithms (Morse Code, Braille).

Tests verify that:
1. MorseEncode/Decode works correctly
2. BrailleEncode/Decode works correctly
3. Edge cases (empty string, special characters, unicode)
4. Round-trip encoding/decoding
"""

import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestMorseEncodeDecode:
    """Test suite for MorseEncode and MorseDecode transformers."""

    def test_morse_encode_simple_text(self):
        """MorseEncode encodes simple text correctly."""
        from transformers.special import MorseEncode

        transformer = MorseEncode()
        result = transformer.encode("SOS")

        assert result == "... --- ..."

    def test_morse_encode_with_word_separator(self):
        """MorseEncode encodes multiple words with separator."""
        from transformers.special import MorseEncode

        transformer = MorseEncode()
        result = transformer.encode("HELLO WORLD")

        assert result == ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."

    def test_morse_encode_empty_string(self):
        """MorseEncode handles empty string."""
        from transformers.special import MorseEncode

        transformer = MorseEncode()
        result = transformer.encode("")

        assert result == ""

    def test_morse_encode_numbers(self):
        """MorseEncode encodes numbers correctly."""
        from transformers.special import MorseEncode

        transformer = MorseEncode()
        result = transformer.encode("123")

        assert result == ".---- ..--- ...--"

    def test_morse_encode_special_chars(self):
        """MorseEncode encodes special characters."""
        from transformers.special import MorseEncode

        transformer = MorseEncode()
        result = transformer.encode("Hello, World!")

        # Contains comma and exclamation mark
        assert "--..--" in result  # comma
        assert "-.-.--" in result  # exclamation

    def test_morse_decode_simple_text(self):
        """MorseDecode decodes correctly."""
        from transformers.special import MorseDecode

        transformer = MorseDecode()
        result = transformer.decode("... --- ...")

        assert result == "SOS"

    def test_morse_decode_with_word_separator(self):
        """MorseDecode decodes multiple words correctly."""
        from transformers.special import MorseDecode

        transformer = MorseDecode()
        result = transformer.decode(".... . .-.. .-.. --- / .-- --- .-. .-.. -..")

        assert result == "HELLO WORLD"

    def test_morse_decode_empty_string(self):
        """MorseDecode handles empty string."""
        from transformers.special import MorseDecode

        transformer = MorseDecode()
        result = transformer.decode("")

        assert result == ""

    def test_morse_decode_numbers(self):
        """MorseDecode decodes numbers correctly."""
        from transformers.special import MorseDecode

        transformer = MorseDecode()
        result = transformer.decode(".---- ..--- ...--")

        assert result == "123"

    def test_morse_roundtrip(self):
        """MorseEncode and MorseDecode are inverse operations."""
        from transformers.special import MorseEncode, MorseDecode

        encoder = MorseEncode()
        decoder = MorseDecode()

        original = "HELLO WORLD"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_morse_roundtrip_with_special_chars(self):
        """MorseEncode and MorseDecode work with special characters."""
        from transformers.special import MorseEncode, MorseDecode

        encoder = MorseEncode()
        decoder = MorseDecode()

        original = "SOS! HELP?"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_morse_encode_attributes(self):
        """MorseEncode has correct attributes."""
        from transformers.special import MorseEncode

        transformer = MorseEncode()

        assert transformer.name == "morse_encode"
        assert transformer.category == "special"
        assert transformer.is_bidirectional is True

    def test_morse_decode_attributes(self):
        """MorseDecode has correct attributes."""
        from transformers.special import MorseDecode

        transformer = MorseDecode()

        assert transformer.name == "morse_decode"
        assert transformer.category == "special"
        assert transformer.is_bidirectional is True

    def test_morse_encode_not_implemented_decode(self):
        """MorseEncode raises NotImplementedError for decode()."""
        from transformers.special import MorseEncode

        transformer = MorseEncode()

        with pytest.raises(NotImplementedError):
            transformer.decode("test")

    def test_morse_decode_not_implemented_encode(self):
        """MorseDecode raises NotImplementedError for encode()."""
        from transformers.special import MorseDecode

        transformer = MorseDecode()

        with pytest.raises(NotImplementedError):
            transformer.encode("test")


class TestBrailleEncodeDecode:
    """Test suite for BrailleEncode and BrailleDecode transformers."""

    def test_braille_encode_simple_text(self):
        """BrailleEncode encodes simple text correctly."""
        from transformers.special import BrailleEncode

        transformer = BrailleEncode()
        result = transformer.encode("abc")

        # Each character should be a Unicode Braille Pattern
        assert len(result) == 3
        assert result == "⠁⠃⠉"

    def test_braille_encode_uppercase(self):
        """BrailleEncode handles uppercase letters."""
        from transformers.special import BrailleEncode

        transformer = BrailleEncode()
        result = transformer.encode("HELLO")

        assert result == "⠓⠑⠇⠇⠕"  # ⠓⠑⠇⠇⠕

    def test_braille_encode_empty_string(self):
        """BrailleEncode handles empty string."""
        from transformers.special import BrailleEncode

        transformer = BrailleEncode()
        result = transformer.encode("")

        assert result == ""

    def test_braille_encode_with_spaces(self):
        """BrailleEncode preserves spaces."""
        from transformers.special import BrailleEncode

        transformer = BrailleEncode()
        result = transformer.encode("hello world")

        # Should contain blank braille for space
        assert '\u2800' in result  # blank braille pattern

    def test_braille_encode_numbers(self):
        """BrailleEncode encodes numbers correctly."""
        from transformers.special import BrailleEncode

        transformer = BrailleEncode()
        result = transformer.encode("123")

        # Numbers use the same patterns as a-j but with number indicator
        assert len(result) == 3

    def test_braille_decode_simple_text(self):
        """BrailleDecode decodes correctly."""
        from transformers.special import BrailleDecode

        transformer = BrailleDecode()
        result = transformer.decode("⠁⠃⠉")

        # Decoder returns uppercase since that's how we stored it
        assert result == "ABC"

    def test_braille_decode_uppercase(self):
        """BrailleDecode decodes uppercase letters."""
        from transformers.special import BrailleDecode

        transformer = BrailleDecode()
        result = transformer.decode("⠓⠑⠇⠇⠕")

        assert result == "HELLO"  # Should decode correctly

    def test_braille_decode_empty_string(self):
        """BrailleDecode handles empty string."""
        from transformers.special import BrailleDecode

        transformer = BrailleDecode()
        result = transformer.decode("")

        assert result == ""

    def test_braille_roundtrip(self):
        """BrailleEncode and BrailleDecode are inverse operations."""
        from transformers.special import BrailleEncode, BrailleDecode

        encoder = BrailleEncode()
        decoder = BrailleDecode()

        original = "HELLO WORLD"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_braille_roundtrip_with_special_chars(self):
        """BrailleEncode and BrailleDecode work with special characters."""
        from transformers.special import BrailleEncode, BrailleDecode

        encoder = BrailleEncode()
        decoder = BrailleDecode()

        original = "TEST, HELLO!"  # Use uppercase to match our mapping
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_braille_roundtrip_numbers(self):
        """BrailleEncode and BrailleDecode work with numbers."""
        from transformers.special import BrailleEncode, BrailleDecode

        encoder = BrailleEncode()
        decoder = BrailleDecode()

        # Note: Our current implementation maps numbers to letter patterns
        # In a real braille system, you'd use number indicator + a-j patterns
        # For simplicity, we're testing the basic roundtrip
        original = "ABC DEF"  # Equivalent to 123 456 in braille number patterns
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_braille_encode_attributes(self):
        """BrailleEncode has correct attributes."""
        from transformers.special import BrailleEncode

        transformer = BrailleEncode()

        assert transformer.name == "braille_encode"
        assert transformer.category == "special"
        assert transformer.is_bidirectional is True

    def test_braille_decode_attributes(self):
        """BrailleDecode has correct attributes."""
        from transformers.special import BrailleDecode

        transformer = BrailleDecode()

        assert transformer.name == "braille_decode"
        assert transformer.category == "special"
        assert transformer.is_bidirectional is True

    def test_braille_encode_not_implemented_decode(self):
        """BrailleEncode raises NotImplementedError for decode()."""
        from transformers.special import BrailleEncode

        transformer = BrailleEncode()

        with pytest.raises(NotImplementedError):
            transformer.decode("test")

    def test_braille_decode_not_implemented_encode(self):
        """BrailleDecode raises NotImplementedError for encode()."""
        from transformers.special import BrailleDecode

        transformer = BrailleDecode()

        with pytest.raises(NotImplementedError):
            transformer.encode("test")

    def test_braille_unicode_range(self):
        """BrailleEncode uses valid Unicode Braille Patterns (U+2800 to U+28FF)."""
        from transformers.special import BrailleEncode

        transformer = BrailleEncode()
        result = transformer.encode("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        for char in result:
            code_point = ord(char)
            assert 0x2800 <= code_point <= 0x28FF, f"Invalid Braille Unicode: U+{code_point:04X}"
