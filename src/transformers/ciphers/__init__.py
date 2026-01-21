"""
Classic cipher algorithms.

Includes ROT13, Caesar, Vigenère, and Atbash ciphers.
"""

from transformers.base import TransformerInterface


class ROT13Encode(TransformerInterface):
    """Encode text using ROT13 cipher (13-character shift)."""

    name = "rot13"
    category = "ciphers"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """
        Encode text using ROT13.

        Args:
            text: Input string

        Returns:
            ROT13 encoded string (each letter shifted by 13 positions)
        """
        result = []
        for char in text:
            if 'a' <= char <= 'z':
                # Shift lowercase letters by 13
                result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                # Shift uppercase letters by 13
                result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
            else:
                # Leave non-alphabetic characters unchanged
                result.append(char)
        return ''.join(result)

    def decode(self, text: str) -> str:
        """
        Decode ROT13 (same as encoding since ROT13 is self-inverse).

        Args:
            text: ROT13 encoded string

        Returns:
            Decoded original string
        """
        return self.encode(text)


class ROT13Decode(TransformerInterface):
    """Decode ROT13 encoded text."""

    name = "rot13_decode"
    category = "ciphers"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use ROT13Encode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode ROT13 string.

        Args:
            text: ROT13 encoded string

        Returns:
            Decoded original string
        """
        encoder = ROT13Encode()
        return encoder.encode(text)


class CaesarEncode(TransformerInterface):
    """Encode text using Caesar cipher (shift=3)."""

    name = "caesar"
    category = "ciphers"
    is_bidirectional = True

    def __init__(self, shift: int = 3):
        """
        Initialize Caesar cipher with specified shift.

        Args:
            shift: Number of positions to shift (default: 3)
        """
        self.shift = shift

    def encode(self, text: str) -> str:
        """
        Encode text using Caesar cipher.

        Args:
            text: Input string

        Returns:
            Caesar cipher encoded string (each letter shifted by 3 positions)
        """
        result = []
        for char in text:
            if 'a' <= char <= 'z':
                # Shift lowercase letters
                result.append(chr((ord(char) - ord('a') + self.shift) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                # Shift uppercase letters
                result.append(chr((ord(char) - ord('A') + self.shift) % 26 + ord('A')))
            else:
                # Leave non-alphabetic characters unchanged
                result.append(char)
        return ''.join(result)

    def decode(self, text: str) -> str:
        """
        Decode Caesar cipher (not applicable for encoder).

        Args:
            text: Caesar encoded string

        Returns:
            Decoded string
        """
        raise NotImplementedError("Use CaesarDecode for decoding")


class CaesarDecode(TransformerInterface):
    """Decode Caesar cipher encoded text."""

    name = "caesar_decode"
    category = "ciphers"
    is_bidirectional = True

    def __init__(self, shift: int = 3):
        """
        Initialize Caesar cipher decoder with specified shift.

        Args:
            shift: Number of positions to shift back (default: 3)
        """
        self.shift = shift

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use CaesarEncode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode Caesar cipher string.

        Args:
            text: Caesar cipher encoded string

        Returns:
            Decoded original string
        """
        result = []
        for char in text:
            if 'a' <= char <= 'z':
                # Shift lowercase letters back
                result.append(chr((ord(char) - ord('a') - self.shift) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                # Shift uppercase letters back
                result.append(chr((ord(char) - ord('A') - self.shift) % 26 + ord('A')))
            else:
                # Leave non-alphabetic characters unchanged
                result.append(char)
        return ''.join(result)


class VigenereEncode(TransformerInterface):
    """Encode text using Vigenère cipher."""

    name = "vigenere"
    category = "ciphers"
    is_bidirectional = True

    def __init__(self, key: str = "KEY"):
        """
        Initialize Vigenère cipher with specified key.

        Args:
            key: Encryption key (default: "KEY")
        """
        if not key or not key.isalpha():
            raise ValueError("Key must be a non-empty alphabetic string")
        self.key = key.upper()

    def encode(self, text: str) -> str:
        """
        Encode text using Vigenère cipher.

        Args:
            text: Input string

        Returns:
            Vigenère cipher encoded string
        """
        result = []
        key_index = 0

        for char in text:
            if 'a' <= char <= 'z':
                # Shift lowercase letters
                key_char = self.key[key_index % len(self.key)]
                shift = ord(key_char) - ord('A')
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
                key_index += 1
            elif 'A' <= char <= 'Z':
                # Shift uppercase letters
                key_char = self.key[key_index % len(self.key)]
                shift = ord(key_char) - ord('A')
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
                key_index += 1
            else:
                # Leave non-alphabetic characters unchanged
                result.append(char)

        return ''.join(result)

    def decode(self, text: str) -> str:
        """
        Decode Vigenère cipher (not applicable for encoder).

        Args:
            text: Vigenère encoded string

        Returns:
            Decoded string
        """
        raise NotImplementedError("Use VigenereDecode for decoding")


class VigenereDecode(TransformerInterface):
    """Decode Vigenère cipher encoded text."""

    name = "vigenere_decode"
    category = "ciphers"
    is_bidirectional = True

    def __init__(self, key: str = "KEY"):
        """
        Initialize Vigenère decoder with specified key.

        Args:
            key: Decryption key (default: "KEY")
        """
        if not key or not key.isalpha():
            raise ValueError("Key must be a non-empty alphabetic string")
        self.key = key.upper()

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use VigenereEncode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode Vigenère cipher string.

        Args:
            text: Vigenère cipher encoded string

        Returns:
            Decoded original string
        """
        result = []
        key_index = 0

        for char in text:
            if 'a' <= char <= 'z':
                # Shift lowercase letters back
                key_char = self.key[key_index % len(self.key)]
                shift = ord(key_char) - ord('A')
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
                key_index += 1
            elif 'A' <= char <= 'Z':
                # Shift uppercase letters back
                key_char = self.key[key_index % len(self.key)]
                shift = ord(key_char) - ord('A')
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
                key_index += 1
            else:
                # Leave non-alphabetic characters unchanged
                result.append(char)

        return ''.join(result)


class AtbashEncode(TransformerInterface):
    """Encode text using Atbash cipher (A<->Z, a<->z)."""

    name = "atbash"
    category = "ciphers"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """
        Encode text using Atbash cipher.

        Args:
            text: Input string

        Returns:
            Atbash cipher encoded string (alphabet reversed)
        """
        result = []
        for char in text:
            if 'a' <= char <= 'z':
                # Reverse lowercase letters (a->z, b->y, ..., z->a)
                result.append(chr(ord('z') - (ord(char) - ord('a'))))
            elif 'A' <= char <= 'Z':
                # Reverse uppercase letters (A->Z, B->Y, ..., Z->A)
                result.append(chr(ord('Z') - (ord(char) - ord('A'))))
            else:
                # Leave non-alphabetic characters unchanged
                result.append(char)
        return ''.join(result)

    def decode(self, text: str) -> str:
        """
        Decode Atbash cipher (same as encoding since Atbash is self-inverse).

        Args:
            text: Atbash encoded string

        Returns:
            Decoded original string
        """
        return self.encode(text)


class AtbashDecode(TransformerInterface):
    """Decode Atbash cipher encoded text."""

    name = "atbash_decode"
    category = "ciphers"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use AtbashEncode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode Atbash cipher string.

        Args:
            text: Atbash encoded string

        Returns:
            Decoded original string
        """
        encoder = AtbashEncode()
        return encoder.encode(text)
