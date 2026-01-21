# Data Model

**Feature**: 확장형 GUI 텍스트 유틸리티 툴
**Date**: 2026-01-21
**Phase**: 1 - Design

## Overview

본 문서는 텍스트 유틸리티 툴의 핵심 데이터 모델과 상태 관리를 정의한다.

---

## 1. Core Entities

### 1.1 TransformationOperation

변환 작업의 실행 결과를 나타내는 엔티티.

```python
from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass

class OperationType(Enum):
    """작업 유형"""
    ENCODING = "encoding"
    DECODING = "decoding"
    HASH = "hash"
    TEXT_PROCESSING = "text_processing"
    CIPHER = "cipher"

@dataclass
class TransformationOperation:
    """변환 작업 결과"""
    operation_type: OperationType
    algorithm: str                    # 예: "Base64", "SHA-256", "ROT13"
    input_text: str                   # 사용자 입력
    output_text: Optional[str]        # 변환 결과 (성공 시)
    success: bool                     # 성공 여부
    error_message: Optional[str]      # 에러 메시지 (실패 시)
    options: Dict[str, any]           # 알고리즘별 옵션
        # Base64: {"padding": true}
        # Caesar Cipher: {"shift": 3}
        # Hash: {"salt": ""} (선택적)

    def to_dict(self) -> dict:
        """디버깅용 딕셔너리 변환"""
        return {
            "operation_type": self.operation_type.value,
            "algorithm": self.algorithm,
            "input_length": len(self.input_text),
            "output_length": len(self.output_text) if self.output_text else 0,
            "success": self.success,
            "error": self.error_message,
        }
```

### 1.2 ApplicationState

애플리케이션의 현재 상태를 관리하는 엔티티.

```python
from enum import Enum
from typing import Optional

class WindowVisibility(Enum):
    """창 가시성 상태"""
    VISIBLE = "visible"
    HIDDEN = "hidden"

class BackgroundState(Enum):
    """백그라운드 실행 상태"""
    RUNNING = "running"
    TERMINATED = "terminated"

@dataclass
class ApplicationState:
    """프로그램 전체 상태"""
    window_visibility: WindowVisibility
    background_state: BackgroundState
    current_transformation: Optional[str]  # 마지막 사용 알고리즘
    search_filter: str                    # 현재 검색어 (빈 문자열 = 미사용)
    preserved_input: str                  # 창 숨김 시 보존할 입력 텍스트
    preserved_output: str                 # 창 숨김 시 보존할 출력 텍스트
    hotkey_enabled: bool = True           # 핫키 활성화 여부

    def clear_preserved(self) -> None:
        """보존된 텍스트 초기화"""
        self.preserved_input = ""
        self.preserved_output = ""
```

### 1.3 UIComponents

UI 구성 요소의 정적 데이터.

```python
from typing import Dict, List

@dataclass
class UIComponents:
    """UI 구성 요소"""
    categories: List[str]  # 카테고리 순서
    algorithms: Dict[str, List[str]]  # {category: [algorithm names]}

    def __post_init__(self):
        """초기화"""
        if not self.categories:
            self.categories = [
                "Encoding",
                "Hash",
                "Text Processing",
                "Classical Ciphers"
            ]
        if not self.algorithms:
            self.algorithms = {
                "Encoding": [
                    "Base64", "URL", "Hex", "Base32", "Base58", "Base62",
                    "Base85", "HTML Entities", "Punycode", "Unicode Escape"
                ],
                "Hash": [
                    "MD5", "SHA-1", "SHA-256", "SHA-512", "SHA3-256",
                    "BLAKE2", "CRC32", "Adler32"
                ],
                "Text Processing": [
                    "JSON Beautify", "JSON Minify", "UPPERCASE", "lowercase",
                    "Remove Duplicates", "Sort Lines"
                ],
                "Classical Ciphers": [
                    "ROT13", "Caesar Cipher", "Vigenère Cipher", "Atbash"
                ]
            }

    def get_all_algorithms(self) -> List[str]:
        """모든 알고리즘 이름 플랫 리스트"""
        result = []
        for algorithms in self.algorithms.values():
            result.extend(algorithms)
        return result
```

### 1.4 HotkeyConfiguration

핫키 설정 엔티티.

```python
@dataclass
class HotkeyConfiguration:
    """핫키 설정"""
    key_combination: str  # 예: "Ctrl+.", "Ctrl+Shift+T"
    action: str           # "toggle_visibility"

    def is_valid(self) -> bool:
        """핫키 유효성 검증"""
        # 시스템 단축키와의 충돌 방지
        blocked = {
            "Ctrl+C", "Ctrl+V", "Ctrl+X", "Ctrl+Z", "Ctrl+Y",
            "Ctrl+A", "Ctrl+S", "Ctrl+O", "Ctrl+N", "Ctrl+W",
            "Ctrl+F", "Ctrl+P"
        }
        return self.key_combination not in blocked

    def to_pynput_format(self) -> str:
        """pynput 포맷으로 변환"""
        # "Ctrl+." -> "<ctrl>+<period>"
        parts = self.key_combination.lower().split("+")
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
                }
                result.append(key_map.get(part, part))
        return "+".join(result)
```

---

## 2. State Transitions

### 2.1 Window Visibility State Machine

```
[INITIAL] → VISIBLE (app start)
    ↓
VISIBLE ─(Ctrl+. or X button)─→ HIDDEN (to tray)
    ↓
HIDDEN ─(Ctrl+. or tray double-click)─→ VISIBLE
    ↓
HIDDEN ─(Exit menu)─→ TERMINATED
```

