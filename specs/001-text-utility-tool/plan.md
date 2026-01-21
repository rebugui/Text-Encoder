# Implementation Plan: 확장형 GUI 텍스트 유틸리티 툴

**Branch**: `001-text-utility-tool` | **Date**: 2026-01-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-text-utility-tool/spec.md`

## Summary

보안 전문가와 개발자를 위한 포괄적인 텍스트 변환 유틸리티 데스크톱 애플리케이션을 개발한다. 80개 이상의 변환 알고리즘(인코딩/디코딩, 해시, 텍스트 처리, 클래식 암호)을 제공하며, 백그라운드 실행과 글로벌 핫키(`Ctrl + .`)로 빠른 접근성을 확보한다. PySide6 기반 GUI와 플러그인 아키텍처를 사용하여 확장 가능한 모듈 구조를 구현하고, PyInstaller로 각 플랫폼(Windows, macOS, Linux)별 단일 실행 파일로 패키징한다.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**:
- PySide6 (Qt6 UI framework, system tray, native widgets)
- pynput (global hotkey listener)
- PyInstaller (single .exe packaging)
- Python standard library: hashlib, base64, urllib.parse, json, re, binascii, html

**Storage**: N/A (stateless desktop application, temporary in-memory state only)

**Testing**: pytest (unit tests for all transformation algorithms)

**Target Platform**:
- **Windows**: Windows 10/11 (x64)
- **macOS**: macOS 11+ (Big Sur and later, Intel + Apple Silicon)
- **Linux**: Ubuntu 20.04+, Fedora 35+, Debian 11+ with GNOME/KDE/XFCE (x64)

**Project Type**: single (desktop GUI application)

**Performance Goals**:
- Text transformation: ≤2 seconds for 10,000 characters
- Search filter response: ≤0.3 seconds
- Hotkey toggle: ≤0.5 seconds
- UI responsiveness: No freezing during operations
- Memory footprint: <100MB idle

**Constraints**:
- Single executable file per platform (Windows .exe, macOS .app, Linux binary, no separate dependencies)
- Offline operation (no network calls)
- Administrator/root rights not required
- Korean language UI with error messages
- Plugin architecture for algorithm extensibility
- Cross-platform compatibility using Qt6 (automatic native look & feel per OS)

**Scale/Scope**:
- 80+ transformation algorithms across 4 categories
- 6 user stories (P1-P6 priorities)
- 85 functional requirements
- ~2,000-3,000 LOC estimated (excluding tests)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. 한국어 문서화 (NON-NEGOTIABLE)
- **Status**: PASS
- **Evidence**: spec.md 작성 완료, plan.md와 모든 산출물 한국어 작성 예정

### ✅ II. 단위별 작업 및 Git 워크플로우 (NON-NEGOTIABLE)
- **Status**: PASS
- **Evidence**: User stories P1-P6 명확히 정의됨, 각 기능 완료 시 commit 계획

### ✅ III. 테스트 주도 개발 (NON-NEGOTIABLE)
- **Status**: PASS
- **Evidence**: pytest 선정, 모든 변환 알고리즘 유닛 테스트 계획 (Phase 1)

### ✅ IV. 단일 실행 파일 배포
- **Status**: PASS
- **Evidence**: PyInstaller 사용, 단일 .exe 패키징 계획

### ✅ V. 직관적 GUI 설계
- **Status**: PASS
- **Evidence**:
  - Input/Output 텍스트 박스 명확히 분리 (사이드바 + 우측 컨텐츠 영역)
  - 카테고리별 알고리즘 그룹화 (Encoding, Hash, Text Processing, Classical Ciphers)
  - 검색 필터링 기능으로 80+ 알고리즘 빠른 찾기
  - 한국어 에러 메시지 (FR-073)
  - 복사 버튼 제공 (FR-006, FR-UX-004)

**결과**: 모든 헌법 원칙 준수. Phase 0/1 진행 가능.

## Project Structure

### Documentation (this feature)

```text
specs/001-text-utility-tool/
├── spec.md              # Feature specification (완료)
├── plan.md              # This file (본 파일)
├── research.md          # Phase 0 출력 (기술 조사 결과)
├── data-model.md        # Phase 1 출력 (데이터 모델)
├── quickstart.md        # Phase 1 출력 (빠른 시작 가이드)
├── contracts/           # Phase 1 출력 (내부 API 계약서)
│   ├── transformer_interface.md  # 변환기 인터페이스 정의
│   ├── hotkey_engine.md          # 핫키 엔진 계약서
│   └── registry.md               # 알고리즘 등록 시스템
└── tasks.md             # Phase 2 출력 (/speckit.tasks 명령으로 생성)
```

### Source Code (repository root)

```text
src/
├── main.py              # 애플리케이션 진입점
├── ui/                  # PySide6 GUI 컴포넌트
│   ├── __init__.py
│   ├── main_window.py   # 메인 윈도우 (사이드바 + 컨텐츠 영역)
│   ├── sidebar.py       # 좌측 사이드바 (카테고리 트리, 검색)
│   ├── content_area.py  # 우측 컨텐츠 영역 (입력/옵션/출력)
│   ├── tray_icon.py     # 시스템 트레이 아이콘
│   └── settings_dialog.py  # 설정 다이얼로그 (핫키 설정 등)
├── transformers/        # 변환 알고리즘 모듈 (플러그인 아키텍처)
│   ├── __init__.py
│   ├── base.py          # 추상 base 클래스
│   ├── encoding/        # 인코딩/디코딩
│   │   ├── __init__.py
│   │   ├── base64.py
│   │   ├── url.py
│   │   ├── hex.py
│   │   ├── base32.py
│   │   ├── base58.py
│   │   ├── base85.py
│   │   ├── html_entities.py
│   │   └── ...         # 기타 인코딩
│   ├── hashing/         # 해시 알고리즘
│   │   ├── __init__.py
│   │   ├── md5.py
│   │   ├── sha.py
│   │   └── ...         # 기타 해시
│   ├── text_processing/ # 텍스트 처리
│   │   ├── __init__.py
│   │   ├── json_format.py
│   │   ├── case_conversion.py
│   │   └── ...         # 기타 텍스트 처리
│   └── ciphers/         # 클래식 암호
│       ├── __init__.py
│       ├── rot13.py
│       └── ...         # 기타 암호
├── registry.py          # 알고리즘 등록 시스템 (동적 로딩)
├── hotkey/              # 글로벌 핫키 엔진
│   ├── __init__.py
│   └── listener.py      # pynput 기반 백그라운드 리스너
└── utils/               # 유틸리티
    ├── __init__.py
    ├── clipboard.py     # 클립보드 관리
    └── validators.py    # 입력 유효성 검증

