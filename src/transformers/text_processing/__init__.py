"""
Text processing algorithms.

Includes case conversion, text cleaning, and JSON/XML formatting transformers.
"""

import json
import re
import xml.etree.ElementTree as ET
from io import StringIO

from transformers.base import TransformerInterface


# ============================================================================
# Case Conversion Transformers
# ============================================================================

class ToUpperCase(TransformerInterface):
    """Convert text to uppercase."""

    name = "to_upper_case"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Convert text to uppercase.

        Args:
            text: Input string

        Returns:
            Uppercase string
        """
        return text.upper()

    def decode(self, text: str) -> str:
        """Decode not available for case conversion."""
        raise NotImplementedError("ToUpperCase is not bidirectional")


class ToLowerCase(TransformerInterface):
    """Convert text to lowercase."""

    name = "to_lower_case"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Convert text to lowercase.

        Args:
            text: Input string

        Returns:
            Lowercase string
        """
        return text.lower()

    def decode(self, text: str) -> str:
        """Decode not available for case conversion."""
        raise NotImplementedError("ToLowerCase is not bidirectional")


class ToCamelCase(TransformerInterface):
    """Convert text to camelCase."""

    name = "to_camel_case"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Convert text to camelCase.

        Handles snake_case, kebab-case, PascalCase, and space-separated text.

        Args:
            text: Input string

        Returns:
            camelCase string
        """
        if not text:
            return ""

        # First, split by various separators
        words = re.split(r'[_\-\s]+', text)

        # Process each word to handle PascalCase within words
        processed_words = []
        for word in words:
            if not word:
                continue
            # Split PascalCase words (e.g., "HelloWorld" -> ["Hello", "World"])
            # Find uppercase letters and split
            sub_words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', word)
            if sub_words:
                processed_words.extend(sub_words)
            else:
                processed_words.append(word)

        # First word is lowercase, subsequent words are capitalized
        if not processed_words:
            return ""

        result = processed_words[0].lower()
        for word in processed_words[1:]:
            if word:
                result += word[0].upper() + word[1:].lower()

        return result

    def decode(self, text: str) -> str:
        """Decode not available for case conversion."""
        raise NotImplementedError("ToCamelCase is not bidirectional")


class ToSnakeCase(TransformerInterface):
    """Convert text to snake_case."""

    name = "to_snake_case"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Convert text to snake_case.

        Handles camelCase, PascalCase, kebab-case, and space-separated text.

        Args:
            text: Input string

        Returns:
            snake_case string
        """
        if not text:
            return ""

        # Insert underscore before capital letters (for camelCase/PascalCase)
        text = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text)

        # Replace hyphens and spaces with underscores
        text = re.sub(r'[\-\s]+', '_', text)

        # Convert to lowercase
        return text.lower()

    def decode(self, text: str) -> str:
        """Decode not available for case conversion."""
        raise NotImplementedError("ToSnakeCase is not bidirectional")


class ToKebabCase(TransformerInterface):
    """Convert text to kebab-case."""

    name = "to_kebab_case"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Convert text to kebab-case.

        Handles camelCase, PascalCase, snake_case, and space-separated text.

        Args:
            text: Input string

        Returns:
            kebab-case string
        """
        if not text:
            return ""

        # Insert hyphen before capital letters (for camelCase/PascalCase)
        text = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', text)

        # Replace underscores and spaces with hyphens
        text = re.sub(r'[_\s]+', '-', text)

        # Convert to lowercase
        return text.lower()

    def decode(self, text: str) -> str:
        """Decode not available for case conversion."""
        raise NotImplementedError("ToKebabCase is not bidirectional")


class ToPascalCase(TransformerInterface):
    """Convert text to PascalCase."""

    name = "to_pascal_case"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Convert text to PascalCase.

        Handles camelCase, snake_case, kebab-case, and space-separated text.

        Args:
            text: Input string

        Returns:
            PascalCase string
        """
        if not text:
            return ""

        # Split by various separators and capital letters
        words = re.split(r'[_\-\s]+', text)

        # Capitalize first letter of each word
        result = ""
        for word in words:
            if word:
                # Handle camelCase input
                if word and word[0].islower() and len(word) > 1:
                    # Find uppercase letters and split
                    sub_words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', word)
                    for sub_word in sub_words:
                        result += sub_word[0].upper() + sub_word[1:].lower()
                else:
                    result += word[0].upper() + word[1:].lower()

        return result

    def decode(self, text: str) -> str:
        """Decode not available for case conversion."""
        raise NotImplementedError("ToPascalCase is not bidirectional")


