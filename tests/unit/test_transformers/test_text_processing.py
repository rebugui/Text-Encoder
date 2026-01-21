"""
Unit tests for text processing algorithms.

Tests verify that:
1. Case conversion transformers work correctly
2. Text cleaning transformers work correctly
3. JSON/XML formatting transformers work correctly
4. Edge cases (empty string, special characters, unicode)
"""

import pytest
import json

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


# ============================================================================
# Case Conversion Tests
# ============================================================================

class TestToUpperCase:
    """Test suite for ToUpperCase transformer."""

    def test_upper_case_simple_text(self):
        """ToUpperCase converts simple text to uppercase."""
        from transformers.text_processing import ToUpperCase

        transformer = ToUpperCase()
        result = transformer.encode("Hello World!")

        assert result == "HELLO WORLD!"

    def test_upper_case_empty_string(self):
        """ToUpperCase handles empty string."""
        from transformers.text_processing import ToUpperCase

        transformer = ToUpperCase()
        result = transformer.encode("")

        assert result == ""

    def test_upper_case_unicode(self):
        """ToUpperCase handles unicode characters."""
        from transformers.text_processing import ToUpperCase

        transformer = ToUpperCase()
        result = transformer.encode("café")

        assert result == "CAFÉ"

    def test_upper_case_attributes(self):
        """ToUpperCase has correct attributes."""
        from transformers.text_processing import ToUpperCase

        transformer = ToUpperCase()

        assert transformer.name == "to_upper_case"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False

    def test_upper_case_decode_raises_error(self):
        """ToUpperCase decode raises NotImplementedError."""
        from transformers.text_processing import ToUpperCase

        transformer = ToUpperCase()

        with pytest.raises(NotImplementedError):
            transformer.decode("test")


