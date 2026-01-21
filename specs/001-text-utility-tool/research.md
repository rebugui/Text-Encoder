# Research & Technology Decisions

**Feature**: 확장형 GUI 텍스트 유틸리티 툴
**Date**: 2026-01-21
**Phase**: 0 - Research & Technology Selection

## Overview

본 문서는 텍스트 유틸리티 툴 개발을 위한 기술 스택 선정 및 최적 구현 방안을 조사하고 결정한 내용을 담고 있다.

---

## 1. GUI 프레임워크 선정

### 조사 대상
- **PySide6**: Qt for Python의 공식 바인딩 (LGPL 라이선스)
- **PyQt6**: Riverbank Computing의 Qt 바인딩 (GPL/상업 라이선스)
- **Tkinter**: Python 표준 라이브러리 내장 GUI

### 평가 기준
1. 시스템 트레이(QSystemTrayIcon) 지원
2. 네이티브 look & feel
3. 문서화 품질 및 커뮤니티 지원
4. 라이선스 (단일 .exe 배포 시 영향)
5. 배포 용이성

### 결정: **PySide6**

**이유**:
1. ✅ **시스템 트레이 지원**: `QSystemTrayIcon`, `QMenu`로 모든 플랫폼에서 네이티브 트레이 기능 완벽 지원
2. ✅ **네이티브 UI**: Qt6는 Windows 10/11, macOS, Linux 각각의 네이티브 look & feel 자동 제공
3. ✅ **크로스플랫폼**: 단일 코드베이스로 Windows/macOS/Linux 모두 지원
4. ✅ **라이선스**: LGPL로 상용 프로젝트에도 사용 가능 (PyQt6는 GPL)
5. ✅ **문서화**: Qt 공식 문서와 PySide6 가이드 잘 정리되어 있음
6. ✅ **풍부한 위젯**: Sidebar, TreeView, Splitter 등 복잡한 UI 구현에 용이
7. ✅ **PyInstaller 호환성**: 모든 플랫폼에서 단일 실행 파일 패키징에 검증된 사례 다수

**거른 대안**:
- Tkinter: 트레이 지원이 약하고, 모던 UI 구현에 제약 있음, 크로스플랫폼 일관성 부족
- PyQt6: GPL 라이선스로 오픈소스 배포 시 소스 코드 공개 의무 발생

---

## 2. 글로벌 핫키 라이브러리 선정

### 조사 대상
- **pynput**: 크로스플랫폼 키보드/마우스 입력 제어 라이브러리
- **keyboard**: Windows 전용 키보드 후킹 라이브러리

### 평가 기준
1. 백그라운드 스레드 안정성
2. 전역 핫키(다른 앱 focused 시) 동작
3. Windows/macOS/Linux 호환성
4. PySide6와의 충돌 여부
5. 플랫폼별 핫키 차이(예: macOS Cmd vs Ctrl) 처리

### 결정: **pynput**

**이유**:
1. ✅ **백그라운드 스레드 안정성**: 전용 listener 스레드에서 실행되어 UI 차단 없음
2. ✅ **글로벌 핫키 지원**: `pynput.keyboard.GlobalHotKeys`로 애플리케이션 밖에서도 동작
3. ✅ **크로스플랫폼**: Windows, macOS, Linux 모두 지원 (단일 코드베이스)
4. ✅ **안정성**: 오래된 프로젝트로 안정적인 버그 수정 및 커뮤니티 지원
5. ✅ **플랫폼별 자동 처리**: macOS에서 Cmd 키, Windows/Linux에서 Ctrl 키 자동 인식

**구현 방안**:
```python
from pynput import keyboard

def on_activate():
    """Ctrl+. 핫키 핸들러"""
    toggle_window_visibility()

# 백그라운드 스레드에서 리스너 실행
with keyboard.GlobalHotKeys({
    '<ctrl>+.': on_activate
}) as h:
    h.join()
```

**거른 대안**:
- keyboard: Windows 전용으로 Linux/macOS 포팅 시 재작성 필요

---

## 3. 멀티 플랫폼 패키징 전략

### 조사 대상
- **PyInstaller**: 가장 널리 사용되는 Python 패커 (크로스플랫폼)
- **py2exe**: Windows 전용, PyInstaller보다 덜 인기
- **Nuitka**: Python → C++ 컴파일러 (더 빠르지만 복잡함)

### 결정: **PyInstaller**

**최적화 옵션**:

