"""
Sidebar widget - Algorithm categories and search.

Features:
- Search bar with debouncing
- Category selection via ComboBox
- Algorithm list (filtered by category and search)
- Visual selection highlight
"""

import customtkinter as ctk
from typing import Optional, Callable, List
from registry import AlgorithmRegistry


class Sidebar(ctk.CTkFrame):
    """
    Sidebar widget with search and algorithm list.

    Callbacks:
        algorithm_selected: Called when user selects an algorithm
    """

    # Categories
    CATEGORIES = [
        "All",
        "Encoding",
        "Hashing",
        "Text_Processing",  # Changed from "Text Processing" to match algorithm category
        "Special",
        "Ciphers"
    ]

    def __init__(self, parent=None, **kwargs):
        """
        Initialize sidebar.

        Args:
            parent: Parent widget
            **kwargs: Additional arguments for CTkFrame
        """
        super().__init__(parent, **kwargs)

        # Callbacks
        self._on_algorithm_selected: Optional[Callable] = None

        # State
        self._current_category = "All"
        self._registry = AlgorithmRegistry()
        self._search_timer = None
        self._selected_algorithm = None  # Currently selected algorithm
        self._selected_line_number = None  # Currently selected line number

        # Cache deduplicated algorithms
        self._all_deduplicated = self._deduplicate_algorithms(self._registry.get_all())

        self._setup_ui()

        # Initialize with all algorithms
        self._perform_search()

    def _setup_ui(self):
        """Setup sidebar UI components."""
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Search label
        self.grid_rowconfigure(1, weight=0)  # Search entry
        self.grid_rowconfigure(2, weight=0)  # Category label
        self.grid_rowconfigure(3, weight=0)  # Category combo
        self.grid_rowconfigure(4, weight=0)  # Algorithm list label
        self.grid_rowconfigure(5, weight=1)  # Algorithm listbox + scrollbar

        # Search section
        search_label = ctk.CTkLabel(
            self,
            text="Search:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        search_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Search algorithms..."
        )
        self.search_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.search_entry.bind("<KeyRelease>", self._on_search_text_changed)

        # Category section
        category_label = ctk.CTkLabel(
            self,
            text="Category:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        category_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")

        self.category_combo = ctk.CTkComboBox(
            self,
            values=self.CATEGORIES,
            command=self._on_category_changed,
            dropdown_fg_color="gray20",
            dropdown_hover_color="gray25"
        )
        self.category_combo.set("All")
        self.category_combo.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Algorithm list section
        algorithm_label = ctk.CTkLabel(
            self,
            text="Algorithms:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        algorithm_label.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="w")

        # Algorithm listbox with scrollbar
        listbox_frame = ctk.CTkFrame(self, fg_color="gray15")
        listbox_frame.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Create listbox
        self.algorithm_listbox = ctk.CTkTextbox(
            listbox_frame,
            wrap="none",
            activate_scrollbars=False
        )
        self.algorithm_listbox.pack(side="left", fill="both", expand=True)

        # Configure tags for highlighting
        self.algorithm_listbox.tag_config("selected", background="#1f6aa5", foreground="white")
        self.algorithm_listbox.tag_config("normal", background="gray15", foreground="white")

        # Make listbox read-only but clickable
        self.algorithm_listbox.configure(state="disabled")
        self.algorithm_listbox.bind("<Button-1>", self._on_listbox_clicked)

    def _deduplicate_algorithms(self, algorithms: List) -> List:
        """
        Remove encode/decode duplicates - show each algorithm only once.

        Internally stores both encoder and decoder for each base algorithm.

        Args:
            algorithms: List of all TransformerInterface instances

        Returns:
            Filtered list with unique algorithms (shown once per base name)
        """
        # Use a dict to store encoder/decoder pairs by base name
        algo_pairs = {}
        seen_non_pair = set()  # For algorithms without encode/decode suffix

        for transformer in algorithms:
            name = transformer.name

            # Check for _encode or _decode suffix (snake_case)
            if name.endswith("_encode") or name.endswith("_decode"):
                # Remove suffix to get base name
                if name.endswith("_encode"):
                    base_name = name[:-7]  # Remove "_encode"
                else:  # ends with "_decode"
                    base_name = name[:-7]  # Remove "_decode"

                # Store encoder/decoder pair
                if base_name not in algo_pairs:
                    algo_pairs[base_name] = {"encoder": None, "decoder": None}

                if name.endswith("_encode"):
                    algo_pairs[base_name]["encoder"] = transformer
                else:
                    algo_pairs[base_name]["decoder"] = transformer
            else:
                # Hashing, Text Processing, Special - track by full name
                if name not in seen_non_pair:
                    seen_non_pair.add(name)
                    algo_pairs[name] = {"encoder": transformer, "decoder": None}

        # Build result list - ONE transformer per base name
        result = []
        for base_name, pair in algo_pairs.items():
            if pair["encoder"]:
                result.append(pair["encoder"])
                # Store decoder reference on encoder
                if pair["decoder"]:
                    pair["encoder"].decoder_pair = pair["decoder"]
            elif pair["decoder"]:
                result.append(pair["decoder"])

        return result

    def _on_search_text_changed(self, event):
        """Handle search text change with debouncing."""
        # Cancel existing timer
        if self._search_timer:
            try:
                self.after_cancel(self._search_timer)
            except Exception:
                pass

        # Start new timer (150ms debounce)
        try:
            self._search_timer = self.after(150, self._perform_search)
        except Exception:
            pass

    def _perform_search(self):
        """Perform search after debounce timer expires."""
        search_text = self.search_entry.get()

        # Start with cached deduplicated list
        results = self._all_deduplicated

        # Apply search filter
        if search_text:
            search_lower = search_text.lower()
            results = [r for r in results if search_lower in r.name.lower()]

        # Apply category filter if set
        if self._current_category and self._current_category != "All":
            category_lower = self._current_category.lower()
            results = [r for r in results if r.category.lower() == category_lower]

        self._update_algorithm_list(results)

    def _on_category_changed(self, choice: str):
        """
        Handle category combo box change.

        Args:
            choice: Selected category
        """
        self._current_category = choice
        self._perform_search()

    def _get_display_name(self, name: str) -> str:
        """
        Get display name for algorithm (removes _encode/_decode suffix).

        Args:
            name: Original algorithm name

        Returns:
            Display name without suffix
        """
        # Remove _encode or _decode suffix for display
        if name.endswith("_encode"):
            return name[:-7]  # Remove "_encode"
        elif name.endswith("_decode"):
            return name[:-7]  # Remove "_decode"
        return name

    def _update_algorithm_list(self, algorithms: List):
        """
        Update algorithm list display.

        Args:
            algorithms: List of TransformerInterface instances
        """
        # Enable listbox for editing
        self.algorithm_listbox.configure(state="normal")
        self.algorithm_listbox.delete("1.0", "end")

        # Store algorithms for lookup
        self._algorithms = algorithms

        # Add each algorithm to listbox with clean display name
        for i, transformer in enumerate(algorithms):
            # Get clean display name (without _encode/_decode)
            display_name = self._get_display_name(transformer.name)
            line = f"{display_name}\n"
            self.algorithm_listbox.insert("end", line)

        # Re-apply selection if we still have the same algorithm
        if self._selected_algorithm and self._selected_algorithm in algorithms:
            line_num = algorithms.index(self._selected_algorithm) + 1
            self._highlight_line(line_num)
        else:
            self._selected_algorithm = None
            self._selected_line_number = None

        # Disable listbox (read-only but clickable)
        self.algorithm_listbox.configure(state="disabled")

    def _highlight_line(self, line_number: int):
        """
        Highlight a specific line to show selection.

        Args:
            line_number: Line number to highlight (1-indexed)
        """
        self.algorithm_listbox.configure(state="normal")

        # Clear previous highlighting
        start_index = "1.0"
        end_index = "end"
        self.algorithm_listbox.tag_remove("selected", start_index, end_index)

        # Apply new highlighting
        line_start = f"{line_number}.0"
        line_end = f"{line_number}.end"
        self.algorithm_listbox.tag_add("selected", line_start, line_end)

        self.algorithm_listbox.configure(state="disabled")

    def _on_listbox_clicked(self, event):
        """
        Handle algorithm listbox click.

        Args:
            event: Mouse event
        """
        # Get click position
        index = self.algorithm_listbox.index(f"@{event.x},{event.y}")
        line_number = int(index.split(".")[0])

        # Get corresponding algorithm
        if 1 <= line_number <= len(self._algorithms):
            transformer = self._algorithms[line_number - 1]

            # Update selection state
            self._selected_algorithm = transformer
            self._selected_line_number = line_number

            # Highlight the selected line
            self._highlight_line(line_number)

            # Trigger callback
            if self._on_algorithm_selected:
                self._on_algorithm_selected(transformer)

    def set_algorithms(self, algorithms: List):
        """
        Update algorithm list with provided transformers.

        Args:
            algorithms: List of TransformerInterface instances
        """
        self._update_algorithm_list(algorithms)

    def set_algorithm_selected_callback(self, callback: Callable):
        """
        Set callback for algorithm selection.

        Args:
            callback: Function to call when algorithm is selected
        """
        self._on_algorithm_selected = callback

    def get_current_category(self) -> str:
        """
        Get currently selected category.

        Returns:
            Category name
        """
        return self._current_category