class TestToLowerCase:
    """Test suite for ToLowerCase transformer."""

    def test_lower_case_simple_text(self):
        """ToLowerCase converts simple text to lowercase."""
        from transformers.text_processing import ToLowerCase

        transformer = ToLowerCase()
        result = transformer.encode("HELLO WORLD!")

        assert result == "hello world!"

    def test_lower_case_empty_string(self):
        """ToLowerCase handles empty string."""
        from transformers.text_processing import ToLowerCase

        transformer = ToLowerCase()
        result = transformer.encode("")

        assert result == ""

    def test_lower_case_unicode(self):
        """ToLowerCase handles unicode characters."""
        from transformers.text_processing import ToLowerCase

        transformer = ToLowerCase()
        result = transformer.encode("CAFÉ")

        assert result == "café"

    def test_lower_case_attributes(self):
        """ToLowerCase has correct attributes."""
        from transformers.text_processing import ToLowerCase

        transformer = ToLowerCase()

        assert transformer.name == "to_lower_case"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestToCamelCase:
    """Test suite for ToCamelCase transformer."""

    def test_camel_case_from_snake(self):
        """ToCamelCase converts snake_case to camelCase."""
        from transformers.text_processing import ToCamelCase

        transformer = ToCamelCase()
        result = transformer.encode("hello_world_test")

        assert result == "helloWorldTest"

    def test_camel_case_from_kebab(self):
        """ToCamelCase converts kebab-case to camelCase."""
        from transformers.text_processing import ToCamelCase

        transformer = ToCamelCase()
        result = transformer.encode("hello-world-test")

        assert result == "helloWorldTest"

    def test_camel_case_from_spaces(self):
        """ToCamelCase converts space-separated to camelCase."""
        from transformers.text_processing import ToCamelCase

        transformer = ToCamelCase()
        result = transformer.encode("hello world test")

        assert result == "helloWorldTest"

    def test_camel_case_from_pascal(self):
        """ToCamelCase converts PascalCase to camelCase."""
        from transformers.text_processing import ToCamelCase

        transformer = ToCamelCase()
        result = transformer.encode("HelloWorldTest")

        assert result == "helloWorldTest"

    def test_camel_case_empty_string(self):
        """ToCamelCase handles empty string."""
        from transformers.text_processing import ToCamelCase

        transformer = ToCamelCase()
        result = transformer.encode("")

        assert result == ""

    def test_camel_case_attributes(self):
        """ToCamelCase has correct attributes."""
        from transformers.text_processing import ToCamelCase

        transformer = ToCamelCase()

        assert transformer.name == "to_camel_case"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestToSnakeCase:
    """Test suite for ToSnakeCase transformer."""

    def test_snake_case_from_camel(self):
        """ToSnakeCase converts camelCase to snake_case."""
        from transformers.text_processing import ToSnakeCase

        transformer = ToSnakeCase()
        result = transformer.encode("helloWorldTest")

        assert result == "hello_world_test"

    def test_snake_case_from_pascal(self):
        """ToSnakeCase converts PascalCase to snake_case."""
        from transformers.text_processing import ToSnakeCase

        transformer = ToSnakeCase()
        result = transformer.encode("HelloWorldTest")

        assert result == "hello_world_test"

    def test_snake_case_from_kebab(self):
        """ToSnakeCase converts kebab-case to snake_case."""
        from transformers.text_processing import ToSnakeCase

        transformer = ToSnakeCase()
        result = transformer.encode("hello-world-test")

        assert result == "hello_world_test"

    def test_snake_case_from_spaces(self):
        """ToSnakeCase converts space-separated to snake_case."""
        from transformers.text_processing import ToSnakeCase

        transformer = ToSnakeCase()
        result = transformer.encode("hello world test")

        assert result == "hello_world_test"

    def test_snake_case_empty_string(self):
        """ToSnakeCase handles empty string."""
        from transformers.text_processing import ToSnakeCase

        transformer = ToSnakeCase()
        result = transformer.encode("")

        assert result == ""

    def test_snake_case_attributes(self):
        """ToSnakeCase has correct attributes."""
        from transformers.text_processing import ToSnakeCase

        transformer = ToSnakeCase()

        assert transformer.name == "to_snake_case"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestToKebabCase:
    """Test suite for ToKebabCase transformer."""

    def test_kebab_case_from_camel(self):
        """ToKebabCase converts camelCase to kebab-case."""
        from transformers.text_processing import ToKebabCase

        transformer = ToKebabCase()
        result = transformer.encode("helloWorldTest")

        assert result == "hello-world-test"

    def test_kebab_case_from_pascal(self):
        """ToKebabCase converts PascalCase to kebab-case."""
        from transformers.text_processing import ToKebabCase

        transformer = ToKebabCase()
        result = transformer.encode("HelloWorldTest")

        assert result == "hello-world-test"

    def test_kebab_case_from_snake(self):
        """ToKebabCase converts snake_case to kebab-case."""
        from transformers.text_processing import ToKebabCase

        transformer = ToKebabCase()
        result = transformer.encode("hello_world_test")

        assert result == "hello-world-test"

    def test_kebab_case_from_spaces(self):
        """ToKebabCase converts space-separated to kebab-case."""
        from transformers.text_processing import ToKebabCase

        transformer = ToKebabCase()
        result = transformer.encode("hello world test")

        assert result == "hello-world-test"

    def test_kebab_case_empty_string(self):
        """ToKebabCase handles empty string."""
        from transformers.text_processing import ToKebabCase

        transformer = ToKebabCase()
        result = transformer.encode("")

        assert result == ""

    def test_kebab_case_attributes(self):
        """ToKebabCase has correct attributes."""
        from transformers.text_processing import ToKebabCase

        transformer = ToKebabCase()

        assert transformer.name == "to_kebab_case"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestToPascalCase:
    """Test suite for ToPascalCase transformer."""

    def test_pascal_case_from_camel(self):
        """ToPascalCase converts camelCase to PascalCase."""
        from transformers.text_processing import ToPascalCase

        transformer = ToPascalCase()
        result = transformer.encode("helloWorldTest")

        assert result == "HelloWorldTest"

    def test_pascal_case_from_snake(self):
        """ToPascalCase converts snake_case to PascalCase."""
        from transformers.text_processing import ToPascalCase

        transformer = ToPascalCase()
        result = transformer.encode("hello_world_test")

        assert result == "HelloWorldTest"

    def test_pascal_case_from_kebab(self):
        """ToPascalCase converts kebab-case to PascalCase."""
        from transformers.text_processing import ToPascalCase

        transformer = ToPascalCase()
        result = transformer.encode("hello-world-test")

        assert result == "HelloWorldTest"

    def test_pascal_case_from_spaces(self):
        """ToPascalCase converts space-separated to PascalCase."""
        from transformers.text_processing import ToPascalCase

        transformer = ToPascalCase()
        result = transformer.encode("hello world test")

        assert result == "HelloWorldTest"

    def test_pascal_case_empty_string(self):
        """ToPascalCase handles empty string."""
        from transformers.text_processing import ToPascalCase

        transformer = ToPascalCase()
        result = transformer.encode("")

        assert result == ""

    def test_pascal_case_attributes(self):
        """ToPascalCase has correct attributes."""
        from transformers.text_processing import ToPascalCase

        transformer = ToPascalCase()

        assert transformer.name == "to_pascal_case"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestInvertCase:
    """Test suite for InvertCase transformer."""

    def test_invert_case_mixed(self):
        """InvertCase inverts case of each character."""
        from transformers.text_processing import InvertCase

        transformer = InvertCase()
        result = transformer.encode("Hello World!")

        assert result == "hELLO wORLD!"

    def test_invert_case_all_upper(self):
        """InvertCase inverts all uppercase."""
        from transformers.text_processing import InvertCase

        transformer = InvertCase()
        result = transformer.encode("HELLO")

        assert result == "hello"

    def test_invert_case_all_lower(self):
        """InvertCase inverts all lowercase."""
        from transformers.text_processing import InvertCase

        transformer = InvertCase()
        result = transformer.encode("hello")

        assert result == "HELLO"

    def test_invert_case_empty_string(self):
        """InvertCase handles empty string."""
        from transformers.text_processing import InvertCase

        transformer = InvertCase()
        result = transformer.encode("")

        assert result == ""

    def test_invert_case_attributes(self):
        """InvertCase has correct attributes."""
        from transformers.text_processing import InvertCase

        transformer = InvertCase()

        assert transformer.name == "invert_case"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


