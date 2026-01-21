"""
Special format transformers.

JWT, HTML entities, CSV, Markdown formatting.
"""

import re
import json
import base64
import html
import csv
from io import StringIO
from typing import List
from transformers.base import TransformerInterface


class JWTDecode(TransformerInterface):
    """Decode JWT (JSON Web Token) payload."""

    name = "jwt_decode"
    category = "Special"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Decode JWT and show payload.

        Note: This only decodes the payload, doesn't verify signature.
        """
        try:
            # Remove 'Bearer ' prefix if present
            text = text.replace('Bearer ', '').strip()

            # JWT has 3 parts separated by dots
            parts = text.split('.')
            if len(parts) != 3:
                return "Invalid JWT format: JWT must have 3 parts separated by dots"

            # Decode header
            header = parts[0]
            # Add padding if needed
            header += '=' * (4 - len(header) % 4) if len(header) % 4 else ''
            try:
                header_decoded = base64.urlsafe_b64decode(header).decode('utf-8')
                header_json = json.loads(header_decoded)
            except Exception:
                header_json = {"error": "Failed to decode header"}

            # Decode payload
            payload = parts[1]
            payload += '=' * (4 - len(payload) % 4) if len(payload) % 4 else ''
            try:
                payload_decoded = base64.urlsafe_b64decode(payload).decode('utf-8')
                payload_json = json.loads(payload_decoded)
            except Exception:
                payload_json = {"error": "Failed to decode payload"}

            # Format result
            result = "JWT Decoded:\n\n"
            result += "Header:\n" + json.dumps(header_json, indent=2)
            result += "\n\nPayload:\n" + json.dumps(payload_json, indent=2)
            result += "\n\nSignature: " + parts[2][:20] + "..."

            return result

        except Exception as e:
            return f"Error decoding JWT: {str(e)}"

    def decode(self, text: str) -> str:
        raise NotImplementedError("JWTDecode is not bidirectional")


class JWTEncode(TransformerInterface):
    """Create simple JWT (for educational purposes)."""

    name = "jwt_encode"
    category = "Special"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Create JWT from JSON text.

        Note: This creates unsigned JWT for educational purposes only.
        """
        try:
            # Try to parse as JSON
            payload = json.loads(text)

            # Create simple header
            header = {"alg": "none", "typ": "JWT"}

            # Encode header
            header_json = json.dumps(header, separators=(',', ':'))
            header_b64 = base64.urlsafe_b64encode(header_json.encode()).rstrip(b'=').decode()

            # Encode payload
            payload_json = json.dumps(payload, separators=(',', ':'))
            payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).rstrip(b'=').decode()

            # Create JWT (no signature for educational purposes)
            jwt = f"{header_b64}.{payload_b64}."

            return jwt

        except json.JSONDecodeError:
            return "Error: Input must be valid JSON"
        except Exception as e:
            return f"Error creating JWT: {str(e)}"

    def decode(self, text: str) -> str:
        raise NotImplementedError("JWTEncode is not bidirectional")


class HTMLEntityEncode(TransformerInterface):
    """Encode text to HTML entities."""

    name = "html_entity_encode"
    category = "Special"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Convert text to HTML entities."""
        return html.escape(text)

    def decode(self, text: str) -> str:
        raise NotImplementedError("HTMLEntityEncode is not bidirectional")


class HTMLEntityDecode(TransformerInterface):
    """Decode HTML entities."""

    name = "html_entity_decode"
    category = "Special"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Convert HTML entities back to text."""
        return html.unescape(text)

    def decode(self, text: str) -> str:
        raise NotImplementedError("HTMLEntityDecode is not bidirectional")