### 2.2 Transformation Execution Flow

```
[INPUT_TEXT]
    ↓
[SELECT_ALGORITHM]
    ↓
[VALIDATE_INPUT]
    ↓ (valid)
[EXECUTE_TRANSFORM]
    ↓ (success)     ↓ (failure)
[SHOW_RESULT]    [SHOW_ERROR]
```

---

## 3. Validation Rules

### 3.1 Input Validation

```python
def validate_transformation_input(
    algorithm: str,
    input_text: str,
    operation_type: OperationType
) -> tuple[bool, Optional[str]]:
    """
    입력 유효성 검증

    Returns:
        (is_valid, error_message)
    """
    # 빈 입력 체크
    if not input_text and operation_type != OperationType.HASH:
        return False, "입력 텍스트가 비어있습니다"

    # 길이 제한 (10,000자)
    if len(input_text) > 10000:
        return False, "입력 텍스트가 너무 깁니다 (최대 10,000자)"

    # 알고리즘별 검증
    if algorithm == "Morse Code" and not _is_morse_compatible(input_text):
        return False, "모스 부호로 변환할 수 없는 문자가 포함되어 있습니다"

    if operation_type == OperationType.DECODING:
        if algorithm == "Base64" and not _is_valid_base64(input_text):
            return False, "잘못된 Base64 형식입니다"

    return True, None
```

### 3.2 Algorithm Option Validation

```python
VALID_OPTIONS = {
    "Caesar Cipher": ["shift"],  # shift: int (1-25)
    "Base64": ["padding"],        # padding: bool
    "Hash": ["salt"],             # salt: str
}

def validate_algorithm_options(
    algorithm: str,
    options: Dict[str, any]
) -> tuple[bool, Optional[str]]:
    """
    알고리즘 옵션 유효성 검증

    Returns:
        (is_valid, error_message)
    """
    if algorithm not in VALID_OPTIONS:
        return True, None  # 옵션 없는 알고리즘

    valid_keys = VALID_OPTIONS[algorithm]
    for key in options:
        if key not in valid_keys:
            return False, f"잘못된 옵션입니다: {key}"

    # 타입 검증
    if "shift" in options:
        shift = options["shift"]
        if not isinstance(shift, int) or not (1 <= shift <= 25):
            return False, "shift는 1-25 사이 정수여야 합니다"

    return True, None
```

---

## 4. Data Flow

### 4.1 Transformation Flow

```
User Input (input_text)
    ↓
Sidebar Algorithm Selection
    ↓
Options Panel (optional parameters)
    ↓
[TransformationWorker Thread]
    ├─→ Validator.validate_input()
    ├─→ Transformer.transform()
    └─→ Result emitted via Qt Signal
    ↓
Output Area (result or error)
    ↓
Copy Button (to clipboard)
```

### 4.2 Search Flow

```
User types in search box
    ↓
[Debounce Timer: 150ms]
    ↓
Registry.search(query)
    ├─→ Filter algorithms by name/category
    └─→ Update sidebar tree view (highlight matches)
```

---

## 5. Persistence

### 5.1 User Configuration

**파일 경로** (플랫폼별):

```python
# Windows
# C:\Users\<Username>\.text-encoder\config.json
Path(Path.home() / '.text-encoder' / 'config.json')

# macOS
# /Users/<Username>/.text-encoder/config.json
Path(Path.home() / '.text-encoder' / 'config.json')

# Linux
# /home/<username>/.text-encoder/config.json
Path(Path.home() / '.text-encoder' / 'config.json')
```

**config.json 내용**:

```json
{
  "hotkey": "Ctrl+.",
  "window_position": {
    "x": 100,
    "y": 100,
    "width": 900,
    "height": 600
  },
  "last_category": "Encoding",
  "sidebar_expanded": true,
  "search_history": [],
  "platform": "auto-detected"  # "windows", "macos", "linux"
}
```

### 5.2 No Data Persistence

- 변환 작업 결과는 저장하지 않음 (stateless)
- 창 상태만 `ApplicationState`에 인메모리로 보존
- 프로그램 종료 시 모든 상태 소멸

---

## 6. Type Hints

```python
from typing import Protocol, Dict, List, Optional, Callable
from PySide6.QtCore import QObject, Signal

class TransformerInterface(Protocol):
    """모든 변환기가 구현해야 하는 프로토콜"""

    @property
    def name(self) -> str: ...

    @property
    def category(self) -> str: ...

    def transform(self, input_text: str, options: Optional[Dict[str, any]] = None) -> str:
        ...

    def validate_input(self, input_text: str) -> bool:
        ...

class AlgorithmRegistry:
    """알고리즘 등록 시스템"""

    def register(self, transformer: TransformerInterface) -> None: ...

    def get_by_category(self, category: str) -> List[TransformerInterface]: ...

    def search(self, query: str) -> List[TransformerInterface]: ...

    def get_by_name(self, name: str) -> Optional[TransformerInterface]: ...
```

---

## Summary

데이터 모델은 다음을 포함:
- **Core Entities**: `TransformationOperation`, `ApplicationState`, `UIComponents`, `HotkeyConfiguration`
- **State Machines**: Window visibility, transformation execution flow
- **Validation Rules**: Input validation, algorithm options validation
- **Data Flows**: Transformation, search
- **Persistence**: User config only (JSON file), stateless transformation results

이 모델은 Phase 2 구현 시 참조된다.
