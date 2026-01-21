# Transformer Interface Contract

**Version**: 1.0
**Date**: 2026-01-21

## Overview

모든 변환 알고리즘(Transformer)이 구현해야 하는 인터페이스 정의입니다.

---

## Interface Definition

```python
from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from enum import Enum

class OperationType(Enum):
    """작업 유형"""
    ENCODING = "encoding"
    DECODING = "decoding"
    HASH = "hash"
    TEXT_PROCESSING = "text_processing"
    CIPHER = "cipher"

class TransformerInterface(ABC):
    """모든 변환 알고리즘의 추상 인터페이스"""

    @property
    @abstractmethod
    def name(self) -> str:
        """
        알고리즘 이름 (사용자에게 표시)

        Returns:
            str: 알고리즘 이름 (예: "Base64 Encode", "SHA-256")
        """
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """
        카테고리 이름 (사이드바 그룹핑)

        Returns:
            str: 카테고리 (Encoding, Hash, TextProcessing, Cipher)
        """
        pass

    @abstractmethod
    def transform(self, input_text: str, options: Optional[Dict[str, any]] = None) -> str:
        """
        변환 실행

        Args:
            input_text: 사용자 입력 텍스트
            options: 알고리즘별 옵션 (可选)

        Returns:
            str: 변환 결과 텍스트

        Raises:
            ValueError: 입력이 유효하지 않을 때 (한국어 에러 메시지)
        """
        pass

    @abstractmethod
    def validate_input(self, input_text: str) -> bool:
        """
        입력 유효성 검증 (사전 검증)

        Args:
            input_text: 사용자 입력 텍스트

        Returns:
            bool: 유효하면 True, 아니면 False
        """
        pass

    @property
    def operation_type(self) -> OperationType:
        """
        작업 유형 반환 (기본 구현 제공)

        Returns:
            OperationType: 이 트랜스포머의 작업 유형
        """
        # 기본 구현: 하위 클래스에서 오버라이드 가능
        return OperationType.TEXT_PROCESSING
```

---

## Implementation Guidelines

### 1. Naming Convention

- **모듈 파일**: `{algorithm}.py` (소문자, 밑줄로 단어 구분)
  - 예: `base64.py`, `sha256.py`, `caesar_cipher.py`
- **클래스명**: `{Algorithm}Encode`, `{Algorithm}Decode`, `{Algorithm}Hash`
  - 예: `Base64Encode`, `URLDecode`, `SHA256Hash`

### 2. Error Handling

모든 에러는 `ValueError`를 발생시키고 **한국어 메시지**를 제공해야 합니다.

```python
# ✅ 좋은 예
def transform(self, input_text: str, options=None) -> str:
    if not input_text:
        raise ValueError("입력 텍스트가 비어있습니다")
    if not self._is_valid_base64(input_text):
        raise ValueError("잘못된 Base64 형식입니다")
    # ... 변환 로직

# ❌ 나쁜 예
def transform(self, input_text: str, options=None) -> str:
    if not input_text:
        raise Exception("empty input")  # 영어, 구체적이지 않음
```

### 3. Options 처리

```python
def transform(self, input_text: str, options=None) -> str:
    opts = options or {}

    # 옵션 기본값 제공
    padding = opts.get("padding", True)

    # 옵션 유효성 검증
    if "shift" in opts:
        shift = opts["shift"]
        if not isinstance(shift, int) or not (1 <= shift <= 25):
            raise ValueError("shift는 1-25 사이 정수여야 합니다")

    # ... 변환 로직
```

### 4. 입력 검증

```python
def validate_input(self, input_text: str) -> bool:
    """빠른 사전 검증"""

    # 빈 입력 체크 (해시 제외)
    if not input_text and self.operation_type != OperationType.HASH:
        return False

    # 길이 제한
    if len(input_text) > 10000:
        return False

    # 알고리즘별 검증
    if self.category == "Encoding":
        return self._validate_encoding_input(input_text)

    return True
```

---

## Examples

### Example 1: Base64 Encoder

```python
# src/transformers/encoding/base64.py

class Base64Encode(TransformerInterface):
    @property
    def name(self) -> str:
        return "Base64 Encode"

    @property
    def category(self) -> str:
        return "Encoding"

    @property
    def operation_type(self) -> OperationType:
        return OperationType.ENCODING

    def transform(self, input_text: str, options=None) -> str:
        if not input_text:
            raise ValueError("입력 텍스트가 비어있습니다")

        opts = options or {}
        padding = opts.get("padding", True)

        encoded = base64.b64encode(input_text.encode('utf-8')).decode('ascii')

        if not padding:
            encoded = encoded.rstrip('=')

        return encoded

    def validate_input(self, input_text: str) -> bool:
        return bool(input_text)  # Base64는 모든 텍스트 인코딩 가능
```

### Example 2: SHA-256 Hash

```python
# src/transformers/hashing/sha256.py

class SHA256Hash(TransformerInterface):
    @property
    def name(self) -> str:
        return "SHA-256"

    @property
    def category(self) -> str:
        return "Hash"

    @property
    def operation_type(self) -> OperationType:
        return OperationType.HASH

    def transform(self, input_text: str, options=None) -> str:
        opts = options or {}
        salt = opts.get("salt", "")

        # 빈 텍스트도 해시 가능
        data = (input_text + salt).encode('utf-8')
        return hashlib.sha256(data).hexdigest()

    def validate_input(self, input_text: str) -> bool:
        return True  # 모든 텍스트 해시 가능
```

---

## Testing Contract

모든 Transformer는 다음 테스트를 통과해야 합니다:

```python
import pytest

def test_basic_transformation():
    """기본 변환 테스트"""

def test_empty_input():
    """빈 입력 처리 (해시 제외)"""

def test_large_input():
    """대용량 입력 (10,000자)"""

def test_invalid_input():
    """잘못된 입력 에러 처리"""

def test_options_handling():
    """옵션 처리 (해당하는 경우)"""
```

---

## Registration

모든 Transformer는 `AlgorithmRegistry`에 등록해야 합니다:

```python
# src/transformers/encoding/__init__.py

from .base64 import Base64Encode, Base64Decode

def register_encodings(registry):
    """Encoding 카테고리 트랜스포머 등록"""
    registry.register(Base64Encode())
    registry.register(Base64Decode())
    # ...
```
