# Algorithm Registry Contract

**Version**: 1.0
**Date**: 2026-01-21

## Overview

알고리즘 등록 시스템(AlgorithmRegistry)의 API 계약서입니다.

---

## Class Definition

```python
from typing import Dict, List, Optional, Protocol
from PySide6.QtCore import QObject, Signal

class TransformerInterface(Protocol):
    """트랜스포머 인터페이스 (간략화)"""
    @property
    def name(self) -> str: ...
    @property
    def category(self) -> str: ...
    def transform(self, input_text: str, options=None) -> str: ...

class AlgorithmRegistry(QObject):
    """알고리즘 등록 및 검색 시스템"""

    # Signal: 새 알고리즘 등록 시
    algorithm_registered = Signal(str)  # algorithm_name

    # Signal: 검색 완료 시
    search_completed = Signal(list)  # List[TransformerInterface]

    def __new__(cls):
        """싱글톤 패턴"""
        if not hasattr(cls, '_instance'):
            cls._instance = super(AlgorithmRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self._algorithms: Dict[str, List[TransformerInterface]] = {
            "Encoding": [],
            "Hash": [],
            "Text Processing": [],
            "Classical Ciphers": [],
        }
        self._search_index: List[tuple[str, str, TransformerInterface]] = []

    def register(self, transformer: TransformerInterface) -> None:
        """
        알고리즘 등록

        Args:
            transformer: TransformerInterface 구현체

        Raises:
            ValueError: 동일한 이름의 알고리즘이 이미 등록된 경우
        """
        category = transformer.category
        name = transformer.name

        # 카테고리 유효성 검증
        if category not in self._algorithms:
            raise ValueError(f"알 수 없는 카테고리입니다: {category}")

        # 중복 등록 방지
        for existing in self._algorithms[category]:
            if existing.name == name:
                raise ValueError(f"이미 등록된 알고리즘입니다: {name}")

        # 등록
        self._algorithms[category].append(transformer)
        self._search_index.append((name, category, transformer))

        # Signal 발사
        self.algorithm_registered.emit(name)

    def get_all(self) -> Dict[str, List[TransformerInterface]]:
        """
        카테고리별 모든 알고리즘 반환

        Returns:
            Dict[str, List[TransformerInterface]]: {category: [transformers]}
        """
        return self._algorithms.copy()

    def get_by_category(self, category: str) -> List[TransformerInterface]:
        """
        카테고리별 알고리즘 리스트 반환

        Args:
            category: 카테고리 이름

        Returns:
            List[TransformerInterface]: 해당 카테고리의 알고리즘 리스트

        Raises:
            KeyError: 존재하지 않는 카테고리
        """
        return self._algorithms[category].copy()

    def search(self, query: str) -> List[TransformerInterface]:
        """
        이름/카테고리로 검색 (대소문자 구분 없음)

        Args:
            query: 검색어 (빈 문자열 = 모두 반환)

        Returns:
            List[TransformerInterface]: 검색 결과
        """
        if not query:
            # 빈 검색어 = 모두 반환
            return [t for _, _, t in self._search_index]

        query_lower = query.lower()
        results = []
        for name, category, transformer in self._search_index:
            if query_lower in name.lower() or query_lower in category.lower():
                results.append(transformer)

        self.search_completed.emit(results)
        return results

    def get_by_name(self, name: str) -> Optional[TransformerInterface]:
        """
        이름으로 알고리즘 조회

        Args:
            name: 알고리즘 이름 (예: "Base64 Encode")

        Returns:
            Optional[TransformerInterface]: 찾으면 반환, 없으면 None
        """
        for transformer_list in self._algorithms.values():
            for transformer in transformer_list:
                if transformer.name == name:
                    return transformer
        return None

    def get_categories(self) -> List[str]:
        """
        모든 카테고리 이름 반환 (등록된 순서)

        Returns:
            List[str]: 카테고리 리스트
        """
        categories = []
        for category in self._algorithms:
            if self._algorithms[category]:  # 비어있지 않은 카테고리만
                categories.append(category)
        return categories
```

---

## Usage Examples

### Example 1: Algorithm Registration

```python
# src/main.py 또는 각 카테고리 __init__.py

from src.transformers.encoding.base64 import Base64Encode, Base64Decode
from src.transformers.hashing.sha256 import SHA256Hash

registry = AlgorithmRegistry()

# 인코딩 등록
registry.register(Base64Encode())
registry.register(Base64Decode())

# 해시 등록
registry.register(SHA256Hash())
```

### Example 2: Searching

```python
# src/ui/sidebar.py

registry = AlgorithmRegistry()

# 검색
results = registry.search("base64")  # ["Base64 Encode", "Base64 Decode"]
results = registry.search("SHA")     # ["SHA-256", "SHA-512", ...]
results = registry.search("")        # 모든 알고리즘
```

### Example 3: Category Filtering

```python
# src/ui/sidebar.py

registry = AlgorithmRegistry()

# 카테고리별 트리 구성
for category in registry.get_categories():
    algorithms = registry.get_by_category(category)
    for algo in algorithms:
        print(f"{category}: {algo.name}")
```

---

## Performance Requirements

- **등록 시간**: O(1) (append operation)
- **검색 시간**: O(n) where n = 전체 알고리즘 수 (n=80으로 충분히 빠름)
- **메모리**: 각 알고리즘 당 ~1KB 예상 (총 ~80KB)
- **0.3초 목표**: 80개 알고리즘 선형 탐색으로 충분히 달성 가능

---

## Thread Safety

- `register()`: UI 스레드에서 호출 (싱글톤 보장 필요 없음)
- `search()`: 백그라운드 스레드에서 호출 가능 (읽기 전용)
- Qt Signal을 사용하므로 자동으로 스레드 세이프