# ============================================================================
# Text Cleaning Tests
# ============================================================================

class TestRemoveWhitespace:
    """Test suite for RemoveWhitespace transformer."""

    def test_remove_whitespace_all_types(self):
        """RemoveWhitespace removes all whitespace."""
        from transformers.text_processing import RemoveWhitespace

        transformer = RemoveWhitespace()
        result = transformer.encode("Hello   World\tTest\nNew Line")

        assert result == "HelloWorldTestNewLine"

    def test_remove_whitespace_empty_string(self):
        """RemoveWhitespace handles empty string."""
        from transformers.text_processing import RemoveWhitespace

        transformer = RemoveWhitespace()
        result = transformer.encode("")

        assert result == ""

    def test_remove_whitespace_attributes(self):
        """RemoveWhitespace has correct attributes."""
        from transformers.text_processing import RemoveWhitespace

        transformer = RemoveWhitespace()

        assert transformer.name == "remove_whitespace"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestRemoveExtraSpaces:
    """Test suite for RemoveExtraSpaces transformer."""

    def test_remove_extra_spaces_multiple_spaces(self):
        """RemoveExtraSpaces replaces multiple spaces with single."""
        from transformers.text_processing import RemoveExtraSpaces

        transformer = RemoveExtraSpaces()
        result = transformer.encode("Hello     World")

        assert result == "Hello World"

    def test_remove_extra_spaces_mixed_whitespace(self):
        """RemoveExtraSpaces normalizes all whitespace."""
        from transformers.text_processing import RemoveExtraSpaces

        transformer = RemoveExtraSpaces()
        result = transformer.encode("Hello\t\tWorld\n\nTest")

        assert result == "Hello World Test"

    def test_remove_extra_spaces_trimming(self):
        """RemoveExtraSpaces trims leading/trailing whitespace."""
        from transformers.text_processing import RemoveExtraSpaces

        transformer = RemoveExtraSpaces()
        result = transformer.encode("   Hello World   ")

        assert result == "Hello World"

    def test_remove_extra_spaces_empty_string(self):
        """RemoveExtraSpaces handles empty string."""
        from transformers.text_processing import RemoveExtraSpaces

        transformer = RemoveExtraSpaces()
        result = transformer.encode("")

        assert result == ""

    def test_remove_extra_spaces_attributes(self):
        """RemoveExtraSpaces has correct attributes."""
        from transformers.text_processing import RemoveExtraSpaces

        transformer = RemoveExtraSpaces()

        assert transformer.name == "remove_extra_spaces"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestTrimLines:
    """Test suite for TrimLines transformer."""

    def test_trim_lines_indented(self):
        """TrimLines removes leading/trailing space from each line."""
        from transformers.text_processing import TrimLines

        transformer = TrimLines()
        result = transformer.encode("  Line 1  \n  Line 2  \n  Line 3  ")

        assert result == "Line 1\nLine 2\nLine 3"

    def test_trim_lines_mixed_indentation(self):
        """TrimLines handles mixed indentation."""
        from transformers.text_processing import TrimLines

        transformer = TrimLines()
        result = transformer.encode("\t  Line 1  \n\t  Line 2  ")

        assert result == "Line 1\nLine 2"

    def test_trim_lines_empty_string(self):
        """TrimLines handles empty string."""
        from transformers.text_processing import TrimLines

        transformer = TrimLines()
        result = transformer.encode("")

        assert result == ""

    def test_trim_lines_attributes(self):
        """TrimLines has correct attributes."""
        from transformers.text_processing import TrimLines

        transformer = TrimLines()

        assert transformer.name == "trim_lines"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestRemoveDuplicates:
    """Test suite for RemoveDuplicates transformer."""

    def test_remove_duplicates_simple(self):
        """RemoveDuplicates removes duplicate lines."""
        from transformers.text_processing import RemoveDuplicates

        transformer = RemoveDuplicates()
        result = transformer.encode("Line 1\nLine 2\nLine 1\nLine 3\nLine 2")

        assert result == "Line 1\nLine 2\nLine 3"

    def test_remove_duplicates_preserves_order(self):
        """RemoveDuplicates preserves order of first occurrence."""
        from transformers.text_processing import RemoveDuplicates

        transformer = RemoveDuplicates()
        result = transformer.encode("Z\nA\nZ\nB\nA")

        assert result == "Z\nA\nB"

    def test_remove_duplicates_empty_string(self):
        """RemoveDuplicates handles empty string."""
        from transformers.text_processing import RemoveDuplicates

        transformer = RemoveDuplicates()
        result = transformer.encode("")

        assert result == ""

    def test_remove_duplicates_attributes(self):
        """RemoveDuplicates has correct attributes."""
        from transformers.text_processing import RemoveDuplicates

        transformer = RemoveDuplicates()

        assert transformer.name == "remove_duplicates"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestSortLines:
    """Test suite for SortLines transformer."""

    def test_sort_lines_alphabetical(self):
        """SortLines sorts lines alphabetically."""
        from transformers.text_processing import SortLines

        transformer = SortLines()
        result = transformer.encode("Zebra\nApple\nBanana")

        assert result == "Apple\nBanana\nZebra"

    def test_sort_lines_numeric(self):
        """SortLines sorts numeric strings."""
        from transformers.text_processing import SortLines

        transformer = SortLines()
        result = transformer.encode("3\n1\n2")

        assert result == "1\n2\n3"

    def test_sort_lines_empty_string(self):
        """SortLines handles empty string."""
        from transformers.text_processing import SortLines

        transformer = SortLines()
        result = transformer.encode("")

        assert result == ""

    def test_sort_lines_attributes(self):
        """SortLines has correct attributes."""
        from transformers.text_processing import SortLines

        transformer = SortLines()

        assert transformer.name == "sort_lines"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestReverseLines:
    """Test suite for ReverseLines transformer."""

    def test_reverse_lines_simple(self):
        """ReverseLines reverses line order."""
        from transformers.text_processing import ReverseLines

        transformer = ReverseLines()
        result = transformer.encode("Line 1\nLine 2\nLine 3")

        assert result == "Line 3\nLine 2\nLine 1"

    def test_reverse_lines_single(self):
        """ReverseLines handles single line."""
        from transformers.text_processing import ReverseLines

        transformer = ReverseLines()
        result = transformer.encode("Single Line")

        assert result == "Single Line"

    def test_reverse_lines_empty_string(self):
        """ReverseLines handles empty string."""
        from transformers.text_processing import ReverseLines

        transformer = ReverseLines()
        result = transformer.encode("")

        assert result == ""

    def test_reverse_lines_attributes(self):
        """ReverseLines has correct attributes."""
        from transformers.text_processing import ReverseLines

        transformer = ReverseLines()

        assert transformer.name == "reverse_lines"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