```python
# build/encoder.spec
a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'pynput',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',       # Tkinter 미사용
        'matplotlib',    # 데이터 시각화 불필요
        'numpy',         # 수학 연산 불필요
        'pandas',        # 데이터 분석 불필요
        'IPython',       # 대화형 쉘 불필요
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TextEncoder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # UPX 압축으로 파일 크기 감소
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 콘솔 창 없음
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',  # 트레이 아이콘
)
```

**실행 명령어**:

```bash
# Windows
pyinstaller build/encoder.spec --clean --onefile
# 출력: build/dist/TextEncoder.exe

# macOS
pyinstaller build/encoder.spec --clean --onefile --windowed
# 출력: build/dist/TextEncoder.app
# Apple Silicon + Intel Universal Binary를 위해 별도 빌드 필요

# Linux
pyinstaller build/encoder.spec --clean --onefile
# 출력: build/dist/text-encoder
```

**최적화 결과 목표**:
- **Windows**: 실행 파일 크기 < 50MB (UPX 압축 적용)
- **macOS**: .app 번들 크기 < 100MB (Intel + Apple Silicon 별도 빌드)
- **Linux**: 바이너리 크기 < 50MB
- **공통**: 콜드 스타트 < 3초, 메모리 사용 < 100MB idle

---

## 4. 80+ 알고리즘 구현 전략

### 조사: 표준 라이브러리 커버리지

**Python 표준 라이브러리로 구현 가능**:
- ✅ Base64: `base64` 모듈
- ✅ URL Encoding: `urllib.parse.quote` / `unquote`
- ✅ Hex: `binascii.hexlify` / `unhexlify`
- ✅ HTML Entities: `html.escape` / `unescape`
- ✅ 해시: `hashlib` (MD5, SHA-1, SHA-224/256/384/512, SHA3, BLAKE2)
- ✅ CRC32: `binascii.crc32`
- ✅ JSON: `json.dumps` (with indent)
- ✅ Unicode Escape: `codecs` 모듈

**자체 구현 필요**:
- Base32, Base58 (Bitcoin), Base62, Base85, Base91, Base32Hex
- Punycode (IDN)
- Quoted-Printable
- Morse Code, Braille
- ROT13, Caesar Cipher, Vigenère, Atbash

### 결정: **표준 라이브러리 중심 + 자체 구현**

**이유**:
1. ✅ **의존성 최소화**: 외부 라이브러리를 최소로 줄여 .exe 크기 감소
2. ✅ **안정성**: 표준 라이브러리는 테스트되고 검증됨
3. ✅ **성능**: C로 구현된 표준 라이브러리가 Python 구현보다 빠름
4. ✅ **유지보수**: 외부 의존성 업데이트 필요 없음

**자체 구현 예시** (Base58):
```python
# src/transformers/encoding/base58.py
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def base58_encode(s: bytes) -> str:
    """Bitcoin Base58 인코딩"""
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break

    num = int.from_bytes(s, 'big')
    result = ''
    while num > 0:
        num, remainder = divmod(num, 58)
        result = ALPHABET[remainder] + result
    return '1' * count + result
```

---

## 5. 검색 필터링 최적화

### 요구사항
- 80개 이상의 알고리즘 이름으로 실시간 필터링
- 응답 시간: 0.3초 이내

### 결정: **인메모리 인덱스 + 문자열 매칭**

**구현 방안**:
```python
class AlgorithmRegistry:
    def __init__(self):
        self._algorithms: Dict[str, List[TransformerInterface]] = {}
        self._search_index: List[Tuple[str, str, TransformerInterface]] = []
        # (name, category, transformer) 튜플 리스트

    def search(self, query: str) -> List[TransformerInterface]:
        """대소문자 구분 없는 실시간 검색 (O(n))"""
        query_lower = query.lower()
        results = []
        for name, category, transformer in self._search_index:
            if query_lower in name.lower() or query_lower in category.lower():
                results.append(transformer)
        return results
```

**최적화**:
- 사전에 (name, category)를 소문자로 변환한 인덱스 구축
- 80개 알고리즘이면 O(n) 선형 탐색으로 충분 (n=80으로 매우 작음)
- 0.3초 목표는 여유있게 달성 가능

---

## 6. 대용량 텍스트 처리 최적화

### 요구사항
- 10,000자 텍스트 변환: 2초 이내
- UI 응답성 유지 (프리징 방지)

### 결정: **백그라운드 스레드에서 처리 + 프로그레스 바**