tests/
├── __init__.py
├── conftest.py          # pytest 설정
├── unit/                # 유닛 테스트
│   ├── test_transformers/  # 각 변환기 테스트
│   │   ├── test_base64.py
│   │   ├── test_url.py
│   │   ├── test_hashing.py
│   │   └── ...
│   ├── test_registry.py     # 레지스트리 테스트
│   └── test_hotkey.py       # 핫키 기능 테스트
└── integration/
    └── test_ui_flows.py     # UI 통합 테스트

build/                      # PyInstaller 빌드 출력
├── encoder.spec            # PyInstaller 스펙 파일
└── dist/
    ├── TextEncoder.exe     # Windows 실행 파일
    ├── TextEncoder.app     # macOS 실행 파일 (번들)
    └── text-encoder        # Linux 실행 파일

requirements.txt            # Python 의존성
pyproject.tombo             # 프로젝트 메타데이터
README.md                   # 사용자 매뉴얼
```

**Structure Decision**: Single project structure 선택 (Desktop GUI 애플리케이션).
- PySide6 기반 UI와 플러그인 방식 transformers 디렉토리로 확장성 확보
- 모든 변환 알고리즘은 독립적인 모듈로 `transformers/` 하위에 카테고리별로 조직
- `registry.py` 중심의 동적 로딩으로 신규 알고리즘 추가 시 UI 코드 수정 불필요
- 테스트는 `tests/unit/`와 `tests/integration/`로 분리

## Complexity Tracking

> **No violations** - Constitution Check에 통과하여 복잡성 추적 불필요

## Phase 0: Research & Technology Decisions

### Research Tasks

1. **GUI 프레임워크 선정**
   - 조사 포인트: 시스템 트레이 지원, 네이티브 look & feel, 라이선스, 문서화 품질
   - 결정: PySide6 (LGPL, Qt 공식 바인딩, 풍부한 위젯, 크로스플랫폼)
   - 상세 분석: `research.md` §1 참조

2. **글로벌 핫키 구현 방법 조사**
   - 조사 포인트: pynput vs keyboard 라이브러리, 백그라운드 스레드 안정성, 플랫폼별 호환성
   - 결정: pynput (크로스플랫폼, 안정적, 저수준 키보드 훅)

3. **단일 실행 파일 패키징 최적화 (멀티 OS)**
   - 조사 포인트: PyInstaller 옵션, 의존성 최소화, 실행 파일 크기 최적화
   - Windows: --onefile --noconsole --icon icon.ico
   - macOS: --onefile --windowed --icon icon.icns (Code signing 고려)
   - Linux: --onefile --noconsole (AppImage 형식도 고려)
   - 결정: --onefile --noconsole --exclude-module 불필요한 모듈 제거, 플랫폼별 별도 빌드

4. **80+ 알고리즘 구현 라이브러리 조사**
   - 조사 포인트: 표준 라이브러리만으로 충분한지, 외부 의존성 필요 여부
   - 결정: 표준 라이브러리 중심 (hashlib, base64, urllib.parse, binascii), 일부는 자체 구현 (Base58, Base62, Morse Code)

5. **플랫폼별 시스템 트레이 차이점 조사**
   - 조사 포인트: Windows 시스템 트레이, macOS Menu Bar, Linux System Tray (GNOME/KDE/XFCE)
   - 결정: Qt6가 플랫폼별 차이를 자동으로 처리하므로 일관된 API 사용 가능

## Phase 1: Design Documents

### 1.1 Data Model (data-model.md)

**주요 엔티티**:

1. **TransformationOperation (변환 작업)**
   - `operation_type`: Enum (ENCODING, DECODING, HASH, TEXT_PROCESSING, CIPHER)
   - `algorithm`: str (알고리즘 이름, 예: "Base64", "SHA-256")
   - `input_text`: str (사용자 입력)
   - `output_text`: str (변환 결과)
   - `options`: dict (알고리즘별 옵션, 예: Base64 padding, Caesar shift)
   - `success`: bool
   - `error_message`: Optional[str]

2. **ApplicationState (프로그램 상태)**
   - `window_visibility`: Enum (VISIBLE, HIDDEN)
   - `background_state`: Enum (RUNNING, TERMINATED)
   - `current_transformation`: Optional[str] (마지막 사용 알고리즘)
   - `search_filter`: str (현재 검색어)
   - `preserved_input`: str (창 숨김 시 입력 텍스트)
   - `preserved_output`: str (창 숨김 시 출력 텍스트)

3. **UIComponents (UI 구성 요소)**
   - `categories`: List[str] = ["Encoding", "Hash", "Text Processing", "Classical Ciphers"]
   - `algorithms`: Dict[str, List[str]] (카테고리별 알고리즘 맵)

4. **HotkeyConfiguration (핫키 설정)**
   - `key_combination`: str (기본: "Ctrl+.")
   - `action`: str ("toggle_visibility")

### 1.2 API Contracts (contracts/)

**contract/transformer_interface.md**:
```python
from abc import ABC, abstractmethod
from typing import Dict, Optional