class InvertCase(TransformerInterface):
    """Invert the case of each character."""

    name = "invert_case"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Invert the case of each character in the text.

        Args:
            text: Input string

        Returns:
            String with inverted case
        """
        return text.swapcase()

    def decode(self, text: str) -> str:
        """Decode not available for case inversion."""
        raise NotImplementedError("InvertCase is not bidirectional")


# ============================================================================
# Text Cleaning Transformers
# ============================================================================

class RemoveWhitespace(TransformerInterface):
    """Remove all whitespace from text."""

    name = "remove_whitespace"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Remove all whitespace characters.

        Args:
            text: Input string

        Returns:
            String without any whitespace
        """
        return re.sub(r'\s+', '', text)

    def decode(self, text: str) -> str:
        """Decode not available for whitespace removal."""
        raise NotImplementedError("RemoveWhitespace is not bidirectional")


class RemoveExtraSpaces(TransformerInterface):
    """Replace multiple spaces with a single space."""

    name = "remove_extra_spaces"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Replace multiple whitespace characters with a single space.

        Args:
            text: Input string

        Returns:
            String with normalized whitespace
        """
        return re.sub(r'\s+', ' ', text).strip()

    def decode(self, text: str) -> str:
        """Decode not available for space normalization."""
        raise NotImplementedError("RemoveExtraSpaces is not bidirectional")


class TrimLines(TransformerInterface):
    """Remove leading and trailing whitespace from each line."""

    name = "trim_lines"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Trim leading and trailing whitespace from each line.

        Args:
            text: Input string

        Returns:
            String with trimmed lines
        """
        lines = text.split('\n')
        trimmed_lines = [line.strip() for line in lines]
        return '\n'.join(trimmed_lines)

    def decode(self, text: str) -> str:
        """Decode not available for line trimming."""
        raise NotImplementedError("TrimLines is not bidirectional")


class RemoveDuplicates(TransformerInterface):
    """Remove duplicate lines from text."""

    name = "remove_duplicates"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Remove duplicate lines while preserving order.

        Args:
            text: Input string

        Returns:
            String with duplicate lines removed
        """
        if not text:
            return ""

        lines = text.split('\n')
        seen = set()
        unique_lines = []

        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)

        return '\n'.join(unique_lines)

    def decode(self, text: str) -> str:
        """Decode not available for duplicate removal."""
        raise NotImplementedError("RemoveDuplicates is not bidirectional")


class SortLines(TransformerInterface):
    """Sort lines alphabetically."""

    name = "sort_lines"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Sort lines alphabetically.

        Args:
            text: Input string

        Returns:
            String with sorted lines
        """
        if not text:
            return ""

        lines = text.split('\n')
        sorted_lines = sorted(lines)
        return '\n'.join(sorted_lines)

    def decode(self, text: str) -> str:
        """Decode not available for line sorting."""
        raise NotImplementedError("SortLines is not bidirectional")