**구현 방안**:
```python
from PySide6.QtCore import QThread, Signal

class TransformationWorker(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, transformer, input_text, options=None):
        super().__init__()
        self.transformer = transformer
        self.input_text = input_text
        self.options = options or {}

    def run(self):
        try:
            result = self.transformer.transform(self.input_text, self.options)
            self.finished.emit(result)
        except ValueError as e:
            self.error.emit(str(e))

# MainWindow에서 사용
worker = TransformationWorker(transformer, input_text)
worker.finished.connect(lambda result: update_output(result))
worker.start()
```

**최적화**:
- Qt의 signal/slot 메커니즘으로 UI 차단 없이 백그라운드 처리
- 10,000자는 실제로는 매우 작아서 (< 1ms) 대부분의 경우 즉시 완료
- 대용량 처리 시에만 백그라운드 스레드 사용

---

## 7. 핫키 충돌 및 설정 저장

### 요구사항 (P5)
- 사용자가 `Ctrl + .` 대신 다른 핫키로 변경 가능
- 시스템 단축키(Ctrl+C, Ctrl+V)와의 충돌 방지

### 결정: **JSON 파일 설정 저장 + 핫키 유효성 검증**

**구현 방안**:
```python
import json
from pathlib import Path

# 사용자 설정 저장 경로
CONFIG_PATH = Path.home() / '.text-encoder' / 'config.json'

DEFAULT_CONFIG = {
    'hotkey': 'Ctrl+.',
    'window_position': {'x': 100, 'y': 100},
    'last_category': 'Encoding'
}

def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return DEFAULT_CONFIG

def save_config(config: dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# 핫키 유효성 검증
BLOCKED_HOTKEYS = [
    'Ctrl+C', 'Ctrl+V', 'Ctrl+X', 'Ctrl+Z', 'Ctrl+Y',
    'Ctrl+A', 'Ctrl+S', 'Ctrl+O', 'Ctrl+N', 'Ctrl+W'
]

def is_hotkey_valid(hotkey: str) -> bool:
    return hotkey not in BLOCKED_HOTKEYS
```

---

## 8. 테스트 전략

### 결정: **pytest + 모의 객체(Mock)**

**테스트 구조**:
```python
# tests/unit/test_transformers/test_base64.py
import pytest
from src.transformers.encoding.base64 import Base64Encode

def test_base64_encode_basic():
    transformer = Base64Encode()
    assert transformer.transform("Hello") == "SGVsbG8="

def test_base64_encode_empty():
    transformer = Base64Encode()
    assert transformer.transform("") == ""

def test_base64_decode_invalid():
    transformer = Base64Decode()
    with pytest.raises(ValueError, match="잘못된 Base64 형식"):
        transformer.transform("Not!Base64")
```

**커버리지 목표**:
- 유닛 테스트: 100% (모든 변환 알고리즘)
- 통합 테스트: 핫키, 트레이, UI 흐름

---

## 9. 한글 에러 메시지 처리

### 결정: **별도 언어 파일 (i18n) 없이 직접 하드코딩**

**이유**:
- 데스크톱 유틸리티로 다국어 지원 불필요
- 한국어 고정 사용자 대상
- 번역 파일 관리 오버헤드 제거

**구현 예시**:
```python
class EncodingError(Exception):
    """인코딩/디코딩 에러"""

    MESSAGES = {
        'base64_invalid': "잘못된 Base64 형식입니다",
        'url_invalid': "잘못된 URL 인코딩 형식입니다",
        'empty_input': "입력 텍스트가 비어있습니다",
    }

    def __init__(self, error_type: str):
        self.message = self.MESSAGES.get(error_type, "알 수 없는 오류입니다")
        super().__init__(self.message)
```

---

## Summary

| Category | Decision | Rationale |
|----------|----------|-----------|
| GUI Framework | **PySide6** | Cross-platform, system tray, native UI per OS, LGPL license |
| Global Hotkey | **pynput** | Background thread, cross-platform (Win/macOS/Linux), stable |
| Packaging | **PyInstaller** | Single executable per platform, UPX compression, proven |
| Algorithms | **Stdlib + Custom** | Minimize dependencies, stable, fast |
| Search | **In-memory index** | O(n) sufficient for n=80 |
| Large Text | **Background thread** | Qt signals/slots, UI responsiveness |
| Config | **JSON file** | Simple, human-readable, no DB needed |
| Testing | **pytest** | Industry standard, fixtures, plugins |
| i18n | **Korean only** | Target audience, no translation overhead |
| Platform Support | **Win/macOS/Linux** | Single codebase, Qt6 automatic native look & feel |

All technical decisions are made and validated. Ready for Phase 1 design documents.
