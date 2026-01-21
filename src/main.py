#!/usr/bin/env python3
"""
Text Encoder - Main entry point.

확장형 GUI 텍스트 유틸리티 툴
80+ 변환 알고리즘을 지원하는 크로스플랫폼 애플리케이션
Refactored to CustomTkinter for modern UI
"""

import sys
from pathlib import Path

# Add src directory to path - handle both normal execution and PyInstaller
if getattr(sys, 'frozen', False):
    # Running as compiled executable (PyInstaller)
    # PyInstaller extracts to sys._MEIPASS
    if hasattr(sys, '_MEIPASS'):
        sys.path.insert(0, sys._MEIPASS)
else:
    # Running as script
    sys.path.insert(0, str(Path(__file__).parent))

# Import with absolute path from src
from ui.main_window import MainWindow
from ui.system_tray import SystemTray
from hotkey.global_hotkey import GlobalHotkey
from registry import AlgorithmRegistry
from transformers.encoding import (
    Base64Encode, Base64Decode,
    Base32Encode, Base32Decode,
    Base58Encode, Base58Decode,
    Base62Encode, Base62Decode,
    Base85Encode, Base85Decode,
    Base91Encode, Base91Decode,
    URLEncode, URLDecode,
    HexEncode, HexDecode
)
from transformers.ascii_encoding import (
    BinaryEncode, BinaryDecode,
    OctalEncode, OctalDecode,
    ASCIIEncode, ASCIIDecode
)
from transformers.hashing import (
    MD5Hash, SHA1Hash, SHA256Hash, SHA512Hash,
    BLAKE2sHash, BLAKE2bHash, CRC32Hash, Adler32Hash
)
from transformers.text_processing import (
    ToUpperCase, ToLowerCase,
    ToCamelCase, ToSnakeCase, ToKebabCase, ToPascalCase,
    ToTitleCase,
    InvertCase, SwapCase,
    RemoveWhitespace, RemoveExtraSpaces, TrimLines,
    RemoveDuplicates, SortLines, ReverseLines,
    ReverseText, ShuffleLines,
    JsonBeautify, JsonMinify,
    XmlBeautify, XmlMinify,
    RemoveBOM,
    CountCharacters, CountWords, CountLines,
    NumberLines,
    RemoveNumbers, RemovePunctuation
)
from transformers.special import (
    MorseEncode, MorseDecode,
    BrailleEncode, BrailleDecode
)
from transformers.special_formats import (
    JWTEncode, JWTDecode,
    HTMLEntityEncode, HTMLEntityDecode,
    CSVFormat, CSVUnformat,
    MarkdownTableEncode,
    MarkdownBoldEncode,
    MarkdownItalicEncode,
    MarkdownCodeEncode,
    MarkdownInlineCodeEncode
)
from transformers.ciphers import (
    ROT13Encode, ROT13Decode,
    CaesarEncode, CaesarDecode,
    VigenereEncode, VigenereDecode,
    AtbashEncode, AtbashDecode
)


def register_algorithms():
    """Register all available transformers with AlgorithmRegistry."""
    registry = AlgorithmRegistry()

    # Standard encoding algorithms
    registry.register(Base64Encode())
    registry.register(Base64Decode())
    registry.register(Base32Encode())
    registry.register(Base32Decode())
    registry.register(Base58Encode())
    registry.register(Base58Decode())
    registry.register(Base62Encode())
    registry.register(Base62Decode())
    registry.register(Base85Encode())
    registry.register(Base85Decode())
    registry.register(Base91Encode())
    registry.register(Base91Decode())
    registry.register(URLEncode())
    registry.register(URLDecode())
    registry.register(HexEncode())
    registry.register(HexDecode())

    # ASCII/Binary/Octal encoding algorithms
    registry.register(BinaryEncode())
    registry.register(BinaryDecode())
    registry.register(OctalEncode())
    registry.register(OctalDecode())
    registry.register(ASCIIEncode())
    registry.register(ASCIIDecode())

    # Hash algorithms
    registry.register(MD5Hash())
    registry.register(SHA1Hash())
    registry.register(SHA256Hash())
    registry.register(SHA512Hash())
    registry.register(BLAKE2sHash())
    registry.register(BLAKE2bHash())
    registry.register(CRC32Hash())
    registry.register(Adler32Hash())

    # Text processing algorithms
    registry.register(ToUpperCase())
    registry.register(ToLowerCase())
    registry.register(ToCamelCase())
    registry.register(ToSnakeCase())
    registry.register(ToKebabCase())
    registry.register(ToPascalCase())
    registry.register(ToTitleCase())
    registry.register(InvertCase())
    registry.register(SwapCase())
    registry.register(RemoveWhitespace())
    registry.register(RemoveExtraSpaces())
    registry.register(TrimLines())
    registry.register(RemoveDuplicates())
    registry.register(SortLines())
    registry.register(ReverseLines())
    registry.register(ReverseText())
    registry.register(ShuffleLines())
    registry.register(JsonBeautify())
    registry.register(JsonMinify())
    registry.register(XmlBeautify())
    registry.register(XmlMinify())
    registry.register(RemoveBOM())
    registry.register(CountCharacters())
    registry.register(CountWords())
    registry.register(CountLines())
    registry.register(NumberLines())
    registry.register(RemoveNumbers())
    registry.register(RemovePunctuation())

    # Special encoding algorithms
    registry.register(MorseEncode())
    registry.register(MorseDecode())
    registry.register(BrailleEncode())
    registry.register(BrailleDecode())

    # Special format algorithms
    registry.register(JWTEncode())
    registry.register(JWTDecode())
    registry.register(HTMLEntityEncode())
    registry.register(HTMLEntityDecode())
    registry.register(CSVFormat())
    registry.register(CSVUnformat())
    registry.register(MarkdownTableEncode())
    registry.register(MarkdownBoldEncode())
    registry.register(MarkdownItalicEncode())
    registry.register(MarkdownCodeEncode())
    registry.register(MarkdownInlineCodeEncode())

    # Classic cipher algorithms
    registry.register(ROT13Encode())
    registry.register(ROT13Decode())
    registry.register(CaesarEncode())
    registry.register(CaesarDecode())
    registry.register(VigenereEncode())
    registry.register(VigenereDecode())
    registry.register(AtbashEncode())
    registry.register(AtbashDecode())

    print(f"Registered {len(registry.get_all())} algorithms")


def main():
    """Main application entry point."""
    # Register all transformation algorithms
    register_algorithms()

    # Create system tray
    system_tray = SystemTray()

    # Create and show main window with system tray
    app = MainWindow(system_tray=system_tray)

    # Setup global hotkey
    global_hotkey = GlobalHotkey()

    def on_hotkey_activated():
        """Handle global hotkey activation."""
        # Bring window to front and focus
        app.deiconify()  # Show if hidden
        app.lift()  # Bring to front
        app.focus()  # Give focus
        # Print notification to console
        print("Global hotkey activated! Window focused.")

    # Connect signal to handler
    global_hotkey.hotkey_activated.connect(on_hotkey_activated)

    # Register the hotkey
    try:
        if global_hotkey.register():
            hotkey_name = "Cmd+Alt+T" if sys.platform == 'darwin' else "Ctrl+Alt+T"
            print(f"Global hotkey registered: {hotkey_name}")
        else:
            print("Failed to register global hotkey")
    except Exception as e:
        print(f"Error registering global hotkey: {e}")

    # Run event loop
    app.mainloop()


if __name__ == "__main__":
    main()
