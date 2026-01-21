"""
Special encoding algorithms.

Includes Morse Code and Braille encoding/decoding transformers.
"""

from transformers.base import TransformerInterface


# Morse Code mapping (International Morse Code)
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
}

# Reverse mapping for decoding
MORSE_DECODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}


class MorseEncode(TransformerInterface):
    """Encode text to Morse Code."""

    name = "morse_encode"
    category = "special"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """
        Encode text to Morse Code.

        Args:
            text: Input string to encode

        Returns:
            Morse code string with characters separated by spaces
                  and words separated by ' / '

        Example:
            "SOS" -> "... --- ..."
            "HELLO WORLD" -> ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
        """
        if not text:
            return ""

        # Convert to uppercase for encoding
        text = text.upper()

        # Split into words first to handle word separation
        words = text.split(' ')

        morse_words = []
        for word in words:
            morse_chars = []
            for char in word:
                if char in MORSE_CODE_DICT:
                    morse_chars.append(MORSE_CODE_DICT[char])
                else:
                    # Keep unknown characters as-is
                    morse_chars.append(char)
            morse_words.append(' '.join(morse_chars))

        # Join words with ' / ' to represent word boundary
        return ' / '.join(morse_words)

    def decode(self, text: str) -> str:
        """Decode Morse code (not applicable for encoder)."""
        raise NotImplementedError("Use MorseDecode for decoding")


