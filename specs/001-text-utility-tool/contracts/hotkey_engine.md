# Hotkey Engine Contract

**Version**: 1.0
**Date**: 2026-01-21

## Overview

글로벌 핫키(Hotkey) 엔진의 API 계약서입니다.

---

## Class Definition

```python
from typing import Callable, Optional
from pynput import keyboard
from PySide6.QtCore import QObject, Signal

class HotkeyEngine(QObject):
    """글로벌 핫키 관리 엔진"""

    # Signal: 핫키 눌릴 때
    hotkey_pressed = Signal()  # 인자 없음

    # Signal: 핫키 해제될 때 (선택 사항)
    hotkey_released = Signal()

    def __new__(cls):
        """싱글톤 패턴"""
        if not hasattr(cls, '_instance'):
            cls._instance = super(HotkeyEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self._hotkey: str = "Ctrl+."  # 기본 핫키
        self._listener: Optional[keyboard.Listener] = None
        self._is_running: bool = False

    def start(self) -> None:
        """
        핫키 리스너 시작 (백그라운드 스레드)

        Raises:
            RuntimeError: 이미 실행 중인 경우
        """
        if self._is_running:
            raise RuntimeError("핫키 리스너가 이미 실행 중입니다")

        # pynput 포맷으로 변환
        pynput_hotkey = self._to_pynput_format(self._hotkey)

        def on_activate():
            """핫키 핸들러"""
            self.hotkey_pressed.emit()

        # 리스너 시작 (백그라운드 스레드)
        self._listener = keyboard.GlobalHotKeys({
            pynput_hotkey: on_activate
        })

        self._listener.start()
        self._is_running = True

    def stop(self) -> None:
        """
        핫키 리스너 중지

        Raises:
            RuntimeError: 실행 중이 아닌 경우
        """
        if not self._is_running:
            raise RuntimeError("핫키 리스너가 실행 중이 아닙니다")

        if self._listener:
            self._listener.stop()
            self._listener = None

        self._is_running = False

    def set_hotkey(self, hotkey: str) -> None:
        """
        핫키 변경

        Args:
            hotkey: 새 핫키 (예: "Ctrl+Shift+T")

        Raises:
            ValueError: 핫키가 유효하지 않은 경우

        Note:
            실행 중인 경우 리스너를 재시작해야 적용됨
        """
        if not self._is_valid_hotkey(hotkey):
            raise ValueError(f"유효하지 않은 핫키입니다: {hotkey}")

        was_running = self._is_running
        if was_running:
            self.stop()

        self._hotkey = hotkey

        if was_running:
            self.start()

    def get_hotkey(self) -> str:
        """현재 핫키 반환"""
        return self._hotkey

    def _to_pynput_format(self, hotkey: str) -> str:
        """
        "Ctrl+." → "<ctrl>+<period>" 변환

        Args:
            hotkey: 사람이 읽는 형식 (예: "Ctrl+.")

        Returns:
            str: pynput 포맷 (예: "<ctrl>+<period>")
        """
        parts = hotkey.lower().split("+")
        modifiers = {"ctrl", "alt", "shift", "cmd"}
        result = []
        for part in parts:
            if part in modifiers:
                result.append(f"<{part}>")
            else:
                # 키 매핑
                key_map = {
                    ".": "period",
                    ",": "comma",
                    "-": "minus",
                    "=": "equal",
                    "+": "plus",
                }
                result.append(key_map.get(part, part))
        return "+".join(result)

    def _is_valid_hotkey(self, hotkey: str) -> bool:
        """
        핫키 유효성 검증

        Checks:
        1. 시스템 단축키와 충돌하지 않아야 함
        2. 형식이 올바라야 함 (Modifier+Key)

        Returns:
            bool: 유효하면 True
        """
        # 시스템 단축키 블록리스트
        blocked = {
            "Ctrl+C", "Ctrl+V", "Ctrl+X", "Ctrl+Z", "Ctrl+Y",
            "Ctrl+A", "Ctrl+S", "Ctrl+O", "Ctrl+N", "Ctrl+W",
            "Ctrl+F", "Ctrl+P", "Ctrl+Shift+Z"
        }

        return hotkey not in blocked
```

---

## Integration with MainWindow

```python
# src/ui/main_window.py

from PySide6.QtWidgets import QMainWindow
from src.hotkey.engine import HotkeyEngine

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._hotkey_engine = HotkeyEngine()
        self._setup_hotkey()

    def _setup_hotkey(self):
        """핫키 엔진 연결"""
        # Signal 연결
        self._hotkey_engine.hotkey_pressed.connect(self._toggle_visibility)

        # 리스너 시작
        self._hotkey_engine.start()

    def _toggle_visibility(self):
        """창 표시/숨김 토글"""
        if self.isVisible():
            self.hide()
            # 상태 보존
            self._app_state.preserved_input = self.input_area.toPlainText()
            self._app_state.preserved_output = self.output_area.toPlainText()
        else:
            self.show()
            self.raise_()
            self.activateWindow()
            # 상태 복원
            if self._app_state.preserved_input:
                self.input_area.setPlainText(self._app_state.preserved_input)
            if self._app_state.preserved_output:
                self.output_area.setPlainText(self._app_state.preserved_output)
```

---

## Thread Safety

- `start()`: 메인 스레드에서 호출 (Qt 메인 루프 전)
- `stop()`: 메인 스레드에서 호출 (앱 종료 시)
- `hotkey_pressed` Signal: 백그라운드에서 발생 → Qt가 자동으로 메인 스레드로 전달
- Qt Signal/Slot 메커니즘으로 스레드 세이프 보장

---

## Error Handling

```python
# 시스템 권한 문제
try:
    engine.start()
except PermissionError:
    QMessageBox.critical(
        None,
        "핫키 오류",
        "핫키를 등록할 권한이 없습니다.\n"
        "관리자 권한으로 실행하거나 보안 소프트웨어를 확인해 주세요."
    )

# 핫키 충돌 (실제 사용 시 감지 필요)
def on_activate():
    try:
        engine.hotkey_pressed.emit()
    except Exception as e:
        logger.error(f"핫키 실행 오류: {e}")
```
