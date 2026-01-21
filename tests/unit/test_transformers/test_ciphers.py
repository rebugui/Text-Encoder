"""
Unit tests for classic cipher algorithms.

Tests verify that:
1. ROT13 works correctly (self-inverse)
2. Caesar cipher works correctly with shift=3
3. Vigenère cipher works correctly with key "KEY"
4. Atbash cipher works correctly (self-inverse)
5. Edge cases (empty string, special characters, unicode)
6. Round-trip encoding/decoding
"""

import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestROT13EncodeDecode:
    """Test suite for ROT13 cipher."""

    def test_rot13_encode_simple_text(self):
        """ROT13Encode encodes simple text correctly."""
        from transformers.ciphers import ROT13Encode

        transformer = ROT13Encode()
        result = transformer.encode("Hello")

        # H->U, e->r, l->y, l->y, o->b
        assert result == "Uryyb"

    def test_rot13_encode_full_alphabet(self):
        """ROT13Encode handles full alphabet."""
        from transformers.ciphers import ROT13Encode

        transformer = ROT13Encode()
        result = transformer.encode("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        # Each letter shifted by 13
        assert result == "NOPQRSTUVWXYZABCDEFGHIJKLM"

    def test_rot13_encode_lowercase(self):
        """ROT13Encode handles lowercase letters."""
        from transformers.ciphers import ROT13Encode

        transformer = ROT13Encode()
        result = transformer.encode("abcdefghijklmnopqrstuvwxyz")

        assert result == "nopqrstuvwxyzabcdefghijklm"

    def test_rot13_encode_mixed_case(self):
        """ROT13Encode preserves case."""
        from transformers.ciphers import ROT13Encode

        transformer = ROT13Encode()
        result = transformer.encode("Hello World")

        assert result == "Uryyb Jbeyq"

    def test_rot13_encode_non_alphabetic(self):
        """ROT13Encode leaves non-alphabetic characters unchanged."""
        from transformers.ciphers import ROT13Encode

        transformer = ROT13Encode()
        result = transformer.encode("Hello, World! 123")

        assert result == "Uryyb, Jbeyq! 123"

    def test_rot13_encode_empty_string(self):
        """ROT13Encode handles empty string."""
        from transformers.ciphers import ROT13Encode

        transformer = ROT13Encode()
        result = transformer.encode("")

        assert result == ""

    def test_rot13_self_inverse(self):
        """ROT13 is its own inverse (encode twice = original)."""
        from transformers.ciphers import ROT13Encode

        transformer = ROT13Encode()
        original = "Hello, World!"
        encoded = transformer.encode(original)
        decoded = transformer.encode(encoded)

        assert decoded == original

    def test_rot13_decode_same_as_encode(self):
        """ROT13Decode is the same as ROT13Encode."""
        from transformers.ciphers import ROT13Encode, ROT13Decode

        encoder = ROT13Encode()
        decoder = ROT13Decode()

        original = "Hello, World!"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_rot13_encode_attributes(self):
        """ROT13Encode has correct attributes."""
        from transformers.ciphers import ROT13Encode

        transformer = ROT13Encode()

        assert transformer.name == "rot13"
        assert transformer.category == "ciphers"
        assert transformer.is_bidirectional is True

    def test_rot13_decode_attributes(self):
        """ROT13Decode has correct attributes."""
        from transformers.ciphers import ROT13Decode

        transformer = ROT13Decode()

        assert transformer.name == "rot13_decode"
        assert transformer.category == "ciphers"
        assert transformer.is_bidirectional is True


class TestCaesarEncodeDecode:
    """Test suite for Caesar cipher."""

    def test_caesar_encode_simple_text(self):
        """CaesarEncode encodes simple text correctly (shift=3)."""
        from transformers.ciphers import CaesarEncode

        transformer = CaesarEncode()
        result = transformer.encode("Hello")

        # H->K, e->h, l->o, l->o, o->r
        assert result == "Khoor"

    def test_caesar_encode_full_alphabet(self):
        """CaesarEncode handles full alphabet with wrap-around."""
        from transformers.ciphers import CaesarEncode

        transformer = CaesarEncode()
        result = transformer.encode("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        # Each letter shifted by 3
        assert result == "DEFGHIJKLMNOPQRSTUVWXYZABC"

    def test_caesar_encode_wrap_around(self):
        """CaesarEncode handles wrap-around correctly."""
        from transformers.ciphers import CaesarEncode

        transformer = CaesarEncode()
        result = transformer.encode("XYZ")

        # X->A, Y->B, Z->C
        assert result == "ABC"

    def test_caesar_encode_lowercase(self):
        """CaesarEncode handles lowercase letters."""
        from transformers.ciphers import CaesarEncode

        transformer = CaesarEncode()
        result = transformer.encode("xyz")

        # x->a, y->b, z->c
        assert result == "abc"

    def test_caesar_encode_preserve_case(self):
        """CaesarEncode preserves case."""
        from transformers.ciphers import CaesarEncode

        transformer = CaesarEncode()
        result = transformer.encode("Hello World")

        assert result == "Khoor Zruog"

    def test_caesar_encode_non_alphabetic(self):
        """CaesarEncode leaves non-alphabetic characters unchanged."""
        from transformers.ciphers import CaesarEncode

        transformer = CaesarEncode()
        result = transformer.encode("Hello, World! 123")

        assert result == "Khoor, Zruog! 123"

    def test_caesar_encode_empty_string(self):
        """CaesarEncode handles empty string."""
        from transformers.ciphers import CaesarEncode

        transformer = CaesarEncode()
        result = transformer.encode("")

        assert result == ""

    def test_caesar_roundtrip(self):
        """CaesarEncode and CaesarDecode are inverse operations."""
        from transformers.ciphers import CaesarEncode, CaesarDecode

        encoder = CaesarEncode()
        decoder = CaesarDecode()

        original = "Hello, World!"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_caesar_custom_shift(self):
        """CaesarEncode can use custom shift value."""
        from transformers.ciphers import CaesarEncode

        transformer = CaesarEncode(shift=5)
        result = transformer.encode("Hello")

        # H->M, e->j, l->q, l->q, o->t
        assert result == "Mjqqt"

    def test_caesar_decode_custom_shift(self):
        """CaesarDecode can use custom shift value."""
        from transformers.ciphers import CaesarEncode, CaesarDecode

        encoder = CaesarEncode(shift=10)
        decoder = CaesarDecode(shift=10)

        original = "Hello World"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_caesar_encode_attributes(self):
        """CaesarEncode has correct attributes."""
        from transformers.ciphers import CaesarEncode

        transformer = CaesarEncode()

        assert transformer.name == "caesar"
        assert transformer.category == "ciphers"
        assert transformer.is_bidirectional is True

    def test_caesar_decode_attributes(self):
        """CaesarDecode has correct attributes."""
        from transformers.ciphers import CaesarDecode

        transformer = CaesarDecode()

        assert transformer.name == "caesar_decode"
        assert transformer.category == "ciphers"
        assert transformer.is_bidirectional is True


class TestVigenereEncodeDecode:
    """Test suite for Vigenère cipher."""

    def test_vigenere_encode_simple_text(self):
        """VigenereEncode encodes simple text correctly."""
        from transformers.ciphers import VigenereEncode

        transformer = VigenereEncode(key="KEY")
        result = transformer.encode("Hello")

        # H(7) + K(10) = R(17), e(4) + E(4) = I(8), l(11) + Y(24) = J(9)
        # l(11) + K(10) = V(21), o(14) + E(4) = S(18)
        assert result == "Rijvs"

    def test_vigenere_encode_with_default_key(self):
        """VigenereEncode uses 'KEY' as default key."""
        from transformers.ciphers import VigenereEncode

        transformer = VigenereEncode()  # Default key is "KEY"
        result = transformer.encode("Hello")

        assert result == "Rijvs"

    def test_vigenere_encode_longer_text(self):
        """VigenereEncode encodes longer text correctly."""
        from transformers.ciphers import VigenereEncode

        transformer = VigenereEncode(key="KEY")
        result = transformer.encode("Hello World")

        # H+K=R, e+E=I, l+Y=J, l+K=V, o+E=S, [space], W+K=U, o+E=Y, r+Y=v, l+K=j, d+E=h
        assert result == "Rijvs Uyvjn"

    def test_vigenere_encode_custom_key(self):
        """VigenereEncode can use custom key."""
        from transformers.ciphers import VigenereEncode

        transformer = VigenereEncode(key="ABC")
        result = transformer.encode("Hello")

        # H(7) + A(0) = H, e(4) + B(1) = f, l(11) + C(2) = n
        # l(11) + A(0) = l, o(14) + B(1) = p
        assert result == "Hfnlp"

    def test_vigenere_encode_preserve_case(self):
        """VigenereEncode preserves case."""
        from transformers.ciphers import VigenereEncode

        transformer = VigenereEncode(key="KEY")
        result = transformer.encode("Hello World")

        assert result == "Rijvs Uyvjn"

    def test_vigenere_encode_non_alphabetic(self):
        """VigenereEncode leaves non-alphabetic characters unchanged."""
        from transformers.ciphers import VigenereEncode

        transformer = VigenereEncode(key="KEY")
        result = transformer.encode("Hello, World! 123")

        assert result == "Rijvs, Uyvjn! 123"

    def test_vigenere_encode_empty_string(self):
        """VigenereEncode handles empty string."""
        from transformers.ciphers import VigenereEncode

        transformer = VigenereEncode(key="KEY")
        result = transformer.encode("")

        assert result == ""

    def test_vigenere_roundtrip(self):
        """VigenereEncode and VigenereDecode are inverse operations."""
        from transformers.ciphers import VigenereEncode, VigenereDecode

        encoder = VigenereEncode(key="KEY")
        decoder = VigenereDecode(key="KEY")

        original = "Hello, World!"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_vigenere_roundtrip_custom_key(self):
        """VigenereEncode and VigenereDecode work with custom key."""
        from transformers.ciphers import VigenereEncode, VigenereDecode

        encoder = VigenereEncode(key="SECRET")
        decoder = VigenereDecode(key="SECRET")

        original = "The quick brown fox jumps over the lazy dog"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_vigenere_encode_invalid_key_raises_error(self):
        """VigenereEncode raises error for invalid key."""
        from transformers.ciphers import VigenereEncode

        with pytest.raises(ValueError):
            VigenereEncode(key="")

        with pytest.raises(ValueError):
            VigenereEncode(key="123")

    def test_vigenere_encode_attributes(self):
        """VigenereEncode has correct attributes."""
        from transformers.ciphers import VigenereEncode

        transformer = VigenereEncode(key="KEY")

        assert transformer.name == "vigenere"
        assert transformer.category == "ciphers"
        assert transformer.is_bidirectional is True

    def test_vigenere_decode_attributes(self):
        """VigenereDecode has correct attributes."""
        from transformers.ciphers import VigenereDecode

        transformer = VigenereDecode(key="KEY")

        assert transformer.name == "vigenere_decode"
        assert transformer.category == "ciphers"
        assert transformer.is_bidirectional is True


class TestAtbashEncodeDecode:
    """Test suite for Atbash cipher."""

    def test_atbash_encode_simple_text(self):
        """AtbashEncode encodes simple text correctly."""
        from transformers.ciphers import AtbashEncode

        transformer = AtbashEncode()
        result = transformer.encode("Hello")

        # H<->S, e<->v, l<->o, l<->o, o<->l
        assert result == "Svool"

    def test_atbash_encode_full_alphabet(self):
        """AtbashEncode reverses the alphabet."""
        from transformers.ciphers import AtbashEncode

        transformer = AtbashEncode()
        result = transformer.encode("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        # Alphabet reversed
        assert result == "ZYXWVUTSRQPONMLKJIHGFEDCBA"

    def test_atbash_encode_lowercase(self):
        """AtbashEncode handles lowercase letters."""
        from transformers.ciphers import AtbashEncode

        transformer = AtbashEncode()
        result = transformer.encode("abcdefghijklmnopqrstuvwxyz")

        assert result == "zyxwvutsrqponmlkjihgfedcba"

    def test_atbash_encode_mixed_case(self):
        """AtbashEncode preserves case."""
        from transformers.ciphers import AtbashEncode

        transformer = AtbashEncode()
        result = transformer.encode("Hello World")

        assert result == "Svool Dliow"

    def test_atbash_encode_non_alphabetic(self):
        """AtbashEncode leaves non-alphabetic characters unchanged."""
        from transformers.ciphers import AtbashEncode

        transformer = AtbashEncode()
        result = transformer.encode("Hello, World! 123")

        assert result == "Svool, Dliow! 123"

    def test_atbash_encode_empty_string(self):
        """AtbashEncode handles empty string."""
        from transformers.ciphers import AtbashEncode

        transformer = AtbashEncode()
        result = transformer.encode("")

        assert result == ""

    def test_atbash_self_inverse(self):
        """Atbash is its own inverse (encode twice = original)."""
        from transformers.ciphers import AtbashEncode

        transformer = AtbashEncode()
        original = "Hello, World!"
        encoded = transformer.encode(original)
        decoded = transformer.encode(encoded)

        assert decoded == original

    def test_atbash_decode_same_as_encode(self):
        """AtbashDecode is the same as AtbashEncode."""
        from transformers.ciphers import AtbashEncode, AtbashDecode

        encoder = AtbashEncode()
        decoder = AtbashDecode()

        original = "Hello, World!"
        encoded = encoder.encode(original)
        decoded = decoder.decode(encoded)

        assert decoded == original

    def test_atbash_symmetric_pairs(self):
        """AtbashEncode maps A<->Z, B<->Y, etc."""
        from transformers.ciphers import AtbashEncode

        transformer = AtbashEncode()

        assert transformer.encode("AZ") == "ZA"
        assert transformer.encode("BY") == "YB"
        assert transformer.encode("MN") == "NM"

    def test_atbash_encode_attributes(self):
        """AtbashEncode has correct attributes."""
        from transformers.ciphers import AtbashEncode

        transformer = AtbashEncode()

        assert transformer.name == "atbash"
        assert transformer.category == "ciphers"
        assert transformer.is_bidirectional is True

    def test_atbash_decode_attributes(self):
        """AtbashDecode has correct attributes."""
        from transformers.ciphers import AtbashDecode

        transformer = AtbashDecode()

        assert transformer.name == "atbash_decode"
        assert transformer.category == "ciphers"
        assert transformer.is_bidirectional is True