class ReverseLines(TransformerInterface):
    """Reverse the order of lines."""

    name = "reverse_lines"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Reverse the order of lines.

        Args:
            text: Input string

        Returns:
            String with reversed line order
        """
        if not text:
            return ""

        lines = text.split('\n')
        reversed_lines = list(reversed(lines))
        return '\n'.join(reversed_lines)

    def decode(self, text: str) -> str:
        """Decode not available for line reversal."""
        raise NotImplementedError("ReverseLines is not bidirectional")


# ============================================================================
# JSON/XML/YAML Formatting Transformers
# ============================================================================

class JsonBeautify(TransformerInterface):
    """Format JSON with pretty printing (indent=2)."""

    name = "json_beautify"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Format JSON with 2-space indentation.

        Args:
            text: Input JSON string

        Returns:
            Pretty-printed JSON string

        Raises:
            json.JSONDecodeError: If input is not valid JSON
        """
        if not text:
            return ""

        data = json.loads(text)
        return json.dumps(data, indent=2, ensure_ascii=False)

    def decode(self, text: str) -> str:
        """Decode not available for JSON beautification."""
        raise NotImplementedError("JsonBeautify is not bidirectional")


class JsonMinify(TransformerInterface):
    """Minify JSON by removing whitespace."""

    name = "json_minify"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Minify JSON by removing unnecessary whitespace.

        Args:
            text: Input JSON string

        Returns:
            Minified JSON string

        Raises:
            json.JSONDecodeError: If input is not valid JSON
        """
        if not text:
            return ""

        data = json.loads(text)
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)

    def decode(self, text: str) -> str:
        """Decode not available for JSON minification."""
        raise NotImplementedError("JsonMinify is not bidirectional")


class XmlBeautify(TransformerInterface):
    """Format XML with pretty printing."""

    name = "xml_beautify"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Format XML with proper indentation.

        Args:
            text: Input XML string

        Returns:
            Pretty-printed XML string

        Raises:
            ET.ParseError: If input is not valid XML
        """
        if not text:
            return ""

        # Parse XML
        root = ET.fromstring(text)

        # Pretty print using ElementTree
        # We need to manually add indentation
        self._indent(root)

        # Convert back to string
        # Using tostring with method='xml' for proper XML formatting
        result = ET.tostring(root, encoding='unicode')

        # Add XML declaration if it was in the original
        if text.startswith('<?xml'):
            # Extract encoding from original or default to UTF-8
            declaration_match = re.match(r'<\?xml[^?]*\?>', text)
            if declaration_match:
                result = declaration_match.group() + '\n' + result

        return result

    def _indent(self, elem, level=0, indent='  '):
        """Add indentation to XML element."""
        i = "\n" + level * indent
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + indent
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self._indent(child, level + 1, indent)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def decode(self, text: str) -> str:
        """Decode not available for XML beautification."""
        raise NotImplementedError("XmlBeautify is not bidirectional")


class XmlMinify(TransformerInterface):
    """Minify XML by removing whitespace."""

    name = "xml_minify"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Minify XML by removing unnecessary whitespace.

        Args:
            text: Input XML string

        Returns:
            Minified XML string

        Raises:
            ET.ParseError: If input is not valid XML
        """
        if not text:
            return ""

        # Parse XML
        root = ET.fromstring(text)

        # Minify by removing all text/tail whitespace between elements
        self._minify_element(root)

        # Convert back to string without pretty printing
        result = ET.tostring(root, encoding='unicode', method='xml')

        # Preserve XML declaration if present
        if text.startswith('<?xml'):
            declaration_match = re.match(r'<\?xml[^?]*\?>', text)
            if declaration_match:
                result = declaration_match.group() + result

        return result

    def _minify_element(self, elem):
        """Remove whitespace from element and its children."""
        # Remove text whitespace between elements
        if elem.text and not elem.text.strip():
            elem.text = None
        elif elem.text:
            elem.text = elem.text.strip()

        if elem.tail and not elem.tail.strip():
            elem.tail = None
        elif elem.tail:
            elem.tail = elem.tail.strip()

        # Process children
        for child in elem:
            self._minify_element(child)

    def decode(self, text: str) -> str:
        """Decode not available for XML minification."""
        raise NotImplementedError("XmlMinify is not bidirectional")


class RemoveBOM(TransformerInterface):
    """Remove BOM (Byte Order Mark) from text."""

    name = "remove_bom"
    category = "text_processing"
    is_bidirectional = False

    # BOM character for UTF-8, UTF-16 LE, UTF-16 BE
    BOM_MARKS = [
        '\ufeff',  # UTF-8 BOM
        '\ufeff',  # UTF-16 LE BOM (same as UTF-8 when decoded)
    ]

    def encode(self, text: str) -> str:
        """
        Remove BOM from the beginning of text.

        Args:
            text: Input string

        Returns:
            String without BOM
        """
        # Remove UTF-8 BOM (Zero Width No-Break Space)
        if text.startswith('\ufeff'):
            return text[1:]

        # Also check for other potential BOM characters
        for bom in self.BOM_MARKS:
            if text.startswith(bom):
                return text[len(bom):]

        return text

    def decode(self, text: str) -> str:
        """Decode not available for BOM removal."""
        raise NotImplementedError("RemoveBOM is not bidirectional")


# ============================================================================
# Additional Case Conversion Transformers
# ============================================================================

class ToTitleCase(TransformerInterface):
    """Convert text to Title Case."""

    name = "to_title_case"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Convert text to Title Case (Each Word Capitalized)."""
        return text.title()

    def decode(self, text: str) -> str:
        raise NotImplementedError("ToTitleCase is not bidirectional")


