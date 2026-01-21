# Quickstart Guide

**Feature**: 확장형 GUI 텍스트 유틸리티 툴
**Date**: 2026-01-21
**Phase**: 1 - Design

---

## 개발 환경 설정

### 1. Python 설치

Python 3.11 이상이 필요합니다.

```bash
# Python 버전 확인
python --version
# 출력: Python 3.11.x 이상이어야 함
```

**Python 다운로드**:
- Windows: https://www.python.org/downloads/
- 설치 시 "Add Python to PATH" 체크박스 선택

### 2. 가상 환경 생성 (권장)

```bash
# 프로젝트 루트로 이동
cd C:\Users\yuh\Desktop\encoder

# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
venv\Scripts\activate
```

### 3. 의존성 설치

```bash
# requirements.txt 생성 (이미 프로젝트에 있음)
pip install -r requirements.txt
```

**requirements.txt 내용**:
```text
PySide6==6.6.0
pynput==1.7.6
pytest==7.4.3
pytest-qt==4.2.0
```

---

## 프로젝트 구조 이해

```
encoder/
├── src/                          # 소스 코드
│   ├── main.py                   # 앱 진입점
│   ├── ui/                       # PySide6 GUI
│   │   ├── main_window.py        # 메인 윈도
│   │   ├── sidebar.py            # 좌측 사이드바
│   │   ├── content_area.py       # 우측 컨텐츠 영역
│   │   ├── tray_icon.py          # 시스템 트레이
│   │   └── settings_dialog.py    # 설정 다이얼로그
│   ├── transformers/             # 변환 알고리즘
│   │   ├── base.py              # TransformerInterface
│   │   ├── encoding/            # 인코딩/디코딩
│   │   ├── hashing/             # 해시
│   │   ├── text_processing/     # 텍스트 처리
│   │   └── ciphers/             # 클래식 암호
│   ├── registry.py              # 알고리즘 등록 시스템
│   ├── hotkey/                  # 핫키 엔진
│   │   └── listener.py          # pynput 리스너
│   └── utils/                   # 유틸리티
├── tests/                       # 테스트
│   ├── unit/                    # 유닛 테스트
│   └── integration/             # 통합 테스트
├── build/                       # PyInstaller 설정
├── requirements.txt             # 의존성
└── README.md                    # 사용자 매뉴얼
```

---

## 애플리케이션 실행

### 개발 모드 실행

```bash
# 가상 환경 활성화 후
python src/main.py
```

**예상 동작**:
- 메인 윈도 표시
- 좌측 사이드바에 카테고리 트리 (Encoding, Hash, Text Processing, Classical Ciphers)
- 상단 검색창
- 우측 입력창 + 옵션 + 출력창
- 시스템 트레이 아이콘 생성

### 핫키 테스트

```bash
# 앱 실행 중 Ctrl + . 누르면
# 창 숨김/표시 전환
```

---

## 테스트 실행

### 전체 테스트

```bash
# 모든 테스트 실행
pytest tests/ -v

# 특정 카테고리 테스트
pytest tests/unit/test_transformers/ -v

# 커버리지 리포트
pytest tests/ --cov=src --cov-report=html
```

### 특정 테스트 파일

```bash
# Base64 테스트
pytest tests/unit/test_transformers/test_base64.py -v

# 레지스트리 테스트
pytest tests/unit/test_registry.py -v
```

---

## 빌드 및 배포

### 실행 파일 생성 (멀티 플랫폼)

**Windows (.exe)**:
```bash
# PyInstaller로 빌드
pyinstaller build/encoder.spec --clean --onefile

# 출력: build/dist/TextEncoder.exe
```

**macOS (.app)**:
```bash
# macOS에서 PyInstaller로 빌드
pyinstaller build/encoder.spec --clean --onefile --windowed

# 출력: build/dist/TextEncoder.app
# 참고: Apple Silicon M1/M2에서는 먼저 Rosetta 호환 또는 네이티브 빌드 환경 구성 필요
```

**Linux (binary)**:
```bash
# Linux에서 PyInstaller로 빌드
pyinstaller build/encoder.spec --clean --onefile

# 출력: build/dist/text-encoder
# 실행 권한 추가: chmod +x build/dist/text-encoder
```

### 실행 파일 테스트

**Windows**:
```bash
# 생성된 .exe 실행
build\dist\TextEncoder.exe
```

**macOS**:
```bash
# 생성된 .app 실행
open build/dist/TextEncoder.app
# 또는 더블 클릭으로 실행
```

