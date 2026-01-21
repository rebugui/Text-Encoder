"""
TransformationWorker - Threading for background text transformation.

Runs text transformation algorithms in background thread to prevent UI blocking.
Uses callbacks instead of Qt signals for result and error handling.
"""

import threading
from typing import Callable, Optional


class TransformationWorker:
    """
    Worker thread for running text transformations.

    Callbacks:
        on_result(str): Called with transformed text on success
        on_error(Exception): Called if transformation raises exception
        on_finished(): Called when thread completes

    Usage:
        worker = TransformationWorker("hello world", transformer)
        worker.encode(
            on_result=lambda text: print(text),
            on_error=lambda exc: print(f"Error: {exc}")
        )
    """

    def __init__(self, text: str, transformer):
        """
        Initialize worker.

        Args:
            text: Input text to transform
            transformer: TransformerInterface instance
        """
        self.text = text
        self.transformer = transformer
        self.mode = None  # 'encode' or 'decode'
        self.thread = None

        # Callbacks
        self._on_result: Optional[Callable[[str], None]] = None
        self._on_error: Optional[Callable[[Exception], None]] = None
        self._on_finished: Optional[Callable[[], None]] = None

    def encode(
        self,
        on_result: Callable[[str], None] = None,
        on_error: Callable[[Exception], None] = None,
        on_finished: Callable[[], None] = None
    ):
        """
        Start encoding in background thread.

        Args:
            on_result: Callback with transformed text
            on_error: Callback with exception if error occurs
            on_finished: Callback when thread completes
        """
        self.mode = 'encode'
        self._on_result = on_result
        self._on_error = on_error
        self._on_finished = on_finished

        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def decode(
        self,
        on_result: Callable[[str], None] = None,
        on_error: Callable[[Exception], None] = None,
        on_finished: Callable[[], None] = None
    ):
        """
        Start decoding in background thread.

        Args:
            on_result: Callback with transformed text
            on_error: Callback with exception if error occurs
            on_finished: Callback when thread completes
        """
        self.mode = 'decode'
        self._on_result = on_result
        self._on_error = on_error
        self._on_finished = on_finished

        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        """
        Execute transformation in background thread.

        Automatically called by thread start.
        Calls callbacks on success or error.
        """
        try:
            if self.mode == 'encode':
                result = self.transformer.encode(self.text)
            elif self.mode == 'decode':
                result = self.transformer.decode(self.text)
            else:
                raise ValueError("Mode not set. Call encode() or decode() first.")

            # Call result callback on main thread
            if self._on_result:
                self._on_result(result)
        except Exception as e:
            # Call error callback on main thread
            if self._on_error:
                self._on_error(e)
        finally:
            # Call finished callback
            if self._on_finished:
                self._on_finished()

    def is_running(self) -> bool:
        """Check if worker thread is currently running."""
        return self.thread is not None and self.thread.is_alive()
