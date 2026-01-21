"""
MainWindow - Main application window.

Features:
- Sidebar with algorithm categories and search
- Content area with input/output fields
- Separate Encode/Decode buttons
- System tray integration with minimize to tray
"""

import customtkinter as ctk
from pathlib import Path
from typing import Optional

from ui.sidebar import Sidebar
from ui.content_area import ContentArea
from ui.system_tray import SystemTray
from utils.transformation_worker import TransformationWorker
from registry import AlgorithmRegistry


class MainWindow(ctk.CTk):
    """
    Main application window for Text Encoder.

    Layout:
        - Left: Sidebar (categories, search, algorithm list)
        - Right: ContentArea (input field, encode/decode buttons, output field)
    """

    def __init__(self, system_tray: Optional[SystemTray] = None):
        """
        Initialize main window.

        Args:
            system_tray: Optional SystemTray instance
        """
        super().__init__()

        # Window setup
        self.title("Text Encoder")
        self.geometry("1000x600")

        # Set appearance mode
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        # Set window icon (try multiple methods for better compatibility)
        icon_path = self._get_window_icon_path()
        print(f"Icon path: {icon_path}, exists: {icon_path.exists() if icon_path else False}")
        if icon_path and icon_path.exists():
            self._set_window_icon(icon_path)
        else:
            print("Warning: Icon file not found, skipping window icon setup")

        # Current selected algorithms (encoder and decoder)
        self._current_encoder = None
        self._current_decoder = None
        self._worker: Optional[TransformationWorker] = None

        # Algorithm registry for finding encoder/decoder pairs
        self._registry = AlgorithmRegistry()

        # System tray integration
        self.system_tray = system_tray
        self._setup_system_tray()

        # Configure grid layout
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Content area
        self.grid_rowconfigure(0, weight=1)

        # Create UI components
        self._create_ui()

        # Setup close handler
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_system_tray(self):
        """Setup system tray integration."""
        if self.system_tray and self.system_tray.is_available():
            # Connect callbacks
            self.system_tray.set_show_callback(self._restore_from_tray)
            self.system_tray.set_info_callback(self._show_info_dialog)
            self.system_tray.set_exit_callback(self._exit_from_tray)

            # Create and show tray icon
            icon_path = self._get_icon_path()
            self.system_tray.create_icon(icon_path)
            self.system_tray.run_in_thread()

            # Show notification about tray functionality
            self.system_tray.show_message(
                "Text Encoder",
                "Application is running in the system tray. Click the icon to restore."
            )

    def _set_window_icon(self, icon_path: Path):
        """
        Set window icon using multiple methods for better Windows compatibility.

        Args:
            icon_path: Path to icon file
        """
        import sys

        # Convert to absolute path
        abs_icon_path = str(icon_path.absolute())
        print(f"Setting window icon (absolute): {abs_icon_path}")

        if sys.platform == "win32":
            try:
                # Method 1: iconbitmap with absolute path (standard method)
                self.iconbitmap(abs_icon_path)
                print(f"✓ iconbitmap() succeeded")

                # Method 2: wm_iconbitmap with absolute path
                try:
                    self.wm_iconbitmap(abs_icon_path)
                    print(f"✓ wm_iconbitmap() succeeded")
                except Exception as e:
                    print(f"✗ wm_iconbitmap() failed: {e}")

                # Method 3: Set again after window is fully initialized
                def set_icon_delayed():
                    try:
                        self.iconbitmap(abs_icon_path)
                        self.wm_iconbitmap(abs_icon_path)
                        print(f"✓ Delayed icon set succeeded")
                    except Exception as e:
                        print(f"✗ Delayed icon set failed: {e}")

                self.after(100, set_icon_delayed)

            except Exception as e:
                print(f"✗ Failed to set window icon: {e}")
        else:
            # For non-Windows platforms
            try:
                self.iconbitmap(abs_icon_path)
                print(f"✓ Icon set for non-Windows platform")
            except Exception as e:
                print(f"✗ Failed to set window icon: {e}")

    def _get_window_icon_path(self) -> Optional[Path]:
        """
        Get icon path for window title bar and taskbar.

        Returns:
            Path to icon file or None
        """
        # Get assets directory - try multiple methods
        import sys

        # Method 1: Relative to script location
        try:
            script_dir = Path(__file__).parent.parent.parent  # Go up from src/ui to project root
            icon_file = script_dir / "assets" / "icon.ico"
            if icon_file.exists():
                print(f"Found icon via script dir: {icon_file}")
                return icon_file
        except Exception as e:
            print(f"Method 1 failed: {e}")

        # Method 2: Current working directory
        try:
            cwd = Path.cwd()
            icon_file = cwd / "assets" / "icon.ico"
            if icon_file.exists():
                print(f"Found icon via CWD: {icon_file}")
                return icon_file
        except Exception as e:
            print(f"Method 2 failed: {e}")

        # Method 3: Relative to current directory
        try:
            icon_file = Path("assets/icon.ico")
            if icon_file.exists():
                print(f"Found icon via relative: {icon_file.absolute()}")
                return icon_file
        except Exception as e:
            print(f"Method 3 failed: {e}")

        print("Could not find icon.ico file")
        return None

    def _get_icon_path(self) -> Optional[Path]:
        """
        Get platform-specific icon path.

        Returns:
            Path to icon file or None
        """
        # Get assets directory
        if getattr(__import__('sys'), 'frozen', False):
            # Running as compiled executable
            assets_dir = Path(__import__('sys').executable).parent / "assets"
        else:
            # Running as script
            assets_dir = Path(__file__).parent.parent.parent / "assets"

        # Platform-specific icon file
        import sys
        if sys.platform == "win32":
            icon_file = assets_dir / "icon.ico"
        else:
            # macOS and Linux
            icon_file = assets_dir / "icon.png"

        return icon_file if icon_file.exists() else None

    def _create_ui(self):
        """Create UI components."""
        # Create sidebar
        self.sidebar = Sidebar(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Create content area
        self.content_area = ContentArea(self, corner_radius=0)
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        # Connect callbacks
        self.sidebar.set_algorithm_selected_callback(self._on_algorithm_selected)
        self.content_area.set_encode_callback(self._on_encode_clicked)
        self.content_area.set_decode_callback(self._on_decode_clicked)

    def _on_algorithm_selected(self, transformer):
        """
        Handle algorithm selection from sidebar.

        Args:
            transformer: Selected TransformerInterface instance
        """
        # Use the selected transformer as encoder
        self._current_encoder = transformer

        # Check if decoder_pair is stored on the transformer object
        if hasattr(transformer, 'decoder_pair') and transformer.decoder_pair:
            self._current_decoder = transformer.decoder_pair
        else:
            # Fallback: search registry for decoder
            name = transformer.name
            if name.endswith("_encode"):
                base_name = name[:-7]
            elif name.endswith("_decode"):
                base_name = name[:-7]
            else:
                base_name = name

            all_algos = self._registry.get_all()
            self._current_decoder = None
            for algo in all_algos:
                if algo.name == base_name + "_decode":
                    self._current_decoder = algo
                    break

            # For ciphers that are their own inverse, the transformer itself is both encoder and decoder
            if not self._current_decoder and transformer.is_bidirectional:
                self._current_decoder = transformer

            # Fallback: use selected transformer for both if no pair found
            if not self._current_decoder:
                self._current_decoder = transformer

        # Update content area button text with algorithm name (display name)
        name = transformer.name
        if name.endswith("_encode"):
            display_name = name[:-7]
        elif name.endswith("_decode"):
            display_name = name[:-7]
        else:
            display_name = name

        self.content_area.set_current_algorithm(display_name)

    def _on_encode_clicked(self):
        """Handle Encode button click - execute encoding."""
        if not self._current_encoder:
            self._show_error("No Algorithm Selected", "Please select an algorithm from the sidebar first.")
            return

        input_text = self.content_area.get_input()

        if not input_text or input_text == "Enter text to transform...":
            self._show_error("No Input", "Please enter some text to transform.")
            return

        # Create worker thread with encoder
        self._worker = TransformationWorker(input_text, self._current_encoder)
        self._worker.encode(
            on_result=self._on_transform_result,
            on_error=self._on_transform_error,
            on_finished=self._on_transform_finished
        )

    def _on_decode_clicked(self):
        """Handle Decode button click - execute decoding."""
        if not self._current_decoder:
            self._show_error("No Algorithm Selected", "Please select an algorithm from the sidebar first.")
            return

        input_text = self.content_area.get_input()

        if not input_text or input_text == "Enter text to transform...":
            self._show_error("No Input", "Please enter some text to transform.")
            return

        # Create worker thread with decoder
        self._worker = TransformationWorker(input_text, self._current_decoder)
        self._worker.decode(
            on_result=self._on_transform_result,
            on_error=self._on_transform_error,
            on_finished=self._on_transform_finished
        )

    def _on_transform_result(self, result_text: str):
        """
        Handle successful transformation result.

        Args:
            result_text: Transformed text
        """
        self.content_area.set_output(result_text)

    def _on_transform_error(self, error: Exception):
        """
        Handle transformation error.

        Args:
            error: Exception that occurred
        """
        self._show_error(
            "Transformation Error",
            f"An error occurred during transformation:\n\n{str(error)}"
        )

    def _on_transform_finished(self):
        """Handle transformation completion (re-enable buttons)."""
        self.content_area.set_processing_state(False)

    def _show_error(self, title: str, message: str):
        """
        Show error message dialog.

        Args:
            title: Dialog title
            message: Error message
        """
        # Create error dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.attributes('-topmost', True)

        # Center on parent
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - 400) // 2
        y = self.winfo_y() + (self.winfo_height() - 200) // 2
        dialog.geometry(f"400x200+{x}+{y}")

        # Add message label
        label = ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=350,
            justify="left"
        )
        label.pack(padx=20, pady=20, expand=True, fill="both")

        # Add OK button
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            width=100
        )
        ok_button.pack(pady=(0, 20))

    def set_output(self, text: str):
        """Update output field with transformed text."""
        self.content_area.set_output(text)

    def get_input(self) -> str:
        """Get current input text."""
        return self.content_area.get_input()

    def clear_fields(self):
        """Clear input and output fields."""
        self.content_area.clear()

    def _on_closing(self):
        """
        Handle window close event.

        Minimize to system tray instead of closing.
        """
        # If system tray is available, minimize to tray
        if self.system_tray and self.system_tray.is_available():
            self.withdraw()  # Hide the window
            # Show notification that app is still running
            self.system_tray.show_message(
                "Text Encoder",
                "Minimized to system tray. Click the tray icon to restore."
            )
        else:
            # No system tray, allow normal close
            self._exit_application()

    def _restore_from_tray(self):
        """Restore window from system tray."""
        self.deiconify()  # Show window
        self.lift()  # Bring to front
        self.focus()  # Give focus

    def _show_info_dialog(self):
        """Show about/info dialog from system tray."""
        # Create info dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("About Text Encoder")
        dialog.geometry("400x350")
        dialog.attributes('-topmost', True)

        # Center on parent
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - 400) // 2
        y = self.winfo_y() + (self.winfo_height() - 350) // 2
        dialog.geometry(f"400x350+{x}+{y}")

        # Main container
        container = ctk.CTkFrame(dialog, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            container,
            text="Text Encoder",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 10))

        # Description
        desc_label = ctk.CTkLabel(
            container,
            text="Extended GUI Text Utility Tool\nSupports 80+ transformation algorithms",
            font=ctk.CTkFont(size=12)
        )
        desc_label.pack(pady=(0, 20))

        # Info text
        info_text = f"""Version: 1.0.0
Platform: Cross-platform (Windows/macOS/Linux)

{SystemTray.COPYRIGHT_TEXT}"""

        info_label = ctk.CTkLabel(
            container,
            text=info_text,
            font=ctk.CTkFont(size=11),
            justify="left"
        )
        info_label.pack(pady=(0, 20), fill="both", expand=True)

        # OK button
        ok_button = ctk.CTkButton(
            container,
            text="OK",
            command=dialog.destroy,
            width=100
        )
        ok_button.pack(pady=(0, 10))

    def _exit_from_tray(self):
        """Handle exit request from system tray."""
        self._exit_application()

    def _exit_application(self):
        """Exit the application."""
        # Stop system tray
        if self.system_tray:
            self.system_tray.stop()
        # Destroy window
        self.destroy()