**Linux**:
```bash
# 생성된 바이너리 실행
./build/dist/text-encoder
```

**검증 항목**:
1. 창 정상 표시
2. 모든 변환 기능 작동
3. 핫키(`Ctrl + .`) 작동
4. 시스템 트레이 작동
5. 복사 버튼 작동

---

## 코드 구조 빠른 이해

### 1. 메인 진입점

```python
# src/main.py

import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.registry import AlgorithmRegistry

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Text Encoder")

    # 레지스트리 초기화
    registry = AlgorithmRegistry()

    # 트랜스포머 등록
    from src.transformers.encoding import register_encodings
    from src.transformers.hashing import register_hashing
    # ...

    # 메인 윈도
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### 2. 트랜스포머 등록

```python
# src/transformers/encoding/__init__.py

from .base64 import Base64Encode, Base64Decode
from .url import URLEncode, URLDecode
# ...

def register_encodings(registry):
    """Encoding 카테고리 등록"""
    registry.register(Base64Encode())
    registry.register(Base64Decode())
    # ...
```

### 3. 변환 실행 흐름

```
[User Input] → [Search Algorithm] → [Click Transform Button]
    ↓
[AlgorithmRegistry.get_by_name()]
    ↓
[Transformer.transform(input_text, options)]
    ↓
[Display Result or Error]
```

---

## 개발 워크플로우

### 1. 새로운 알고리즘 추가

```python
# 1. src/transformers/encoding/my_algorithm.py 생성
from src.transformers.base import TransformerInterface

class MyAlgorithmEncode(TransformerInterface):
    @property
    def name(self) -> str:
        return "My Algorithm Encode"

    @property
    def category(self) -> str:
        return "Encoding"

    def transform(self, input_text: str, options=None) -> str:
        # 변환 로직
        return result

    def validate_input(self, input_text: str) -> bool:
        # 검증 로직
        return True

# 2. src/transformers/encoding/__init__.py에 등록 추가
from .my_algorithm import MyAlgorithmEncode

def register_encodings(registry):
    # ...
    registry.register(MyAlgorithmEncode())

# 3. 테스트 작성
# tests/unit/test_transformers/test_my_algorithm.py
```

### 2. Git 커밋 전 체크리스트

```bash
# 1. 테스트 통과 확인
pytest tests/ -v

# 2. tasks.md 진척도 업데이트

# 3. 커밋
git add .
git commit -m "feat: 새로운 알고리즘 구현"
```

---

## 문제 해결

### 1. PyInstaller 오류

**문제**: `ModuleNotFoundError: No module named 'PySide6'`

**해결**:
```bash
# 가상 환경 재설치
python -m venv venv --clear
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. 핫키 작동 안 함

**문제**: 핫키를 눌러도 반응 없음

**해결**:
- **Windows**: 관리자 권한으로 실행 확인, 바이러스 백신 소프트웨어 차단 확인
- **macOS**: 보안 설정에서 "어떤 출처의 다운로드나" 허용, 또는 시스템 환경설정 > 개인정보 보안 & 보안에서 앱 허용
- **Linux**: X11 또는 Wayland 컴포지터와의 호환성 확인, accessibility 권한 확인
- 모든 OS: 다른 애플리케이션이 이미 `Ctrl + .`를 사용하는지 확인

### 3. 테스트 실패

**문제**: `ImportError: No module named src`

**해결 (Windows)**:
```bash
set PYTHONPATH=%CD%\src
pytest tests/ -v
```

**해결 (macOS/Linux)**:
```bash
export PYTHONPATH=$PWD/src
pytest tests/ -v
```

### 4. 플랫폼별 시스템 트레이 문제

**macOS Gatekeeper**:
```bash
# 앱 실행이 차단될 경우
xattr -cr build/dist/TextEncoder.app
```

**Linux 실행 권한**:
```bash
# 실행 권한 부여
chmod +x build/dist/text-encoder
```

**해결**:
```bash
# 프로젝트 루트에서 PYTHONPATH 설정
set PYTHONPATH=%CD%\src
pytest tests/ -v
```

---

## 다음 단계

1. **Phase 2**: `/speckit.tasks` 실행으로 `tasks.md` 생성
2. **구현 시작**: P1(기본 변환)부터 순차적 구현
3. **테스트**: 각 기능 구현 후 유닛 테스트 작성
4. **커밋**: 각 Task/Phase 완료 시 Git commit