class TransformerInterface(ABC):
    """모든 변환 알고리즘이 구현해야 하는 인터페이스"""

    @property
    def name(self) -> str:
        """알고리즘 이름 (예: 'Base64 Encode')"""
        pass

    @property
    def category(self) -> str:
        """카테고리 (Encoding, Hash, TextProcessing, Cipher)"""
        pass

    def transform(self, input_text: str, options: Dict[str, any] = None) -> str:
        """변환 실행

        Args:
            input_text: 사용자 입력 텍스트
            options: 알고리즘별 옵션 (可选)

        Returns:
            변환 결과 텍스트

        Raises:
            ValueError: 입력이 유효하지 않을 때
        """
        pass

    def validate_input(self, input_text: str) -> bool:
        """입력 유효성 검증"""
        pass
```

**contract/registry.md**:
```python
class AlgorithmRegistry:
    """알고리즘 등록 및 검색 시스템"""

    def register(self, transformer: TransformerInterface) -> None:
        """알고리즘 등록"""

    def get_all(self) -> Dict[str, List[TransformerInterface]]:
        """카테고리별 모든 알고리즘 반환"""

    def search(self, query: str) -> List[TransformerInterface]:
        """이름/카테고리/별칭으로 검색 (대소문자 구분 없음)"""

    def get_by_name(self, name: str) -> Optional[TransformerInterface]:
        """이름으로 알고리즘 조회"""
