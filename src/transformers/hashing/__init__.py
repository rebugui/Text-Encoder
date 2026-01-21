"""
Hash algorithms.

Includes MD5, SHA-1, SHA-256, SHA-512, BLAKE2s, BLAKE2b, CRC32, Adler32.

Note: All hash algorithms are unidirectional (is_bidirectional=False).
"""

import hashlib
import zlib

from transformers.base import TransformerInterface


class MD5Hash(TransformerInterface):
    """MD5 hash algorithm (128-bit)."""

    name = "md5"
    category = "hashing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Calculate MD5 hash of text.

        Args:
            text: Input string

        Returns:
            MD5 hash as 32-character hexadecimal string
        """
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def decode(self, text: str) -> str:
        """Hash cannot be reversed."""
        raise NotImplementedError("MD5 is a one-way hash function and cannot be decoded")


class SHA1Hash(TransformerInterface):
    """SHA-1 hash algorithm (160-bit)."""

    name = "sha1"
    category = "hashing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Calculate SHA-1 hash of text.

        Args:
            text: Input string

        Returns:
            SHA-1 hash as 40-character hexadecimal string
        """
        return hashlib.sha1(text.encode('utf-8')).hexdigest()

    def decode(self, text: str) -> str:
        """Hash cannot be reversed."""
        raise NotImplementedError("SHA-1 is a one-way hash function and cannot be decoded")


class SHA256Hash(TransformerInterface):
    """SHA-256 hash algorithm (256-bit)."""

    name = "sha256"
    category = "hashing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Calculate SHA-256 hash of text.

        Args:
            text: Input string

        Returns:
            SHA-256 hash as 64-character hexadecimal string
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def decode(self, text: str) -> str:
        """Hash cannot be reversed."""
        raise NotImplementedError("SHA-256 is a one-way hash function and cannot be decoded")


class SHA512Hash(TransformerInterface):
    """SHA-512 hash algorithm (512-bit)."""

    name = "sha512"
    category = "hashing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Calculate SHA-512 hash of text.

        Args:
            text: Input string

        Returns:
            SHA-512 hash as 128-character hexadecimal string
        """
        return hashlib.sha512(text.encode('utf-8')).hexdigest()

    def decode(self, text: str) -> str:
        """Hash cannot be reversed."""
        raise NotImplementedError("SHA-512 is a one-way hash function and cannot be decoded")


class BLAKE2sHash(TransformerInterface):
    """BLAKE2s hash algorithm (256-bit, optimized for 32-bit platforms)."""

    name = "blake2s"
    category = "hashing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Calculate BLAKE2s hash of text.

        Args:
            text: Input string

        Returns:
            BLAKE2s hash as 64-character hexadecimal string
        """
        return hashlib.blake2s(text.encode('utf-8')).hexdigest()

    def decode(self, text: str) -> str:
        """Hash cannot be reversed."""
        raise NotImplementedError("BLAKE2s is a one-way hash function and cannot be decoded")


class BLAKE2bHash(TransformerInterface):
    """BLAKE2b hash algorithm (512-bit, optimized for 64-bit platforms)."""

    name = "blake2b"
    category = "hashing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Calculate BLAKE2b hash of text.

        Args:
            text: Input string

        Returns:
            BLAKE2b hash as 128-character hexadecimal string
        """
        return hashlib.blake2b(text.encode('utf-8')).hexdigest()

    def decode(self, text: str) -> str:
        """Hash cannot be reversed."""
        raise NotImplementedError("BLAKE2b is a one-way hash function and cannot be decoded")


class CRC32Hash(TransformerInterface):
    """CRC32 checksum algorithm."""

    name = "crc32"
    category = "hashing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Calculate CRC32 checksum of text.

        Args:
            text: Input string

        Returns:
            CRC32 checksum as 8-character hexadecimal string
        """
        checksum = zlib.crc32(text.encode('utf-8'))
        # Convert to unsigned 32-bit integer, then to hex
        return format(checksum & 0xFFFFFFFF, '08x')

    def decode(self, text: str) -> str:
        """Checksum cannot be reversed."""
        raise NotImplementedError("CRC32 is a one-way checksum function and cannot be decoded")


class Adler32Hash(TransformerInterface):
    """Adler32 checksum algorithm."""

    name = "adler32"
    category = "hashing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Calculate Adler32 checksum of text.

        Args:
            text: Input string

        Returns:
            Adler32 checksum as 8-character hexadecimal string
        """
        checksum = zlib.adler32(text.encode('utf-8'))
        # Convert to unsigned 32-bit integer, then to hex
        return format(checksum & 0xFFFFFFFF, '08x')

    def decode(self, text: str) -> str:
        """Checksum cannot be reversed."""
        raise NotImplementedError("Adler32 is a one-way checksum function and cannot be decoded")
