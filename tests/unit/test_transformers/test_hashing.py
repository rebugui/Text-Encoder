"""
Unit tests for hash algorithms.

Tests verify that:
1. MD5, SHA-1, SHA-256, SHA-512, BLAKE2s, BLAKE2b, CRC32, Adler32 produce correct hashes
2. Hash algorithms are unidirectional (is_bidirectional=False)
3. Handle empty strings and unicode correctly
4. Produce consistent output for same input
"""

import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestMD5:
    """Test suite for MD5 hash."""

    def test_md5_simple_text(self):
        """MD5 produces correct hash for simple text."""
        from transformers.hashing import MD5Hash

        transformer = MD5Hash()
        result = transformer.encode("Hello")

        # Known MD5 hash of "Hello"
        assert result == "8b1a9953c4611296a827abf8c47804d7"

    def test_md5_empty_string(self):
        """MD5 handles empty string."""
        from transformers.hashing import MD5Hash

        transformer = MD5Hash()
        result = transformer.encode("")

        # Known MD5 hash of empty string
        assert result == "d41d8cd98f00b204e9800998ecf8427e"

    def test_md5_unicode(self):
        """MD5 handles unicode correctly."""
        from transformers.hashing import MD5Hash

        transformer = MD5Hash()
        result = transformer.encode("안녕하세요")

        # Should produce consistent hash
        assert len(result) == 32  # MD5 is always 32 hex chars
        assert all(c in '0123456789abcdef' for c in result)

    def test_md5_is_unidirectional(self):
        """MD5 is unidirectional (cannot be reversed)."""
        from transformers.hashing import MD5Hash

        transformer = MD5Hash()
        assert transformer.is_bidirectional is False

    def test_md5_decode_raises_error(self):
        """MD5 decode raises NotImplementedError."""
        from transformers.hashing import MD5Hash

        transformer = MD5Hash()
        with pytest.raises(NotImplementedError):
            transformer.decode("any_hash")

    def test_md5_attributes(self):
        """MD5 has correct attributes."""
        from transformers.hashing import MD5Hash

        transformer = MD5Hash()
        assert transformer.name == "md5"
        assert transformer.category == "hashing"


class TestSHA1:
    """Test suite for SHA-1 hash."""

    def test_sha1_simple_text(self):
        """SHA-1 produces correct hash for simple text."""
        from transformers.hashing import SHA1Hash

        transformer = SHA1Hash()
        result = transformer.encode("Hello")

        # Known SHA-1 hash of "Hello"
        assert result == "f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0"

    def test_sha1_empty_string(self):
        """SHA-1 handles empty string."""
        from transformers.hashing import SHA1Hash

        transformer = SHA1Hash()
        result = transformer.encode("")

        # Known SHA-1 hash of empty string
        assert result == "da39a3ee5e6b4b0d3255bfef95601890afd80709"

    def test_sha1_length(self):
        """SHA-1 produces consistent length."""
        from transformers.hashing import SHA1Hash

        transformer = SHA1Hash()
        result = transformer.encode("test")

        # SHA-1 is always 40 hex chars
        assert len(result) == 40


class TestSHA256:
    """Test suite for SHA-256 hash."""

    def test_sha256_simple_text(self):
        """SHA-256 produces correct hash for simple text."""
        from transformers.hashing import SHA256Hash

        transformer = SHA256Hash()
        result = transformer.encode("Hello")

        # Known SHA-256 hash of "Hello"
        assert result == "185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969"

    def test_sha256_empty_string(self):
        """SHA-256 handles empty string."""
        from transformers.hashing import SHA256Hash

        transformer = SHA256Hash()
        result = transformer.encode("")

        # Known SHA-256 hash of empty string
        assert result == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    def test_sha256_length(self):
        """SHA-256 produces consistent length."""
        from transformers.hashing import SHA256Hash

        transformer = SHA256Hash()
        result = transformer.encode("test")

        # SHA-256 is always 64 hex chars
        assert len(result) == 64


