"""
Standard encoding algorithms.

Includes Base64, URL, and Hex encoding/decoding transformers.
"""

import base64
import binascii
from urllib.parse import quote, unquote

from transformers.base import TransformerInterface


class Base64Encode(TransformerInterface):
    """Encode text using Base64 algorithm."""

    name = "base64_encode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """
        Encode text to Base64.

        Args:
            text: Input string

        Returns:
            Base64 encoded string
        """
        if not text:
            return ""
        encoded = base64.b64encode(text.encode('utf-8'))
        return encoded.decode('ascii')

    def decode(self, text: str) -> str:
        """Decode Base64 string (not applicable for encoder)."""
        raise NotImplementedError("Use Base64Decode for decoding")


class Base64Decode(TransformerInterface):
    """Decode Base64 encoded text."""

    name = "base64_decode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use Base64Encode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode Base64 string to text.

        Args:
            text: Base64 encoded string

        Returns:
            Decoded original string

        Raises:
            binascii.Error: If input is not valid Base64
        """
        if not text:
            return ""
        decoded = base64.b64decode(text.encode('ascii'))
        return decoded.decode('utf-8')


class URLEncode(TransformerInterface):
    """Encode text using URL percent-encoding."""

    name = "url_encode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """
        Encode text for safe URL usage.

        Args:
            text: Input string

        Returns:
            URL encoded string (spaces become +, special chars become %XX)
        """
        return quote(text, safe='')

    def decode(self, text: str) -> str:
        """Decode URL string (not applicable for encoder)."""
        raise NotImplementedError("Use URLDecode for decoding")


class URLDecode(TransformerInterface):
    """Decode URL encoded text."""

    name = "url_decode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use URLEncode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode URL encoded string.

        Args:
            text: URL encoded string

        Returns:
            Decoded original string
        """
        return unquote(text)


class HexEncode(TransformerInterface):
    """Encode text using hexadecimal representation."""

    name = "hex_encode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """
        Encode text to hexadecimal.

        Args:
            text: Input string

        Returns:
            Hexadecimal string (lowercase)
        """
        if not text:
            return ""
        return text.encode('utf-8').hex()

    def decode(self, text: str) -> str:
        """Decode hex string (not applicable for encoder)."""
        raise NotImplementedError("Use HexDecode for decoding")


class HexDecode(TransformerInterface):
    """Decode hexadecimal encoded text."""

    name = "hex_decode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use HexEncode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode hexadecimal string to text.

        Args:
            text: Hexadecimal string

        Returns:
            Decoded original string

        Raises:
            binascii.Error: If input is not valid hexadecimal
            ValueError: If input has odd length
        """
        if not text:
            return ""
        decoded = binascii.unhexlify(text)
        return decoded.decode('utf-8')


# Advanced Base Encodings

class Base32Encode(TransformerInterface):
    """Encode text using Base32 algorithm (RFC 4648)."""

    name = "base32_encode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """
        Encode text to Base32.

        Args:
            text: Input string

        Returns:
            Base32 encoded string
        """
        if not text:
            return ""
        encoded = base64.b32encode(text.encode('utf-8'))
        return encoded.decode('ascii')

    def decode(self, text: str) -> str:
        """Decode Base32 string (not applicable for encoder)."""
        raise NotImplementedError("Use Base32Decode for decoding")


class Base32Decode(TransformerInterface):
    """Decode Base32 encoded text."""

    name = "base32_decode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use Base32Encode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode Base32 string to text.

        Args:
            text: Base32 encoded string

        Returns:
            Decoded original string
        """
        if not text:
            return ""
        decoded = base64.b32decode(text.encode('ascii'), casefold=True)
        return decoded.decode('utf-8')


class Base85Encode(TransformerInterface):
    """Encode text using Base85 algorithm (RFC 1924)."""

    name = "base85_encode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """
        Encode text to Base85.

        Args:
            text: Input string

        Returns:
            Base85 encoded string
        """
        if not text:
            return ""
        encoded = base64.b85encode(text.encode('utf-8'))
        return encoded.decode('ascii')

    def decode(self, text: str) -> str:
        """Decode Base85 string (not applicable for encoder)."""
        raise NotImplementedError("Use Base85Decode for decoding")


class Base85Decode(TransformerInterface):
    """Decode Base85 encoded text."""

    name = "base85_decode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use Base85Encode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode Base85 string to text.

        Args:
            text: Base85 encoded string

        Returns:
            Decoded original string
        """
        if not text:
            return ""
        decoded = base64.b85decode(text.encode('ascii'))
        return decoded.decode('utf-8')


# Base58 alphabet (Bitcoin style)
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE58_ALPHABET_MAP = {c: i for i, c in enumerate(BASE58_ALPHABET)}


