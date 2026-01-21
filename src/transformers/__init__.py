"""
Transformers package.

Contains all transformation algorithm implementations organized by category:
- base: TransformerInterface abstract base class
- encoding: Base64, URL, Hex, Base32, Base58, etc.
- hashing: MD5, SHA, BLAKE2, CRC32, etc.
- text_processing: JSON formatting, case conversion, etc.
- special: Morse Code, Braille
- ciphers: ROT13, Caesar, Vigenère, Atbash
"""

from transformers.base import TransformerInterface

__all__ = ['TransformerInterface']