class TestSHA512:
    """Test suite for SHA-512 hash."""

    def test_sha512_simple_text(self):
        """SHA-512 produces hash for simple text."""
        from transformers.hashing import SHA512Hash

        transformer = SHA512Hash()
        result = transformer.encode("Hello")

        # SHA-512 is always 128 hex chars
        assert len(result) == 128

    def test_sha512_empty_string(self):
        """SHA-512 handles empty string."""
        from transformers.hashing import SHA512Hash

        transformer = SHA512Hash()
        result = transformer.encode("")

        # Known SHA-512 hash of empty string
        assert result == "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e"


class TestBLAKE2:
    """Test suite for BLAKE2s and BLAKE2b hashes."""

    def test_blake2s_simple_text(self):
        """BLAKE2s produces hash for simple text."""
        from transformers.hashing import BLAKE2sHash

        transformer = BLAKE2sHash()
        result = transformer.encode("Hello")

        # BLAKE2s produces 64 hex chars (256 bits)
        assert len(result) == 64

    def test_blake2b_simple_text(self):
        """BLAKE2b produces hash for simple text."""
        from transformers.hashing import BLAKE2bHash

        transformer = BLAKE2bHash()
        result = transformer.encode("Hello")

        # BLAKE2b produces 128 hex chars (512 bits)
        assert len(result) == 128

    def test_blake2s_empty_string(self):
        """BLAKE2s handles empty string."""
        from transformers.hashing import BLAKE2sHash

        transformer = BLAKE2sHash()
        result = transformer.encode("")

        # Known BLAKE2s hash of empty string (Python hashlib)
        assert result == "69217a3079908094e11121d042354a7c1f55b6482ca1a51e1b250dfd1ed0eef9"

    def test_blake2b_empty_string(self):
        """BLAKE2b handles empty string."""
        from transformers.hashing import BLAKE2bHash

        transformer = BLAKE2bHash()
        result = transformer.encode("")

        # Known BLAKE2b hash of empty string (Python hashlib)
        assert result == "786a02f742015903c6c6fd852552d272912f4740e15847618a86e217f71f5419d25e1031afee585313896444934eb04b903a685b1448b755d56f701afe9be2ce"


class TestCRC32:
    """Test suite for CRC32 checksum."""

    def test_crc32_simple_text(self):
        """CRC32 produces checksum for simple text."""
        from transformers.hashing import CRC32Hash

        transformer = CRC32Hash()
        result = transformer.encode("Hello")

        # CRC32 produces 8 hex chars
        assert len(result) == 8

    def test_crc32_empty_string(self):
        """CRC32 handles empty string."""
        from transformers.hashing import CRC32Hash

        transformer = CRC32Hash()
        result = transformer.encode("")

        # Known CRC32 of empty string
        assert result == "00000000"

    def test_crc32_consistent(self):
        """CRC32 produces consistent output."""
        from transformers.hashing import CRC32Hash

        transformer = CRC32Hash()
        result1 = transformer.encode("test")
        result2 = transformer.encode("test")

        assert result1 == result2


class TestAdler32:
    """Test suite for Adler32 checksum."""

    def test_adler32_simple_text(self):
        """Adler32 produces checksum for simple text."""
        from transformers.hashing import Adler32Hash

        transformer = Adler32Hash()
        result = transformer.encode("Hello")

        # Adler32 produces 8 hex chars
        assert len(result) == 8

    def test_adler32_empty_string(self):
        """Adler32 handles empty string."""
        from transformers.hashing import Adler32Hash

        transformer = Adler32Hash()
        result = transformer.encode("")

        # Known Adler32 of empty string
        assert result == "00000001"

    def test_adler32_consistent(self):
        """Adler32 produces consistent output."""
        from transformers.hashing import Adler32Hash

        transformer = Adler32Hash()
        result1 = transformer.encode("test")
        result2 = transformer.encode("test")

        assert result1 == result2