```

### 1.3 Quickstart Guide (quickstart.md)

**개발 환경 설정**:
```bash
# 1. Python 3.11+ 설치 확인
python --version

# 2. 가상 환경 생성 (권장)
python -m venv venv
venv\Scripts\activate  # Windows

# 3. 의존성 설치
pip install -r requirements.txt
# requirements.txt 내용:
# PySide6==6.6.0
# pynput==1.7.6
# pytest==7.4.3
# pytest-qt==4.2.0

# 4. 애플리케이션 실행
python src/main.py

# 5. 테스트 실행
pytest tests/ -v

# 6. .exe 빌드
pyinstaller build/encoder.spec
```

**코드 구조 빠른 이해**:
- `src/main.py`: `QApplication` 초기화, `MainWindow` 생성 및 실행
- `src/ui/main_window.py`: 메인 윈도우 레이아웃 (사이드바 + 컨텐츠 영역)
- `src/transformers/base.py`: `TransformerInterface` 추상 클래스
- `src/registry.py`: `AlgorithmRegistry` 싱글톤 인스턴스
- 각 변환기는 `transformers/base.py` 상속 및 `registry.register()` 등록

## Phase 2: Implementation Tasks

> **NOTE**: Phase 2는 `/speckit.tasks` 명령으로 `tasks.md` 생성 시 상세화됨
>
> 여기서는 User Story 기반 Task 구조만 개요적으로 제시

### Phase 2-1: Setup (공통 인프라)
- [ ] T001: 프로젝트 구조 생성 (src/, tests/, build/)
- [ ] T002: requirements.txt 작성 및 의존성 설치
- [ ] T003: pytest 설정 및 conftest.py 작성
- [ ] T004: PyInstaller spec 파일 작성

### Phase 2-2: Foundational (P1-P3 공통 기반)
- [ ] T005: TransformerInterface 추상 클래스 구현
- [ ] T006: AlgorithmRegistry 구현 (동적 로딩)
- [ ] T007: MainWindow 기본 레이아웃 (사이드바 + 컨텐츠 영역)
- [ ] T008: Sidebar 카테고리 트리 구현
- [ ] T009: ContentArea (입력/옵션/출력) 구현
- [ ] T010: GlobalHotkey listener (pynput 백그라운드 스레드)
- [ ] T011: SystemTrayIcon 구현

**Checkpoint**: P1-P3 기능을 위한 기반 완료

### Phase 2-3: User Story 1 - 기본 변환 (P1) 🎯 MVP
- [ ] T012: Base64 인코딩/디코딩 구현
- [ ] T013: URL 인코딩/디코딩 구현
- [ ] T014: Hex 인코딩/디코딩 구현
- [ ] T015: MD5 해시 구현
- [ ] T016: SHA-256 해시 구현
- [ ] T017: 복사 버튼 기능
- [ ] T018: P1 관련 유닛 테스트 작성

**Checkpoint**: 기본 변환 기능 MVP 완료

### Phase 2-4: User Story 2 - 핫키 (P2)
- [ ] T019: 핫키 Toggle 창 표시/숨김 로직
- [ ] T020: 창 상태 보존 (입력/출력 텍스트)
- [ ] T021: 포그라운드/백그라운드 전환

**Checkpoint**: 핫키 기능 완료

### Phase 2-5: User Story 3 - 시스템 트레이 (P3)
- [ ] T022: X 버튼 클릭 시 트레이로 최소화
- [ ] T023: 트레이 아이콘 더블 클릭으로 복원
- [ ] T024: Info/Exit 컨텍스트 메뉴

**Checkpoint**: 트레이 기능 완료

### Phase 2-6: User Story 4-6 - 확장 기능 (P4-P6)
- [ ] T025-T050: 고급 인코딩 (Base32, Base58, Base85, HTML Entities, Punycode, ...)
- [ ] T051-T070: 확장 해시 (SHA-1/224/384/512, SHA3, BLAKE2, ...)
- [ ] T071-T085: 텍스트 처리 (JSON/XML/YAML 포맷팅, Case 변환, ...)
- [ ] T086-T089: 클래식 암호 (ROT13, Caesar, Vigenère, Atbash)
- [ ] T090-T091: JWT 디코딩, 모스 부호
- [ ] T092-T100: 관련 유닛 테스트

### Phase 2-7: Polish & 배포
- [ ] T101: 검색 필터링 최적화 (0.3초 목표)
- [ ] T102: 한국어 에러 메시지 적용
- [ ] T103: 대용량 텍스트 처리 최적화 (10,000자 < 2초)
- [ ] T104: 핫키 설정 UI (P5)
- [ ] T105: Windows용 PyInstaller 빌드 (.exe)
- [ ] T106: macOS용 PyInstaller 빌드 (.app, Intel + Apple Silicon)
- [ ] T107: Linux용 PyInstaller 빌드 (binary)
- [ ] T108: 각 플랫폼별 실행 파일 테스트
- [ ] T109: 플랫폼별 시스템 트레이 동작 검증
- [ ] T110: 전체 유닛 테스트 실행 (100% 통과 확인)

## Success Metrics

- **MVP (P1-P3)**: Base64/URL/Hex 인코딩, MD5/SHA-256 해시, 핫키, 트레이 기능 작동
- **Algorithm Coverage**: 80+ 알고리즘 모두 구현 및 테스트
- **Performance**: 10,000자 텍스트 < 2초, 검색 < 0.3초, 핫키 < 0.5초
- **Quality**: 유닛 테스트 100% 통과, 한국어 에러 메시지
- **Multi-Platform Distribution**:
  - Windows: TextEncoder.exe (< 50MB 목표)
  - macOS: TextEncoder.app (Universal Binary 또는 별도 빌드, < 100MB 목표)
  - Linux: text-encoder binary (< 50MB 목표)
- **Cross-Platform Compatibility**: 모든 플랫폼에서 일관된 UI/UX 제공, 플랫폼별 네이티브 기능(시스템 트레이, 핫키) 정상 작동

## Next Steps

1. **Phase 0**: `research.md` 생성 (위 Research Tasks 상세화)
2. **Phase 1**: `data-model.md`, `contracts/`, `quickstart.md` 생성
3. **Phase 2**: `/speckit.tasks` 실행으로 `tasks.md` 생성 및 구현 착수
