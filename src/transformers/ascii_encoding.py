"""
ASCII, Binary, and Octal encoding transformers.

Converts between text and various numeric representations.
"""

import re
from abc import ABC, abstractmethod
from typing import List


class ASCIIEncodingTransformer(ABC):
    """Base class for ASCII encoding transformers."""

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> str:
        return "Encoding"

    @property
    def is_bidirectional(self) -> bool:
        return False


class BinaryEncode(ASCIIEncodingTransformer):
    """Convert text to binary representation (8-bit per character)."""

    def __init__(self):
        self._name = "binary_encode"

    def encode(self, text: str) -> str:
        """Convert text to binary (space-separated 8-bit groups)."""
        if not text:
            return ""

        binary_chars = []
        for char in text:
            # Convert each character to 8-bit binary
            binary = bin(ord(char))[2:].zfill(8)
            binary_chars.append(binary)

        return " ".join(binary_chars)

    def decode(self, text: str) -> str:
        """Convert binary to text."""
        if not text:
            return ""

        # Remove all whitespace and split
        binary_str = text.strip()
        binary_groups = binary_str.split()

        result = []
        for group in binary_groups:
            # Remove any non-binary characters
            clean_binary = re.sub(r'[^01]', '', group)

            if clean_binary:
                # Pad to multiple of 8
                padding = (8 - len(clean_binary) % 8) % 8
                clean_binary = clean_binary.zfill(len(clean_binary) + padding)

                # Convert each 8-bit group to character
                for i in range(0, len(clean_binary), 8):
                    byte = clean_binary[i:i+8]
                    if len(byte) == 8:
                        result.append(chr(int(byte, 2)))

        return "".join(result)


class BinaryDecode(BinaryEncode):
    """Alias for binary decode operation."""

    def __init__(self):
        super().__init__()
        self._name = "binary_decode"


class OctalEncode(ASCIIEncodingTransformer):
    """Convert text to octal representation."""

    def __init__(self):
        self._name = "octal_encode"

    def encode(self, text: str) -> str:
        """Convert text to octal (space-separated)."""
        if not text:
            return ""

        octal_chars = []
        for char in text:
            # Convert each character to 3-digit octal
            octal = oct(ord(char))[2:].zfill(3)
            octal_chars.append(octal)

        return " ".join(octal_chars)

    def decode(self, text: str) -> str:
        """Convert octal to text."""
        if not text:
            return ""

        # Remove all whitespace and split
        octal_str = text.strip()
        octal_groups = octal_str.split()

        result = []
        for group in octal_groups:
            # Remove any non-octal characters
            clean_octal = re.sub(r'[^0-7]', '', group)

            # Try to parse as octal (handle 1-3 digit groups)
            if clean_octal:
                try:
                    # Pad to multiple of 3
                    padding = (3 - len(clean_octal) % 3) % 3
                    clean_octal = clean_octal.zfill(len(clean_octal) + padding)

                    # Convert each 3-digit group to character
                    for i in range(0, len(clean_octal), 3):
                        byte = clean_octal[i:i+3]
                        if len(byte) == 3:
                            result.append(chr(int(byte, 8)))
                except ValueError:
                    continue

        return "".join(result)


class OctalDecode(OctalEncode):
    """Alias for octal decode operation."""

    def __init__(self):
        super().__init__()
        self._name = "octal_decode"


class ASCIIEncode(ASCIIEncodingTransformer):
    """Convert text to ASCII decimal codes."""

    def __init__(self):
        self._name = "ascii_encode"

    def encode(self, text: str) -> str:
        """Convert text to ASCII decimal codes (space-separated)."""
        if not text:
            return ""

        ascii_codes = []
        for char in text:
            ascii_codes.append(str(ord(char)))

        return " ".join(ascii_codes)

    def decode(self, text: str) -> str:
        """Convert ASCII decimal codes to text."""
        if not text:
            return ""

        # Extract all numbers from the text
        numbers = re.findall(r'\d+', text)

        result = []
        for num_str in numbers:
            try:
                code = int(num_str)
                # Valid ASCII range is 0-127, extended ASCII is 0-255
                if 0 <= code <= 1114111:  # Unicode range
                    result.append(chr(code))
            except (ValueError, OverflowError):
                continue

        return "".join(result)


class ASCIIDecode(ASCIIEncode):
    """Alias for ASCII decode operation."""

    def __init__(self):
        super().__init__()
        self._name = "ascii_decode"