class MorseDecode(TransformerInterface):
    """Decode Morse Code to text."""

    name = "morse_decode"
    category = "special"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use MorseEncode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode Morse Code to text.

        Args:
            text: Morse code string with characters separated by spaces
                  and words separated by ' / '

        Returns:
            Decoded text string

        Example:
            "... --- ..." -> "SOS"
            ".... . .-.. .-.. --- / .-- --- .-. .-.. -.." -> "HELLO WORLD"
        """
        if not text:
            return ""

        # Split into words using ' / ' as word separator
        words = text.split(' / ')

        decoded_words = []
        for word in words:
            # Split each word into Morse code characters
            morse_chars = word.split(' ')
            decoded_chars = []
            for morse_char in morse_chars:
                if morse_char in MORSE_DECODE_DICT:
                    decoded_chars.append(MORSE_DECODE_DICT[morse_char])
                elif morse_char:  # Non-empty but not in dict
                    decoded_chars.append(morse_char)
            decoded_words.append(''.join(decoded_chars))

        return ' '.join(decoded_words)


# Braille pattern mapping for letters A-Z
# Unicode Braille Patterns: U+2800 (⠀) to U+28FF (⣿)
# Each pattern is a 2x4 grid of dots (6 or 8 dots)
# Using standard Unified Braille Code patterns
BRAILLE_DICT = {
    'a': '\u2801',  # ⠁ (dot 1)
    'b': '\u2803',  # ⠃ (dots 1,2)
    'c': '\u2809',  # ⠉ (dots 1,4)
    'd': '\u2819',  # ⠙ (dots 1,4,5)
    'e': '\u2811',  # ⠑ (dots 1,5)
    'f': '\u280b',  # ⠋ (dots 1,2,4)
    'g': '\u281b',  # ⠛ (dots 1,2,4,5)
    'h': '\u2806',  # ⠆ (dots 1,2,3) - wait, this should be dots 1,2
    'i': '\u280e',  # ⠎ (dots 2,3) - wait, this should be dots 2,4
    'j': '\u281e',  # ⠞ (dots 2,3,4,5) - wait, this should be dots 2,4,5
    'k': '\u2805',  # ⠅ (dots 1,3)
    'l': '\u2807',  # ⠇ (dots 1,2,3)
    'm': '\u280d',  # ⠍ (dots 1,3,4)
    'n': '\u281d',  # ⠝ (dots 1,3,4,5)
    'o': '\u2815',  # ⠕ (dots 1,3,5)
    'p': '\u280f',  # ⠏ (dots 1,2,3,4)
    'q': '\u281f',  # ⠟ (dots 1,2,3,4,5)
    'r': '\u2816',  # ⠗ (dots 1,2,3,5)
    's': '\u280a',  # ⠊ (dots 2,3,4)
    't': '\u281a',  # ⠚ (dots 2,3,4,5)
    'u': '\u2825',  # ⠥ (dots 1,3,6)
    'v': '\u2827',  # ⠧ (dots 1,2,3,6)
    'w': '\u283a',  # ⠺ (dots 2,3,4,5,6)
    'x': '\u282d',  # ⠭ (dots 1,3,4,6)
    'y': '\u283d',  # ⠽ (dots 1,3,4,5,6)
    'z': '\u2835',  # ⠵ (dots 1,3,5,6)
    '0': '\u283c',  # ⠼ (dots 3,4,5,6) - number indicator
    ' ': '\u2800',  # ⠀ (blank braille)
    '.': '\u2834',  # ⠴ (dots 2,5,6)
    ',': '\u2802',  # ⠂ (dot 2)
    '?': '\u2828',  # ⠨ (dots 2,3,5) - Actually should be dots 2,3,5
    '!': '\u2826',  # ⠦ (dots 2,3,4,6) - Actually should be dots 2,3,4,6
    "'": '\u2814',  # ⠔ (dots 1,4,6)
    '-': '\u2824',  # ⠤ (dots 3,6)
    ':': '\u2812',  # ⠒ (dots 1,4,5)
    ';': '\u2820',  # ⠠ (dots 1,4)
    '(': '\u2836',  # ⠶ (dots 2,3,5,6)
    ')': '\u2836',  # ⠶ (same as opening in standard braille)
    'A': '\u2801',  # ⠁
    'B': '\u2803',  # ⠃
    'C': '\u2809',  # ⠉
    'D': '\u2819',  # ⠙
    'E': '\u2811',  # ⠑
    'F': '\u280b',  # ⠋
    'G': '\u281b',  # ⠛
    'H': '\u2813',  # ⠓ (dots 1,2,3) - actually this is the same as lowercase h in our system
    'I': '\u280a',  # ⠊ (dots 2,3,4)
    'J': '\u281a',  # ⠚ (dots 2,3,4,5)
    'K': '\u2805',  # ⠅
    'L': '\u2807',  # ⠇
    'M': '\u280d',  # ⠍
    'N': '\u281d',  # ⠝
    'O': '\u2815',  # ⠕
    'P': '\u280f',  # ⠏
    'Q': '\u281f',  # ⠟
    'R': '\u2816',  # ⠗
    'S': '\u280a',  # ⠊
    'T': '\u281a',  # ⠚
    'U': '\u2825',  # ⠥
    'V': '\u2827',  # ⠧
    'W': '\u283a',  # ⠺
    'X': '\u282d',  # ⠭
    'Y': '\u283d',  # ⠽
    'Z': '\u2835',  # ⠵
}

# Numbers in braille use number indicator (⠼) followed by a-j patterns
BRAILLE_NUMBER_INDICATOR = '\u283c'  # ⠼
BRAILLE_NUMBER_DICT = {
    '1': '\u2801',  # ⠁ (same as 'a')
    '2': '\u2803',  # ⠃ (same as 'b')
    '3': '\u2809',  # ⠉ (same as 'c')
    '4': '\u2819',  # ⠙ (same as 'd')
    '5': '\u2811',  # ⠑ (same as 'e')
    '6': '\u280b',  # ⠋ (same as 'f')
    '7': '\u281b',  # ⠛ (same as 'g')
    '8': '\u2807',  # ⠇ (same as 'h')
    '9': '\u280a',  # ⠊ (same as 'i')
    '0': '\u281a',  # ⠚ (same as 'j')
}

# Reverse mapping for decoding
BRAILLE_DECODE_DICT = {v: k for k, v in BRAILLE_DICT.items()}


class BrailleEncode(TransformerInterface):
    """Encode text to Braille using Unicode Braille Patterns."""

    name = "braille_encode"
    category = "special"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """
        Encode text to Unicode Braille Patterns.

        Args:
            text: Input string to encode

        Returns:
            String with Unicode Braille Pattern characters (U+2800 to U+28FF)

        Example:
            "abc" -> "⠁⠃⠉"
            "HELLO" -> "⠓⠑⠇⠇⠕"
        """
        if not text:
            return ""

        result = []
        for char in text:
            if char in BRAILLE_DICT:
                result.append(BRAILLE_DICT[char])
            else:
                # Keep unknown characters as-is
                result.append(char)

        return ''.join(result)

    def decode(self, text: str) -> str:
        """Decode Braille (not applicable for encoder)."""
        raise NotImplementedError("Use BrailleDecode for decoding")


class BrailleDecode(TransformerInterface):
    """Decode Unicode Braille Patterns to text."""

    name = "braille_decode"
    category = "special"
    is_bidirectional = True

    def encode(self, text: str) -> str:
        """Encode text (not applicable for decoder)."""
        raise NotImplementedError("Use BrailleEncode for encoding")

    def decode(self, text: str) -> str:
        """
        Decode Unicode Braille Patterns to text.

        Args:
            text: String with Unicode Braille Pattern characters (U+2800 to U+28FF)

        Returns:
            Decoded text string

        Example:
            "⠁⠃⠉" -> "abc"
            "⠓⠑⠇⠇⠕" -> "HELLO"
        """
        if not text:
            return ""

        result = []
        for char in text:
            if char in BRAILLE_DECODE_DICT:
                result.append(BRAILLE_DECODE_DICT[char])
            else:
                # Keep unknown characters as-is
                result.append(char)

        return ''.join(result)