class SwapCase(TransformerInterface):
    """Swap case of each character (alias for invert_case)."""

    name = "swap_case"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Swap case of each character."""
        return text.swapcase()

    def decode(self, text: str) -> str:
        raise NotImplementedError("SwapCase is not bidirectional")


# ============================================================================
# Text Manipulation Transformers
# ============================================================================

class ReverseText(TransformerInterface):
    """Reverse the entire text character by character."""

    name = "reverse_text"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Reverse the entire text."""
        return text[::-1]

    def decode(self, text: str) -> str:
        raise NotImplementedError("ReverseText is not bidirectional")


class ShuffleLines(TransformerInterface):
    """Shuffle lines randomly."""

    name = "shuffle_lines"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Shuffle lines randomly."""
        import random
        lines = text.split('\n')
        random.shuffle(lines)
        return '\n'.join(lines)

    def decode(self, text: str) -> str:
        raise NotImplementedError("ShuffleLines is not bidirectional")


# ============================================================================
# Text Analysis Transformers
# ============================================================================

class CountCharacters(TransformerInterface):
    """Count characters in text."""

    name = "count_characters"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Count characters."""
        count = len(text)
        return f"Character count: {count}"

    def decode(self, text: str) -> str:
        raise NotImplementedError("CountCharacters is not bidirectional")


class CountWords(TransformerInterface):
    """Count words in text."""

    name = "count_words"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Count words."""
        words = text.split()
        count = len(words)
        return f"Word count: {count}"

    def decode(self, text: str) -> str:
        raise NotImplementedError("CountWords is not bidirectional")


class CountLines(TransformerInterface):
    """Count lines in text."""

    name = "count_lines"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Count lines."""
        lines = text.splitlines()
        count = len(lines)
        return f"Line count: {count}"

    def decode(self, text: str) -> str:
        raise NotImplementedError("CountLines is not bidirectional")


class NumberLines(TransformerInterface):
    """Add line numbers to text."""

    name = "number_lines"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Add line numbers."""
        lines = text.splitlines()
        numbered = [f"{i+1}: {line}" for i, line in enumerate(lines)]
        return '\n'.join(numbered)

    def decode(self, text: str) -> str:
        raise NotImplementedError("NumberLines is not bidirectional")


# ============================================================================
# Text Filtering Transformers
# ============================================================================

class RemoveNumbers(TransformerInterface):
    """Remove all numbers from text."""

    name = "remove_numbers"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Remove all numbers."""
        return re.sub(r'\d+', '', text)

    def decode(self, text: str) -> str:
        raise NotImplementedError("RemoveNumbers is not bidirectional")


class RemovePunctuation(TransformerInterface):
    """Remove punctuation from text."""

    name = "remove_punctuation"
    category = "text_processing"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Remove punctuation."""
        import string
        return text.translate(str.maketrans('', '', string.punctuation))

    def decode(self, text: str) -> str:
        raise NotImplementedError("RemovePunctuation is not bidirectional")
