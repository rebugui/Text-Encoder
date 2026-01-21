#!/usr/bin/env python3
"""
Integration test for UI components and transformation workflow.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QEventLoop, QTimer

from ui.main_window import MainWindow
from registry import AlgorithmRegistry
from transformers.encoding import Base64Encode


def test_sidebar_search():
    """Test sidebar search functionality."""
    from ui.sidebar import Sidebar

    # Register algorithms first
    _register_test_algorithms()

    app = QApplication.instance() or QApplication(sys.argv)
    sidebar = Sidebar()

    # Test initial load
    assert sidebar.algorithm_list.count() > 0, "Sidebar should load with algorithms"

    # Test search
    sidebar.search_field.setText("base64")
    # Wait for debounce timer
    loop = QEventLoop()
    QTimer.singleShot(200, loop.quit)
    loop.exec_()

    # Verify filtered results
    count = sidebar.algorithm_list.count()
    assert count > 0, "Search should return results"

    print("OK Sidebar search test passed")


def test_category_filter():
    """Test category filtering."""
    from ui.sidebar import Sidebar

    # Register algorithms first
    _register_test_algorithms()

    app = QApplication.instance() or QApplication(sys.argv)
    sidebar = Sidebar()

    # Get initial count
    initial_count = sidebar.algorithm_list.count()

    # Click a category button
    encoding_button = None
    for btn in sidebar.findChildren(QWidget):
        if btn.text() == "Encoding":
            encoding_button = btn
            break

    if encoding_button:
        encoding_button.click()
        # Wait for processing
        loop = QEventLoop()
        QTimer.singleShot(100, loop.quit)
        loop.exec_()

        # Verify filtering worked
        filtered_count = sidebar.algorithm_list.count()
        assert filtered_count <= initial_count, "Category filter should reduce count"

        print("OK Category filter test passed")


def test_algorithm_selection():
    """Test algorithm selection signal emission."""
    from ui.sidebar import Sidebar

    # Register algorithms first
    _register_test_algorithms()

    app = QApplication.instance() or QApplication(sys.argv)
    sidebar = Sidebar()

    # Track signal emissions
    selected_algorithm = [None]

    def on_selected(transformer):
        selected_algorithm[0] = transformer

    sidebar.algorithm_selected.connect(on_selected)

    # Click first item
    if sidebar.algorithm_list.count() > 0:
        sidebar.algorithm_list.item(0).setSelected(True)
        # Simulate click
        item = sidebar.algorithm_list.item(0)
        sidebar._on_algorithm_clicked(item)

        assert selected_algorithm[0] is not None, "Algorithm should be selected"

        print("OK Algorithm selection test passed")


def test_transformation_workflow():
    """Test complete transformation workflow."""
    # Register algorithms first
    _register_test_algorithms()

    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()

    # Select an algorithm
    registry = AlgorithmRegistry()
    base64_encoder = Base64Encode()
    window._on_algorithm_selected(base64_encoder)

    # Set input text
    test_text = "Hello, World!"
    window.content_area.input_field.setPlainText(test_text)

    # Trigger transformation
    result_received = [None]
    error_received = [None]

    def on_result(text):
        result_received[0] = text

    def on_error(error):
        error_received[0] = error

    # Mock the worker
    from utils.transformation_worker import TransformationWorker
    worker = TransformationWorker(test_text, base64_encoder)
    worker.result.connect(on_result)
    worker.error.connect(on_error)

    # Execute and wait with event processing
    worker.encode()

    # Process events while worker is running
    loop = QEventLoop()
    worker.finished.connect(loop.quit)
    loop.exec()

    assert error_received[0] is None, f"No error should occur: {error_received[0]}"
    assert result_received[0] is not None, "Result should be received"

    # Verify result
    expected = "SGVsbG8sIFdvcmxkIQ=="
    assert result_received[0] == expected, f"Expected {expected}, got {result_received[0]}"

    print("OK Transformation workflow test passed")


def _register_test_algorithms():
    """Register test algorithms in the registry."""
    registry = AlgorithmRegistry()
    if registry.get_all():
        return  # Already registered

    from transformers.encoding import (
        Base64Encode, Base64Decode,
        Base32Encode, Base32Decode,
        URLEncode, URLDecode,
        HexEncode, HexDecode
    )
    from transformers.hashing import (
        MD5Hash, SHA256Hash
    )
    from transformers.text_processing import (
        ToUpperCase, ToLowerCase
    )

    # Register a few test algorithms
    registry.register(Base64Encode())
    registry.register(Base64Decode())
    registry.register(Base32Encode())
    registry.register(Base32Decode())
    registry.register(URLEncode())
    registry.register(URLDecode())
    registry.register(HexEncode())
    registry.register(HexDecode())
    registry.register(MD5Hash())
    registry.register(SHA256Hash())
    registry.register(ToUpperCase())
    registry.register(ToLowerCase())


def main():
    """Run all integration tests."""
    print("Running UI integration tests...\n")

    try:
        test_sidebar_search()
        test_category_filter()
        test_algorithm_selection()
        test_transformation_workflow()

        print("\n[SUCCESS] All integration tests passed!")
        return 0
    except AssertionError as e:
        print(f"\n[FAILED] Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
