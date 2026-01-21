"""
ContentArea widget - Input/output fields and transformation buttons.

Features:
- Input text field with placeholder
- Separate Encode and Decode buttons
- Output text field (read-only)
- Copy to clipboard button
"""

import customtkinter as ctk
from typing import Optional, Callable
import pyperclip


class ContentArea(ctk.CTkFrame):
    """
    Content area with input/output fields.

    Callbacks:
        encode_clicked: Called when Encode button is clicked
        decode_clicked: Called when Decode button is clicked
    """

    PLACEHOLDER_TEXT = "Enter text to transform..."
    OUTPUT_PLACEHOLDER = "Result will appear here..."

    def __init__(self, parent=None, **kwargs):
        """
        Initialize content area.

        Args:
            parent: Parent widget
            **kwargs: Additional arguments for CTkFrame
        """
        super().__init__(parent, **kwargs)

        # Callbacks
        self._on_encode_clicked: Optional[Callable[[], None]] = None
        self._on_decode_clicked: Optional[Callable[[], None]] = None

        # Placeholder state
        self._input_has_placeholder = True

        self._setup_ui()

    def _setup_ui(self):
        """Setup content area UI components."""
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Input label
        self.grid_rowconfigure(1, weight=1)  # Input field
        self.grid_rowconfigure(2, weight=0)  # Button frame
        self.grid_rowconfigure(3, weight=0)  # Output label
        self.grid_rowconfigure(4, weight=1)  # Output field
        self.grid_rowconfigure(5, weight=0)  # Copy button

        # Input section
        input_label = ctk.CTkLabel(
            self,
            text="Input:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        input_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.input_field = ctk.CTkTextbox(self, height=150)
        self.input_field.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self._set_input_placeholder()

        # Bind focus events for placeholder
        self.input_field.bind("<FocusIn>", self._on_input_focus_in)
        self.input_field.bind("<FocusOut>", self._on_input_focus_out)

        # Button frame for Encode/Decode buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Encode button
        self.encode_button = ctk.CTkButton(
            button_frame,
            text="Encode",
            command=self._on_encode_button_clicked,
            height=40,
            fg_color="#1f6aa5",
            hover_color="#164d7a"
        )
        self.encode_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        # Decode button
        self.decode_button = ctk.CTkButton(
            button_frame,
            text="Decode",
            command=self._on_decode_button_clicked,
            height=40,
            fg_color="#d97706",
            hover_color="#b45309"
        )
        self.decode_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        # Output section
        output_label = ctk.CTkLabel(
            self,
            text="Output:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        output_label.grid(row=3, column=0, padx=10, pady=(0, 5), sticky="w")

        self.output_field = ctk.CTkTextbox(self, height=150)
        self.output_field.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self._set_output_placeholder()
        self.output_field.configure(state="disabled", fg_color="gray15")

        # Copy button
        self.copy_button = ctk.CTkButton(
            self,
            text="Copy to Clipboard",
            command=self._copy_to_clipboard,
            height=35
        )
        self.copy_button.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="ew")

    def _on_encode_button_clicked(self):
        """Handle Encode button click."""
        if self._on_encode_clicked:
            self._on_encode_clicked()

    def _on_decode_button_clicked(self):
        """Handle Decode button click."""
        if self._on_decode_clicked:
            self._on_decode_clicked()

    def _copy_to_clipboard(self):
        """Copy output text to clipboard."""
        text = self.get_output()
        if text:
            try:
                pyperclip.copy(text)
                # Visual feedback
                self.copy_button.configure(text="Copied!")
                self.after(1000, lambda: self.copy_button.configure(text="Copy to Clipboard"))
            except Exception as e:
                print(f"Failed to copy to clipboard: {e}")

    def get_input(self) -> str:
        """
        Get current input text.

        Returns:
            Input text from input field (excludes placeholder)
        """
        text = self.input_field.get("1.0", "end").strip()
        # Return empty string if it's just placeholder
        if text == self.PLACEHOLDER_TEXT:
            return ""
        return text

    def get_output(self) -> str:
        """
        Get current output text.

        Returns:
            Output text from output field (excludes placeholder)
        """
        text = self.output_field.get("1.0", "end").strip()
        # Return empty string if it's just placeholder
        if text == self.OUTPUT_PLACEHOLDER:
            return ""
        return text

    def set_output(self, text: str):
        """
        Update output field with transformed text.

        Args:
            text: Transformed text to display
        """
        self.output_field.configure(state="normal")
        self.output_field.delete("1.0", "end")
        self.output_field.insert("1.0", text)
        self.output_field.configure(state="disabled")

    def clear(self):
        """Clear both input and output fields."""
        self._set_input_placeholder()
        self._set_output_placeholder()

    def _set_input_placeholder(self):
        """Set placeholder text in input field."""
        self.input_field.configure(state="normal")
        self.input_field.delete("1.0", "end")
        self.input_field.insert("1.0", self.PLACEHOLDER_TEXT)
        self._input_has_placeholder = True

    def _set_output_placeholder(self):
        """Set placeholder text in output field."""
        self.output_field.configure(state="normal")
        self.output_field.delete("1.0", "end")
        self.output_field.insert("1.0", self.OUTPUT_PLACEHOLDER)
        self.output_field.configure(state="disabled")

    def _on_input_focus_in(self, event):
        """Handle input field focus in - clear placeholder."""
        if self._input_has_placeholder:
            self.input_field.configure(state="normal")
            self.input_field.delete("1.0", "end")
            self._input_has_placeholder = False

    def _on_input_focus_out(self, event):
        """Handle input field focus out - restore placeholder if empty."""
        text = self.input_field.get("1.0", "end").strip()
        if not text:
            self._set_input_placeholder()

    def set_current_algorithm(self, algorithm_name: str):
        """
        Update button text with current algorithm name.

        Args:
            algorithm_name: Name of selected algorithm
        """
        self.encode_button.configure(text=f"Encode ({algorithm_name})")
        self.decode_button.configure(text=f"Decode ({algorithm_name})")

    def set_processing_state(self, is_processing: bool):
        """
        Update button state during processing.

        Note: This no longer changes button text to preserve algorithm name.

        Args:
            is_processing: True if processing, False otherwise
        """
        # Don't disable buttons or change text - keep them active
        # This allows users to continue using the UI during processing
        pass

    def set_encode_callback(self, callback: Callable[[], None]):
        """
        Set callback for Encode button.

        Args:
            callback: Function to call when Encode is clicked
        """
        self._on_encode_clicked = callback

    def set_decode_callback(self, callback: Callable[[], None]):
        """
        Set callback for Decode button.

        Args:
            callback: Function to call when Decode is clicked
        """
        self._on_decode_clicked = callback
