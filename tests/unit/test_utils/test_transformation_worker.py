"""
Unit tests for TransformationWorker QThread.

Tests verify that:
1. TransformationWorker runs in background thread
2. encode() and decode() methods work correctly
3. Signals (started, finished, result, error) are emitted
4. Worker handles exceptions and emits error signal
5. UI thread is not blocked during transformation
"""

import pytest
from PySide6.QtCore import QThread
from PySide6.QtTest import QSignalSpy

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestTransformationWorker:
    """Test suite for TransformationWorker QThread."""

    def test_worker_is_qthread(self):
        """TransformationWorker inherits from QThread."""
        from utils.transformation_worker import TransformationWorker
        from PySide6.QtCore import QThread

        worker = TransformationWorker("test", None)
        assert isinstance(worker, QThread)

    def test_worker_accepts_text_and_transformer(self):
        """Worker can be initialized with text and transformer."""
        from utils.transformation_worker import TransformationWorker
        from transformers.base import TransformerInterface

        class MockTransformer(TransformerInterface):
            name = "mock"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return f"encoded:{text}"

            def decode(self, text: str) -> str:
                return text.replace("encoded:", "")

        transformer = MockTransformer()
        worker = TransformationWorker("hello", transformer)

        assert worker.text == "hello"
        assert worker.transformer == transformer

    def test_encode_emits_result_signal(self, qapp):
        """encode() emits result signal with transformed text."""
        from utils.transformation_worker import TransformationWorker
        from transformers.base import TransformerInterface

        class MockTransformer(TransformerInterface):
            name = "mock"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return f"encoded:{text}"

            def decode(self, text: str) -> str:
                return text

        transformer = MockTransformer()
        worker = TransformationWorker("test", transformer)

        result_spy = QSignalSpy(worker.result)
        finished_spy = QSignalSpy(worker.finished)

        worker.encode()
        worker.wait()  # Wait for thread to finish

        assert result_spy.count() == 1
        assert finished_spy.count() >= 1  # QThread emits finished, we may also emit it
        assert result_spy.at(0)[0] == "encoded:test"

    def test_decode_emits_result_signal(self, qapp):
        """decode() emits result signal with transformed text."""
        from utils.transformation_worker import TransformationWorker
        from transformers.base import TransformerInterface

        class MockTransformer(TransformerInterface):
            name = "mock"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return f"decoded:{text}"

        transformer = MockTransformer()
        worker = TransformationWorker("encoded:test", transformer)

        result_spy = QSignalSpy(worker.result)
        finished_spy = QSignalSpy(worker.finished)

        worker.decode()
        worker.wait()

        assert result_spy.count() == 1
        assert finished_spy.count() >= 1  # QThread emits finished, we may also emit it
        assert result_spy.at(0)[0] == "decoded:encoded:test"

    def test_exception_emits_error_signal(self, qapp):
        """Worker emits error signal when transformer raises exception."""
        from utils.transformation_worker import TransformationWorker
        from transformers.base import TransformerInterface

        class BrokenTransformer(TransformerInterface):
            name = "broken"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                raise ValueError("Intentional error")

            def decode(self, text: str) -> str:
                return text

        transformer = BrokenTransformer()
        worker = TransformationWorker("test", transformer)

        error_spy = QSignalSpy(worker.error)
        finished_spy = QSignalSpy(worker.finished)

        worker.encode()
        worker.wait()

        assert error_spy.count() == 1
        assert finished_spy.count() >= 1
        assert "Intentional error" in str(error_spy.at(0)[0])

    def test_worker_does_not_block_ui_thread(self, qapp):
        """Worker runs in background thread without blocking UI."""
        from utils.transformation_worker import TransformationWorker
        from transformers.base import TransformerInterface
        import time

        class SlowTransformer(TransformerInterface):
            name = "slow"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                time.sleep(0.1)  # Simulate slow operation
                return text

            def decode(self, text: str) -> str:
                return text

        transformer = SlowTransformer()
        worker = TransformationWorker("test", transformer)

        result_spy = QSignalSpy(worker.result)

        start_time = time.time()
        worker.encode()

        # Worker should return immediately (not block)
        elapsed = time.time() - start_time
        assert elapsed < 0.05  # Should be much less than 0.1s sleep

        # Wait for completion
        worker.wait()
        assert result_spy.count() == 1

    def test_started_signal_emitted(self, qapp):
        """Worker emits started signal when thread starts."""
        from utils.transformation_worker import TransformationWorker
        from transformers.base import TransformerInterface

        class QuickTransformer(TransformerInterface):
            name = "quick"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        transformer = QuickTransformer()
        worker = TransformationWorker("test", transformer)

        started_spy = QSignalSpy(worker.started)

        worker.encode()
        worker.wait()

        assert started_spy.count() == 1

    def test_mode_attribute(self):
        """Worker stores mode ('encode' or 'decode')."""
        from utils.transformation_worker import TransformationWorker
        from transformers.base import TransformerInterface

        class MockTransformer(TransformerInterface):
            name = "mock"
            category = "test"
            is_bidirectional = True

            def encode(self, text: str) -> str:
                return text

            def decode(self, text: str) -> str:
                return text

        transformer = MockTransformer()
        worker = TransformationWorker("test", transformer)

        assert worker.mode is None

        worker.encode()
        assert worker.mode == 'encode'

        worker2 = TransformationWorker("test", transformer)
        worker2.decode()
        assert worker2.mode == 'decode'