class CSVFormat(TransformerInterface):
    """Format text as CSV."""

    name = "csv_format"
    category = "Special"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Convert lines to CSV format.

        Each line becomes a row, tabs/spaces become column separators.
        """
        try:
            lines = text.splitlines()
            if not lines:
                return ""

            # Detect separator (tab first, then spaces)
            output = StringIO()
            writer = csv.writer(output)

            for line in lines:
                # Try to split by tab first
                if '\t' in line:
                    fields = line.split('\t')
                else:
                    # Split by multiple spaces
                    fields = re.split(r'\s{2,}', line.strip())

                writer.writerow(fields)

            return output.getvalue()

        except Exception as e:
            return f"Error formatting CSV: {str(e)}"

    def decode(self, text: str) -> str:
        raise NotImplementedError("CSVFormat is not bidirectional")


class CSVUnformat(TransformerInterface):
    """Convert CSV back to tab-separated text."""

    name = "csv_unformat"
    category = "Special"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Convert CSV to tab-separated format.
        """
        try:
            lines = text.splitlines()
            if not lines:
                return ""

            output = StringIO()
            reader = csv.reader(lines)

            for row in reader:
                output.write('\t'.join(row) + '\n')

            return output.getvalue()

        except Exception as e:
            return f"Error unformatting CSV: {str(e)}"

    def decode(self, text: str) -> str:
        raise NotImplementedError("CSVUnformat is not bidirectional")


class MarkdownTableEncode(TransformerInterface):
    """Convert CSV/TSV to Markdown table."""

    name = "markdown_table_encode"
    category = "Special"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """
        Convert tab-separated or CSV data to Markdown table.

        First row becomes header.
        """
        try:
            lines = text.strip().splitlines()
            if not lines:
                return ""

            # Parse data
            rows = []
            for line in lines:
                if '\t' in line:
                    rows.append(line.split('\t'))
                else:
                    # Try CSV
                    reader = csv.reader([line])
                    rows.append(next(reader))

            if not rows:
                return ""

            # Create Markdown table
            output = []

            # Header
            output.append('| ' + ' | '.join(rows[0]) + ' |')

            # Separator
            output.append('|' + '|'.join(['---'] * len(rows[0])) + '|')

            # Data rows
            for row in rows[1:]:
                output.append('| ' + ' | '.join(row) + ' |')

            return '\n'.join(output)

        except Exception as e:
            return f"Error creating Markdown table: {str(e)}"

    def decode(self, text: str) -> str:
        raise NotImplementedError("MarkdownTableEncode is not bidirectional")


class MarkdownBoldEncode(TransformerInterface):
    """Convert text to Markdown bold."""

    name = "markdown_bold_encode"
    category = "Special"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Wrap each line in Markdown bold (**text**)."""
        lines = text.splitlines()
        return '\n'.join(f"**{line}**" if line.strip() else line for line in lines)

    def decode(self, text: str) -> str:
        raise NotImplementedError("MarkdownBoldEncode is not bidirectional")


class MarkdownItalicEncode(TransformerInterface):
    """Convert text to Markdown italic."""

    name = "markdown_italic_encode"
    category = "Special"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Wrap each line in Markdown italic (*text*)."""
        lines = text.splitlines()
        return '\n'.join(f"*{line}*" if line.strip() else line for line in lines)

    def decode(self, text: str) -> str:
        raise NotImplementedError("MarkdownItalicEncode is not bidirectional")


class MarkdownCodeEncode(TransformerInterface):
    """Convert text to Markdown code block."""

    name = "markdown_code_encode"
    category = "Special"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Wrap text in Markdown code block."""
        return f"```\n{text}\n```"

    def decode(self, text: str) -> str:
        raise NotImplementedError("MarkdownCodeEncode is not bidirectional")


class MarkdownInlineCodeEncode(TransformerInterface):
    """Convert text to Markdown inline code."""

    name = "markdown_inline_code_encode"
    category = "Special"
    is_bidirectional = False

    def encode(self, text: str) -> str:
        """Wrap each line in Markdown inline code (`code`)."""
        lines = text.splitlines()
        return '\n'.join(f"`{line}`" if line.strip() else line for line in lines)

    def decode(self, text: str) -> str:
        raise NotImplementedError("MarkdownInlineCodeEncode is not bidirectional")