class Base58Encode(TransformerInterface):
    """Encode text using Base58 algorithm (Bitcoin style)."""

    name = "base58_encode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """
        Encode text to Base58.

        Args:
            text: Input string

        Returns:
            Base58 encoded string
        """
        if not text:
            return ""

        # Convert to bytes
        bytes_data = text.encode('utf-8')

        # Convert bytes to integer
        num = int.from_bytes(bytes_data, 'big')

        # Convert to Base58
        result = ""
        while num > 0:
            num, remainder = divmod(num, 58)
            result = BASE58_ALPHABET[remainder] + result

        # Add leading zeros
        for byte in bytes_data:
            if byte == 0:
                result = "1" + result
            else:
                break

        return result

    def decode(self, text: str) -> str:
        """Decode Base58 string (not applicable for encoder)."""
        raise NotImplementedError("Use Base58Decode for decoding")


class Base58Decode(TransformerInterface):
    """Decode Base58 encoded text."""

    name = "base58_decode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use Base58Encode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode Base58 string to text.

        Args:
            text: Base58 encoded string

        Returns:
            Decoded original string
        """
        if not text:
            return ""

        # Convert Base58 to integer
        num = 0
        for char in text:
            if char not in BASE58_ALPHABET_MAP:
                raise ValueError(f"Invalid Base58 character: {char}")
            num = num * 58 + BASE58_ALPHABET_MAP[char]

        # Convert integer to bytes
        # Calculate byte length
        byte_length = (num.bit_length() + 7) // 8
        if byte_length == 0:
            return ""

        bytes_data = num.to_bytes(byte_length, 'big')

        # Handle leading zeros
        leading_zeros = 0
        for char in text:
            if char == "1":
                leading_zeros += 1
            else:
                break

        if leading_zeros > 0:
            bytes_data = b'\x00' * leading_zeros + bytes_data

        return bytes_data.decode('utf-8')


# Base62 alphabet (0-9, A-Z, a-z)
BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE62_ALPHABET_MAP = {c: i for i, c in enumerate(BASE62_ALPHABET)}


class Base62Encode(TransformerInterface):
    """Encode text using Base62 algorithm."""

    name = "base62_encode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """
        Encode text to Base62.

        Args:
            text: Input string

        Returns:
            Base62 encoded string
        """
        if not text:
            return ""

        # Convert to bytes
        bytes_data = text.encode('utf-8')

        # Convert bytes to integer
        num = int.from_bytes(bytes_data, 'big')

        # Convert to Base62
        result = ""
        while num > 0:
            num, remainder = divmod(num, 62)
            result = BASE62_ALPHABET[remainder] + result

        # Add leading zeros (represented as '0')
        for byte in bytes_data:
            if byte == 0:
                result = "0" + result
            else:
                break

        return result if result else "0"

    def decode(self, text: str) -> str:
        """Decode Base62 string (not applicable for encoder)."""
        raise NotImplementedError("Use Base62Decode for decoding")


class Base62Decode(TransformerInterface):
    """Decode Base62 encoded text."""

    name = "base62_decode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use Base62Encode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode Base62 string to text.

        Args:
            text: Base62 encoded string

        Returns:
            Decoded original string
        """
        if not text:
            return ""

        # Convert Base62 to integer
        num = 0
        for char in text:
            if char not in BASE62_ALPHABET_MAP:
                raise ValueError(f"Invalid Base62 character: {char}")
            num = num * 62 + BASE62_ALPHABET_MAP[char]

        # Convert integer to bytes
        byte_length = (num.bit_length() + 7) // 8
        if byte_length == 0:
            return ""

        bytes_data = num.to_bytes(byte_length, 'big')

        # Handle leading zeros
        leading_zeros = 0
        for char in text:
            if char == "0":
                leading_zeros += 1
            else:
                break

        if leading_zeros > 0:
            bytes_data = b'\x00' * leading_zeros + bytes_data

        return bytes_data.decode('utf-8')


# Base91 implementation (based on base91 library)
BASE91_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,-./:;<=>?@[]^_`{|}~\""
BASE91_ALPHABET_MAP = {c: i for i, c in enumerate(BASE91_ALPHABET)}


class Base91Encode(TransformerInterface):
    """Encode text using Base91 algorithm."""

    name = "base91_encode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """
        Encode text to Base91.

        Args:
            text: Input string

        Returns:
            Base91 encoded string
        """
        if not text:
            return ""

        bytes_data = text.encode('utf-8')
        b = 0
        n = 0
        result = []

        for byte in bytes_data:
            b |= byte << n
            n += 8
            if n > 13:
                v = b & 8191
                if v > 88:
                    b >>= 13
                    n -= 13
                else:
                    v = b & 16383
                    b >>= 14
                    n -= 14
                result.append(BASE91_ALPHABET[v % 91])
                result.append(BASE91_ALPHABET[v // 91])

        if n > 0:
            result.append(BASE91_ALPHABET[b % 91])
            if n > 7 or b > 90:
                result.append(BASE91_ALPHABET[b // 91])

        return ''.join(result)

    def decode(self, text: str) -> str:
        """Decode Base91 string (not applicable for encoder)."""
        raise NotImplementedError("Use Base91Decode for decoding")


class Base91Decode(TransformerInterface):
    """Decode Base91 encoded text."""

    name = "base91_decode"
    category = "encoding"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use Base91Encode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode Base91 string to text.

        Args:
            text: Base91 encoded string

        Returns:
            Decoded original string
        """
        if not text:
            return ""

        b = 0
        n = 0
        v = -1
        result = []

        for char in text:
            if char not in BASE91_ALPHABET_MAP:
                raise ValueError(f"Invalid Base91 character: {char}")

            c = BASE91_ALPHABET_MAP[char]
            if v < 0:
                v = c
            else:
                v += c * 91
                b |= v << n
                n += 13 if (v & 8191) > 88 else 14
                while n > 7:
                    result.append((b & 255))
                    b >>= 8
                    n -= 8
                v = -1

        if v + 1:
            result.append((b | v << n) & 255)

        return bytes(result).decode('utf-8')