# ============================================================================
# JSON/XML Formatting Tests
# ============================================================================

class TestJsonBeautify:
    """Test suite for JsonBeautify transformer."""

    def test_json_beautify_simple(self):
        """JsonBeautify formats JSON with 2-space indent."""
        from transformers.text_processing import JsonBeautify

        transformer = JsonBeautify()
        result = transformer.encode('{"name":"John","age":30}')

        expected = '{\n  "name": "John",\n  "age": 30\n}'
        assert result == expected

    def test_json_beautify_nested(self):
        """JsonBeautify formats nested JSON."""
        from transformers.text_processing import JsonBeautify

        transformer = JsonBeautify()
        result = transformer.encode('{"user":{"name":"John","age":30}}')

        expected = '{\n  "user": {\n    "name": "John",\n    "age": 30\n  }\n}'
        assert result == expected

    def test_json_beautify_unicode(self):
        """JsonBeautify handles unicode characters."""
        from transformers.text_processing import JsonBeautify

        transformer = JsonBeautify()
        result = transformer.encode('{"message":"안녕하세요"}')

        expected = '{\n  "message": "안녕하세요"\n}'
        assert result == expected

    def test_json_beautify_empty_string(self):
        """JsonBeautify handles empty string."""
        from transformers.text_processing import JsonBeautify

        transformer = JsonBeautify()
        result = transformer.encode("")

        assert result == ""

    def test_json_beautify_invalid_json_raises_error(self):
        """JsonBeautify raises error for invalid JSON."""
        from transformers.text_processing import JsonBeautify

        transformer = JsonBeautify()

        with pytest.raises(json.JSONDecodeError):
            transformer.encode("Not valid JSON!")

    def test_json_beautify_attributes(self):
        """JsonBeautify has correct attributes."""
        from transformers.text_processing import JsonBeautify

        transformer = JsonBeautify()

        assert transformer.name == "json_beautify"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestJsonMinify:
    """Test suite for JsonMinify transformer."""

    def test_json_minify_simple(self):
        """JsonMinify removes whitespace from JSON."""
        from transformers.text_processing import JsonMinify

        transformer = JsonMinify()
        result = transformer.encode('{\n  "name": "John",\n  "age": 30\n}')

        expected = '{"name":"John","age":30}'
        assert result == expected

    def test_json_minify_nested(self):
        """JsonMinify minifies nested JSON."""
        from transformers.text_processing import JsonMinify

        transformer = JsonMinify()
        result = transformer.encode('{\n  "user": {\n    "name": "John",\n    "age": 30\n  }\n}')

        expected = '{"user":{"name":"John","age":30}}'
        assert result == expected

    def test_json_minify_empty_string(self):
        """JsonMinify handles empty string."""
        from transformers.text_processing import JsonMinify

        transformer = JsonMinify()
        result = transformer.encode("")

        assert result == ""

    def test_json_minify_invalid_json_raises_error(self):
        """JsonMinify raises error for invalid JSON."""
        from transformers.text_processing import JsonMinify

        transformer = JsonMinify()

        with pytest.raises(json.JSONDecodeError):
            transformer.encode("Not valid JSON!")

    def test_json_minify_attributes(self):
        """JsonMinify has correct attributes."""
        from transformers.text_processing import JsonMinify

        transformer = JsonMinify()

        assert transformer.name == "json_minify"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestXmlBeautify:
    """Test suite for XmlBeautify transformer."""

    def test_xml_beautify_simple(self):
        """XmlBeautify formats XML with proper indentation."""
        from transformers.text_processing import XmlBeautify

        transformer = XmlBeautify()
        result = transformer.encode('<?xml version="1.0"?><root><child>text</child></root>')

        # Check that it's formatted with newlines and indentation
        assert "<root>" in result
        assert "<child>" in result
        assert "text" in result
        assert "\n" in result  # Has newlines for formatting

    def test_xml_beautify_nested(self):
        """XmlBeautify formats nested XML."""
        from transformers.text_processing import XmlBeautify

        transformer = XmlBeautify()
        result = transformer.encode('<root><parent><child>value</child></parent></root>')

        assert "<root>" in result
        assert "<parent>" in result
        assert "<child>" in result
        assert "value" in result

    def test_xml_beautify_empty_string(self):
        """XmlBeautify handles empty string."""
        from transformers.text_processing import XmlBeautify

        transformer = XmlBeautify()
        result = transformer.encode("")

        assert result == ""

    def test_xml_beautify_attributes(self):
        """XmlBeautify has correct attributes."""
        from transformers.text_processing import XmlBeautify

        transformer = XmlBeautify()

        assert transformer.name == "xml_beautify"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestXmlMinify:
    """Test suite for XmlMinify transformer."""

    def test_xml_minify_simple(self):
        """XmlMinify removes whitespace from XML."""
        from transformers.text_processing import XmlMinify

        transformer = XmlMinify()
        result = transformer.encode('<?xml version="1.0"?>\n<root>\n  <child>text</child>\n</root>')

        # Check that whitespace is removed but structure preserved
        assert "<?xml version=" in result
        assert "<root>" in result
        assert "<child>" in result
        assert "text" in result
        # Should have minimal whitespace
        assert result.count("\n") == 0 or result.count("\n") == 1

    def test_xml_minify_nested(self):
        """XmlMinify minifies nested XML."""
        from transformers.text_processing import XmlMinify

        transformer = XmlMinify()
        result = transformer.encode('<root>\n  <parent>\n    <child>value</child>\n  </parent>\n</root>')

        assert "<root>" in result
        assert "<parent>" in result
        assert "<child>" in result
        assert "value" in result

    def test_xml_minify_empty_string(self):
        """XmlMinify handles empty string."""
        from transformers.text_processing import XmlMinify

        transformer = XmlMinify()
        result = transformer.encode("")

        assert result == ""

    def test_xml_minify_attributes(self):
        """XmlMinify has correct attributes."""
        from transformers.text_processing import XmlMinify

        transformer = XmlMinify()

        assert transformer.name == "xml_minify"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False


class TestRemoveBOM:
    """Test suite for RemoveBOM transformer."""

    def test_remove_bom_utf8(self):
        """RemoveBOM removes UTF-8 BOM."""
        from transformers.text_processing import RemoveBOM

        transformer = RemoveBOM()
        text_with_bom = '\ufeffHello World'
        result = transformer.encode(text_with_bom)

        assert result == "Hello World"
        assert not result.startswith('\ufeff')

    def test_remove_bom_no_bom(self):
        """RemoveBOM preserves text without BOM."""
        from transformers.text_processing import RemoveBOM

        transformer = RemoveBOM()
        text_without_bom = "Hello World"
        result = transformer.encode(text_without_bom)

        assert result == "Hello World"

    def test_remove_bom_empty_string(self):
        """RemoveBOM handles empty string."""
        from transformers.text_processing import RemoveBOM

        transformer = RemoveBOM()
        result = transformer.encode("")

        assert result == ""

    def test_remove_bom_attributes(self):
        """RemoveBOM has correct attributes."""
        from transformers.text_processing import RemoveBOM

        transformer = RemoveBOM()

        assert transformer.name == "remove_bom"
        assert transformer.category == "text_processing"
        assert transformer.is_bidirectional is False
