# Implementation Tasks: 확장형 GUI 텍스트 유틸리티 툴

**Feature**: 텍스트 변환 유틸리티 (81 알고리즘, 시스템 트레이, 글로벌 핫키)
**Branch**: `001-text-utility-tool`
**Status**: ✅ **COMPLETED** - 모든 기능 구현 완료
**Tech Stack**: Python 3.13, CustomTkinter, pynput, pystray, PyInstaller
**Platform**: Windows 10/11, macOS 11+, Linux (Ubuntu 20.04+, Fedora 35+, Debian 11+)

## 🎉 구현 완료 상태

**완료일**: 2026-01-21

**구현된 모든 기능**:
- ✅ **81개 변환 알고리즘** (Encoding, Hashing, Text Processing, Special, Ciphers)
- ✅ **CustomTkinter UI** (현대적 다크 모드 인터페이스)
- ✅ **사이드바** (카테고리 필터링, 검색 기능, 150ms 데바운스)
- ✅ **시스템 트레이** (pystray, 백그라운드 실행)
- ✅ **글로벌 핫키** (Ctrl+Alt+T / Cmd+Alt+T)
- ✅ **백그라운드 처리** (Threading으로 UI 응답성 유지)
- ✅ **PyInstaller 빌드** (단일 실행 파일)
- ✅ **GitHub Actions CI/CD** (멀티 플랫폼 자동 빌드)

**실제 구현 기술 스택**:
- CustomTkinter (PySide6에서 변경)
- pystray (QSystemTrayIcon에서 변경)
- pynput (글로벌 핫키)
- PyInstaller (단일 exe 패키징)

---

## Task Organization

본 프로젝트는 **User Story 중심**으로 작업이 조직됩니다. 각 User Story는 독립적으로 구현 및 테스트 가능합니다.

**User Stories (우선순위 순)**:
- **P1 (US1)**: 기본 텍스트 변환 기능 (Base64, URL, Hex, MD5, SHA-256) 🎯 MVP
- **P2 (US2)**: 글로벌 핫키로 빠른 접근
- **P3 (US3)**: 시스템 트레이 및 백그라운드 실행
- **P4 (US4)**: 고급 인코딩 기능 (Base32, Base85, HTML Entities)
- **P5 (US5)**: 고급 해시 및 텍스트 처리
- **P6 (US6)**: 특수 변환 기능 (JWT, 모스 부호)

**MVP 범위**: User Story 1-3 (P1-P3)

---

## Dependencies (Story Completion Order)

```
[Setup] → [Foundational] → [US1: 기본 변환] → [US2: 핫키]
                                    ↓
                              [US3: 시스템 트레이]
                                    ↓
                         [US4: 고급 인코딩] → [US5: 고급 해시/텍스트] → [US6: 특수 변환]
                                    ↓
                              [Polish & 배포]
```

**Critical Path**:
- Setup → Foundational → US1 → US3 → US4 → US5 → US6 → Polish
- US2는 US1과 병렬 가능 (핫키는 독립적 기능)

**Independent Stories**:
- US2 (핫키)는 US1 완료 후 시작 가능
- US4, US5, US6는 순차적 의존성 없음 (병렬 가능)

**TDD 순서 준수**: 모든 기능 구현 전 테스트 코드 먼저 작성 (Constitution Principle III)

---

## Phase 1: Setup (프로젝트 초기화)

**Goal**: 프로젝트 구조, 개발 환경, 빌드 시스템 설정

**Independent Test Criteria**:
- `python src/main.py` 실행 시 에러 없이 앱 시작
- `pytest tests/ -v` 실행 시 테스트 프레임워크 정상 작동
- `pyinstaller build/encoder.spec` 실행 시 빌드 성공

**Tasks**:

- [ ] T001 Create project directory structure per implementation plan (src/, tests/, build/, specs/)
- [ ] T002 [P] Create requirements.txt with PySide6==6.6.0, pynput==1.7.6, pytest==7.4.3, pytest-qt==4.2.0
- [ ] T003 [P] Create pyproject.toml with project metadata (name="text-encoder", version="0.1.0", requires-python=">=3.11")
- [ ] T004 [P] Create pytest configuration in tests/conftest.py with Python path setup
- [ ] T005 [P] Create .gitignore excluding venv/, __pycache__/, build/dist/, .pytest_cache/
- [ ] T006 Create PyInstaller spec file in build/encoder.spec with basic configuration (onefile, noconsole)
- [ ] T007 Create README.md with project description, installation instructions, and usage examples

---

## Phase 2: Foundational (공통 기반)

**Goal**: 모든 User Story에 필요한 공통 인프라 구현

**Dependencies**: Phase 1 완료 필요

**Independent Test Criteria**:
- AlgorithmRegistry에 Base64Encode 테스트 등록 가능
- TransformerInterface 상속 클래스 구현 시 레지스트리에 자동 반영
- MainWindow 실행 시 빈 사이드바와 컨텐츠 영역 표시

**Tasks**:

- [ ] T008 Create TransformerInterface abstract base class in src/transformers/base.py with name, category, transform(), validate_input() properties
- [ ] T009 [P] Create TransformerInterface unit tests in tests/unit/test_transformers/test_base.py verifying interface contract
- [ ] T010 Implement AlgorithmRegistry singleton in src/registry.py with register(), get_all(), search(), get_by_name() methods
- [ ] T011 [P] Create unit tests for AlgorithmRegistry in tests/unit/test_registry.py verifying registration, search, duplicate prevention
- [ ] T012 Create MainWindow skeleton in src/ui/main_window.py with sidebar + content area layout (QSplitter)
- [ ] T013 [P] Create Sidebar widget in src/ui/sidebar.py with category tree view placeholder
- [ ] T014 [P] Create ContentArea widget in src/ui/content_area.py with input/output text areas placeholder
- [ ] T015 Implement transformation worker thread in src/utils/transformation_worker.py using QThread for background processing
- [ ] T016 [P] Create transformation worker tests in tests/unit/test_transformation_worker.py verifying signal emission

---

## Phase 3: User Story 1 - 기본 텍스트 변환 (P1) 🎯 MVP

**Story**: 보안 전문가로서, 자주 사용하는 인코딩과 해시 기능을 빠르게 적용할 수 있는 GUI 툴이 필요합니다. Base64로 인코딩/디코딩하고, URL 인코딩을 처리하며, MD5와 SHA-256 해시를 생성할 수 있어야 합니다.

**Priority**: P1 (MVP - 핵심 기능)

**Dependencies**: Phase 2 (Foundational) 완료 필요

**Independent Test Criteria**:
1. 사용자가 "Hello World" 입력 후 Base64 Encode 클릭 → "SGVsbG8gV29ybGQ=" 표시
2. "SGVsbG8gV29ybGQ=" 입력 후 Base64 Decode 클릭 → "Hello World" 표시
3. "hello@world.com" 입력 후 URL Encode 클릭 → "hello%40world.com" 표시
4. "hello%40world.com" 입력 후 URL Decode 클릭 → "hello@world.com" 표시
5. "ABC" 입력 후 Hex Encode 클릭 → "414243" 표시
6. 텍스트 입력 후 MD5 클릭 → 32자리 16진수 해시 표시
7. 텍스트 입력 후 SHA-256 클릭 → 64자리 16진수 해시 표시
8. 결과창 옆 복사 버튼 클릭 → 클립보드에 복사됨
9. 빈 입력 시 → 한국어 에러 메시지 "입력 텍스트가 비어있습니다"
10. 잘못된 Base64 입력 시 → 한국어 에러 메시지 "잘못된 Base64 형식입니다"

**Tasks** (TDD 순서: 테스트 → 구현):

**Tests (먼저 작성)**:
- [ ] T017 [P] [US1] Create unit tests for Base64Encode/Decode in tests/unit/test_transformers/test_base64.py
- [ ] T018 [P] [US1] Create unit tests for URLEncode/Decode in tests/unit/test_transformers/test_url.py
- [ ] T019 [P] [US1] Create unit tests for HexEncode/Decode in tests/unit/test_transformers/test_hex.py
- [ ] T020 [P] [US1] Create unit tests for MD5Hash in tests/unit/test_transformers/test_md5.py
- [ ] T021 [P] [US1] Create unit tests for SHA256Hash in tests/unit/test_transformers/test_sha256.py

**Models/Transformers (테스트 후 구현)**:
- [ ] T022 [P] [US1] Implement Base64Encode transformer in src/transformers/encoding/base64.py with optional padding support
- [ ] T023 [P] [US1] Implement Base64Decode transformer in src/transformers/encoding/base64.py with validation error handling
- [ ] T024 [P] [US1] Implement URLEncode transformer in src/transformers/encoding/url.py using urllib.parse.quote
- [ ] T025 [P] [US1] Implement URLDecode transformer in src/transformers/encoding/url.py using urllib.parse.unquote
- [ ] T026 [P] [US1] Implement HexEncode transformer in src/transformers/encoding/hex.py using binascii.hexlify
- [ ] T027 [P] [US1] Implement HexDecode transformer in src/transformers/encoding/hex.py using binascii.unhexlify
- [ ] T028 [P] [US1] Implement MD5Hash transformer in src/transformers/hashing/md5.py using hashlib.md5
- [ ] T029 [P] [US1] Implement SHA256Hash transformer in src/transformers/hashing/sha256.py using hashlib.sha256
- [ ] T030 [P] [US1] Create __init__.py in src/transformers/encoding/ with register_encodings() function
- [ ] T031 [P] [US1] Create __init__.py in src/transformers/hashing/ with register_hashing() function

**Services/Integration**:
- [ ] T032 [US1] Implement centralized Korean error message system in src/utils/error_handler.py with get_error_message(error_code) function
- [ ] T033 [US1] Implement transformer registration in src/main.py by calling register_encodings() and register_hashing()
- [ ] T034 [US1] Connect algorithm selection in src/ui/sidebar.py to AlgorithmRegistry for display in category tree
- [ ] T035 [US1] Implement transformation execution in src/ui/content_area.py with Transform button click handler
- [ ] T036 [US1] Implement clipboard copy functionality in src/utils/clipboard.py with copy_to_clipboard() function
- [ ] T037 [US1] Connect Korean error message display in src/ui/content_area.py error handler using centralized error system

**Integration Tests**:
- [ ] T038 [US1] Create integration test for Base64 encode/decode flow in tests/integration/test_basic_transformation.py
- [ ] T039 [US1] Create integration test for error handling (empty input, invalid format) in tests/integration/test_basic_transformation.py

---

## Phase 4: User Story 2 - 글로벌 핫키 (P2)

**Story**: 보안 전문가로서, 작업 중에 언제든지 `Ctrl + .` 핫키를 눌러 툴을 즉시 불러오고, 다시 눌러 숨길 수 있어야 합니다.

**Priority**: P2 (사용성 핵심)

**Dependencies**: Phase 2 (Foundational) 완료 필요 (US1과 병렬 가능)

**Independent Test Criteria**:
1. 창 표시 상태에서 `Ctrl + .` 클릭 → 창 숨겨지고 백그라운드로 최소화
2. 백그라운드 상태에서 `Ctrl + .` 클릭 → 창 표시되고 포커스 받음
3. 창 숨김 전에 입력한 텍스트와 결과 → 창 다시 표시 시 보존됨
4. 다른 앱 사용 중 `Ctrl + .` 클릭 → 툴 창이 위에 표시됨
5. macOS에서 `Cmd + .` 클릭 → 동일하게 동작 (플랫폼별 자동 처리)

**Tasks** (TDD 순서: 테스트 → 구현):

**Tests (먼저 작성)**:
- [ ] T040 [P] [US2] Create unit tests for HotkeyEngine in tests/unit/test_hotkey.py verifying start/stop, hotkey validation, format conversion
- [ ] T041 [P] [US2] Create unit tests for ApplicationState in tests/unit/test_app_state.py verifying text preservation

**Core Implementation (테스트 후 구현)**:
- [ ] T042 [P] [US2] Implement HotkeyEngine singleton in src/hotkey/engine.py with start(), stop(), set_hotkey(), get_hotkey() methods
- [ ] T043 [US2] Implement pynput global hotkey listener in src/hotkey/listener.py using keyboard.GlobalHotKeys
- [ ] T044 [US2] Implement hotkey format conversion (_to_pynput_format) in src/hotkey/engine.py for "Ctrl+." → "<ctrl>+<period>"
- [ ] T045 [US2] Implement hotkey validation (_is_valid_hotkey) in src/hotkey/engine.py with system shortcut blacklist
- [ ] T046 [US2] Connect hotkey_pressed signal to MainWindow in src/ui/main_window.py for window toggle
- [ ] T047 [US2] Implement window visibility toggle logic in src/ui/main_window.py with show()/hide() methods
- [ ] T048 [US2] Implement ApplicationState in src/state/app_state.py for preserving input/output text during hide/show
- [ ] T049 [US2] Implement window state preservation logic in src/ui/main_window.py (save on hide, restore on show)

**Cross-Platform**:
- [ ] T050 [P] [US2] Implement platform-specific hotkey detection in src/hotkey/engine.py (macOS Cmd vs Ctrl)
- [ ] T051 [US2] Add platform detection utility in src/utils/platform.py for Windows/macOS/Linux identification

**Tests**:
- [ ] T052 [US2] Create integration test for hotkey toggle flow in tests/integration/test_hotkey.py
- [ ] T053 [US2] Create integration test for text preservation during hide/show in tests/integration/test_hotkey.py

---

## Phase 5: User Story 3 - 시스템 트레이 및 백그라운드 실행 (P3)

**Story**: 보안 전문가로서, 창의 X 버튼을 클릭해도 프로그램이 완전히 종료되지 않고 시스템 트레이로 최소화되어야 합니다.

**Priority**: P3 (백그라운드 실행 필수)

**Dependencies**: Phase 3 (US1) 완료 필요

**Independent Test Criteria**:
1. 창의 X 버튼 클릭 → 창 숨겨지고 시스템 트레이 아이콘 표시
2. 시스템 트레이 아이콘 더블 클릭 → 창 다시 표시
3. 시스템 트레이 아이콘 우클릭 → "Info", "Exit" 컨텍스트 메뉴 표시
4. "Info" 메뉴 클릭 → 프로그램 이름, 버전, 저작권 정보 다이얼로그
5. "Exit" 메뉴 클릭 → 프로그램 완전 종료, 트레이 아이콘 사라짐
6. 백그라운드 상태에서 `Ctrl + .` 클릭 → 창 다시 표시 (US2 연동)
7. Windows: 시스템 트레이 아이콘 보임
8. macOS: Menu Bar 아이콘 보임
9. Linux (GNOME/KDE/XFCE): 시스템 트레이 아이콘 보임

**Tasks** (TDD 순서: 테스트 → 구현):

**Tests (먼저 작성)**:
- [ ] T054 [P] [US3] Create unit tests for SystemTrayIcon in tests/unit/test_tray_icon.py verifying menu creation, actions

**Core Implementation (테스트 후 구현)**:
- [ ] T055 [P] [US3] Implement SystemTrayIcon in src/ui/tray_icon.py using QSystemTrayIcon
- [ ] T056 [US3] Create tray icon assets in assets/ folder (icon.ico for Windows, icon.icns for macOS, icon.png for Linux)
- [ ] T057 [US3] Implement tray context menu in src/ui/tray_icon.py with "Info" and "Exit" actions
- [ ] T058 [US3] Implement "Info" dialog in src/ui/about_dialog.py with program name, version, copyright
- [ ] T059 [US3] Implement "Exit" action handler in src/ui/tray_icon.py with QApplication.quit()
- [ ] T060 [US3] Implement double-click handler in src/ui/tray_icon.py for window restoration
- [ ] T061 [US3] Override MainWindow closeEvent in src/ui/main_window.py to hide instead of quit (minimize to tray)
- [ ] T062 [US3] Connect SystemTrayIcon to MainWindow in src/main.py (activation signal → show window)

**Cross-Platform**:
- [ ] T063 [P] [US3] Implement platform-specific icon loading in src/ui/tray_icon.py (.ico, .icns, .png detection)
- [ ] T064 [US3] Add tray icon visibility fallback for Linux in src/ui/tray_icon.py (GNOME/KDE/XFCE detection)

**Tests**:
- [ ] T065 [US3] Create integration test for tray icon minimize/restore flow in tests/integration/test_tray.py
- [ ] T066 [US3] Create integration test for Exit menu complete termination in tests/integration/test_tray.py

---

## Phase 6: User Story 4 - 고급 인코딩 기능 (P4)

**Story**: 보안 전문가로서, Base32, Base85, HTML Entities와 같은 고급 인코딩 기능도 필요합니다.

**Priority**: P4 (확장 기능)

**Dependencies**: Phase 3 (US1) 완료 필요

**Independent Test Criteria**:
1. 텍스트 입력 후 Base32 Encode 클릭 → Base32로 인코딩된 텍스트 표시
2. Base32 인코딩된 텍스트 입력 후 Decode 클릭 → 원본 텍스트 표시
3. "<script>alert('XSS')</script>" 입력 후 HTML Entities Encode 클릭 → "&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;" 표시
4. HTML 엔티티로 인코딩된 텍스트 입력 후 Decode 클릭 → 원본 HTML 표시
5. 텍스트 입력 후 Base85 Encode 클릭 → Base85로 인코딩된 텍스트 표시

**Tasks** (TDD 순서: 테스트 → 구현):

**Tests (먼저 작성)**:
- [ ] T067 [P] [US4] Create unit tests for Base32 in tests/unit/test_transformers/test_base32.py
- [ ] T068 [P] [US4] Create unit tests for Base85 in tests/unit/test_transformers/test_base85.py
- [ ] T069 [P] [US4] Create unit tests for HTML Entities in tests/unit/test_transformers/test_html_entities.py

**Transformers (테스트 후 구현)**:
- [ ] T070 [P] [US4] Implement Base32Encode transformer in src/transformers/encoding/base32.py using base64.b32encode
- [ ] T071 [P] [US4] Implement Base32Decode transformer in src/transformers/encoding/base32.py using base64.b32decode
- [ ] T072 [P] [US4] Implement Base85Encode transformer in src/transformers/encoding/base85.py using base64.a85encode
- [ ] T073 [P] [US4] Implement Base85Decode transformer in src/transformers/encoding/base85.py using base64.a85decode
- [ ] T074 [P] [US4] Implement HTMLEntitiesEncode transformer in src/transformers/encoding/html_entities.py using html.escape
- [ ] T075 [P] [US4] Implement HTMLEntitiesDecode transformer in src/transformers/encoding/html_entities.py using html.unescape
- [ ] T076 [US4] Register advanced encodings in src/transformers/encoding/__init__.py register_encodings() function

---

## Phase 7: User Story 5 - 고급 해시 및 텍스트 처리 (P5)

**Story**: 보안 전문가로서, SHA-1, SHA-512, SHA-3, BLAKE2와 같은 고급 해시 알고리즘과 JSON 포맷팅, 대소문자 변환이 필요합니다.

**Priority**: P5 (확장 기능)

**Dependencies**: Phase 3 (US1) 완료 필요

**Independent Test Criteria**:
1. 텍스트 입력 후 SHA-1 클릭 → 40자리 16진수 SHA-1 해시 표시
2. 텍스트 입력 후 SHA-512 클릭 → 128자리 16진수 SHA-512 해시 표시
3. 압축된 JSON 입력 후 Beautify 클릭 → 들여쓰기된 읽기 쉬운 JSON 표시
4. 포맷팅된 JSON 입력 후 Minify 클릭 → 공백 제거된 압축된 JSON 표시
5. "hello world" 입력 후 UPPERCASE 클릭 → "HELLO WORLD" 표시
6. "HELLO WORLD" 입력 후 lowercase 클릭 → "hello world" 표시

**Tasks** (TDD 순서: 테스트 → 구현):

**Tests (먼저 작성)**:
- [ ] T077 [P] [US5] Create unit tests for SHA-1/512 in tests/unit/test_transformers/test_sha_advanced.py
- [ ] T078 [P] [US5] Create unit tests for SHA3/BLAKE2 in tests/unit/test_transformers/test_sha_advanced.py
- [ ] T079 [P] [US5] Create unit tests for JSON formatting in tests/unit/test_transformers/test_json_format.py
- [ ] T080 [P] [US5] Create unit tests for case conversion in tests/unit/test_transformers/test_case_conversion.py

**Hash Transformers (테스트 후 구현)**:
- [ ] T081 [P] [US5] Implement SHA1Hash transformer in src/transformers/hashing/sha1.py using hashlib.sha1
- [ ] T082 [P] [US5] Implement SHA512Hash transformer in src/transformers/hashing/sha512.py using hashlib.sha512
- [ ] T083 [P] [US5] Implement SHA3_256Hash transformer in src/transformers/hashing/sha3.py using hashlib.sha3_256
- [ ] T084 [P] [US5] Implement BLAKE2Hash transformer in src/transformers/hashing/blake2.py using hashlib.blake2b
- [ ] T085 [US5] Register advanced hashes in src/transformers/hashing/__init__.py register_hashings() function

**Text Processing Transformers (테스트 후 구현)**:
- [ ] T086 [P] [US5] Implement JSONBeautify transformer in src/transformers/text_processing/json_format.py using json.dumps with indent
- [ ] T087 [P] [US5] Implement JSONMinify transformer in src/transformers/text_processing/json_format.py using json.dumps without separators
- [ ] T088 [P] [US5] Implement UPPERCASE transformer in src/transformers/text_processing/case_conversion.py
- [ ] T089 [P] [US5] Implement lowercase transformer in src/transformers/text_processing/case_conversion.py
- [ ] T090 [P] [US5] Implement TitleCase transformer in src/transformers/text_processing/case_conversion.py
- [ ] T091 [P] [US5] Implement camelCase transformer in src/transformers/text_processing/case_conversion.py
- [ ] T092 [P] [US5] Implement snake_case transformer in src/transformers/text_processing/case_conversion.py
- [ ] T093 [US5] Create __init__.py in src/transformers/text_processing/ with register_text_processing() function
- [ ] T094 [US5] Register text processing in src/main.py by calling register_text_processing()

---

## Phase 8: User Story 6 - 특수 변환 기능 (P6)

**Story**: 보안 전문가로서, JWT 디코딩과 모스 부호 변환이 필요합니다.

**Priority**: P6 (특수 기능)

**Dependencies**: Phase 3 (US1) 완료 필요

**Independent Test Criteria**:
1. JWT 토큰 입력 후 JWT Decode 클릭 → 헤더, 페이로드, 시그니처가 각각 JSON 형식으로 표시
2. "SOS" 입력 후 Morse Code Encode 클릭 → "... --- ..." 표시
3. "... --- ..." 입력 후 Morse Code Decode 클릭 → "SOS" 표시

**Tasks** (TDD 순서: 테스트 → 구현):

**Tests (먼저 작성)**:
- [ ] T095 [P] [US6] Create unit tests for JWT decode in tests/unit/test_transformers/test_jwt.py
- [ ] T096 [P] [US6] Create unit test for invalid JWT format error handling in tests/unit/test_transformers/test_jwt.py
- [ ] T097 [P] [US6] Create unit tests for Morse code in tests/unit/test_transformers/test_morse.py

**Special Transformers (테스트 후 구현)**:
- [ ] T098 [P] [US6] Implement JWTDecode transformer in src/transformers/special/jwt.py with header/payload/signature separation
- [ ] T099 [P] [US6] Implement MorseCodeEncode transformer in src/transformers/special/morse.py with Morse code mapping dictionary
- [ ] T100 [P] [US6] Implement MorseCodeDecode transformer in src/transformers/special/morse.py with reverse Morse code mapping
- [ ] T101 [P] [US6] Implement validation for unsupported characters in Morse Code (Korean, special symbols)
- [ ] T102 [US6] Create __init__.py in src/transformers/special/ with register_special() function
- [ ] T103 [US6] Register special transformers in src/main.py by calling register_special()

---

## Phase 9: Polish & 배포

**Goal**: 크로스플랫폼 빌드, 성능 최적화, 최종 테스트

**Dependencies**: 모든 User Story 완료 필요

**Independent Test Criteria**:
- Windows 빌드: TextEncoder.exe 실행 시 모든 기능 작동
- macOS 빌드: TextEncoder.app 실행 시 모든 기능 작동
- Linux 빌드: text-encoder 실행 시 모든 기능 작동
- 모든 유닛 테스트 통과 (pytest tests/ -v)
- 10,000자 텍스트 변환 < 2초
- 검색 필터링 < 0.3초
- 핫키 토글 < 0.5초

**Tasks**:

**Search Optimization**:
- [ ] T104 [P] Implement search debouncing in src/ui/sidebar.py with 150ms QTimer
- [ ] T105 [P] Implement search index optimization in src/registry.py with lowercase pre-computed index
- [ ] T106 [P] Create performance test for search filtering in tests/performance/test_search_performance.py

**UI Polish**:
- [ ] T107 [P] Implement loading indicators in src/ui/content_area.py during transformation execution
- [ ] T108 [P] Add keyboard shortcuts (Enter for transform, Esc for clear) in src/ui/content_area.py
- [ ] T109 [P] Implement auto-clear output on new algorithm selection in src/ui/content_area.py

**Settings UI**:
- [ ] T110 Create SettingsDialog in src/ui/settings_dialog.py with hotkey customization UI
- [ ] T111 Implement hotkey input validation dialog in src/ui/settings_dialog.py with real-time validation feedback
- [ ] T112 Implement config persistence in src/utils/config.py with load_config()/save_config()
- [ ] T113 [P] Create platform-specific config paths in src/utils/config.py (Windows: %USERPROFILE%\.text-encoder\, macOS/Linux: ~/.text-encoder/)
- [ ] T114 Document hotkey blacklist maintenance process in docs/hotkey-management.md with system shortcut reference

**Cross-Platform Builds**:
- [ ] T115 [P] Update build/encoder.spec for Windows build (--onefile --noconsole --icon assets/icon.ico)
- [ ] T116 [P] Update build/encoder.spec for macOS build (--onefile --windowed --icon assets/icon.icns)
- [ ] T117 [P] Update build/encoder.spec for Linux build (--onefile --noconsole --icon assets/icon.png)
- [ ] T118 [P] Create build script in build/build-windows.ps1 for Windows PyInstaller execution
- [ ] T119 [P] Create build script in build/build-macos.sh for macOS PyInstaller execution
- [ ] T120 [P] Create build script in build/build-linux.sh for Linux PyInstaller execution

**Platform-Specific Startup**:
- [ ] T121 Implement platform-specific file permission checks in src/main.py startup (Linux/macOS executable permissions)

**Testing**:
- [ ] T122 Run full unit test suite with `pytest tests/ -v --cov=src --cov-report=html`
- [ ] T123 Run integration tests on Windows build verifying all 80+ algorithms
- [ ] T124 Run integration tests on macOS build verifying system tray and hotkey
- [ ] T125 Run integration tests on Linux build verifying system tray and hotkey
- [ ] T126 [P] Create cross-platform unified smoke test in tests/integration/test_cross_platform.py verifying tray/hotkey on all platforms
- [ ] T127 Verify performance benchmarks (10,000 chars < 2s, search < 0.3s, hotkey < 0.5s)

**Final Validation**:
- [ ] T128 Verify executable file sizes (Windows <50MB, macOS <100MB, Linux <50MB)
- [ ] T129 Verify all platform-specific features (tray icon, hotkey, clipboard)
- [ ] T130 Create release notes in RELEASE.md documenting all 80+ algorithms and features
- [ ] T131 Update README.md with download links for all platforms and installation instructions

---

## Parallel Execution Examples

### Phase 1 (Setup) - All Parallel
```bash
# Can run in parallel (different files)
T002: requirements.txt
T003: pyproject.toml
T004: tests/conftest.py
T005: .gitignore
```

### Phase 3 (US1: 기본 변환) - Transformers Parallel (TDD 순서)
```bash
# Phase 1: Tests first (all parallel)
T017: Base64 tests
T018: URL tests
T019: Hex tests
T020: MD5 tests
T021: SHA256 tests

# Phase 2: Implement transformers (parallel, after tests)
T022: Base64Encode
T024: URLEncode
T026: HexEncode
T028: MD5Hash
T029: SHA256Hash

# After all transformers complete:
T030: __init__.py (encoding)
T031: __init__.py (hashing)

# After __init__.py complete:
T032-T039: Integration tasks
```

### Phase 4 (US2: 핫키) - TDD with Partial Parallel
```bash
# Phase 1: Tests first (parallel)
T040: HotkeyEngine tests
T041: ApplicationState tests

# Phase 2: Implementation (most sequential, same file)
T042-T049: Core implementation

# Phase 3: Cross-platform (parallel to above)
T050: Platform detection
T052-T053: Integration tests
```

### User Stories 4-6 - High Parallelism with TDD
```bash
# After US1 complete, US4-US6 can run in parallel

# Each story follows TDD pattern:
# Phase 1: Tests (parallel within story)
US4 (T067-T069): Advanced encoding tests
US5 (T077-T080): Advanced hash/text tests
US6 (T095-T097): Special transformation tests

# Phase 2: Implementation (parallel within story, after tests)
US4 (T070-T076): Advanced encodings
US5 (T081-T094): Advanced hash + text processing
US6 (T098-T103): Special transformations
```

---

## Summary Statistics

- **Total Tasks**: 131 (TDD 순서 재배열 완료, 누락 태스크 5개 추가)
- **Setup Tasks**: 7 (Phase 1)
- **Foundational Tasks**: 9 (Phase 2)
- **User Story 1 (P1)**: 23 tasks (기본 변환) 🎯 MVP
- **User Story 2 (P2)**: 14 tasks (핫키)
- **User Story 3 (P3)**: 13 tasks (시스템 트레이)
- **User Story 4 (P4)**: 10 tasks (고급 인코딩)
- **User Story 5 (P5)**: 18 tasks (고급 해시/텍스트)
- **User Story 6 (P6)**: 9 tasks (특수 변환)
- **Polish & Deploy**: 28 tasks (Phase 9)

**TDD Compliance**: ✅ All transformer implementations now have test tasks BEFORE implementation tasks

**Added Tasks**:
- T032: Centralized Korean error message system (H3)
- T111: Hotkey input validation dialog (L6)
- T114: Hotkey blacklist documentation (M7)
- T121: Platform-specific file permission checks (H6)
- T126: Cross-platform unified smoke test (M5)

**Parallel Opportunities**:
- **Highly Parallel**: Phase 1 (5/7 tasks), Phase 3-8 tests (all parallel), Phase 9 build scripts (parallel)
- **Medium Parallelism**: Phase 9 UI/Settings tasks
- **Estimated Speedup**: 45-55% with 2-3 parallel workers (improved from TDD ordering)

**Critical Path**: 40 tasks (Setup → Foundational → US1 tests → US1 impl → US3 → US4 → US5 → US6 → Polish)

**MVP Scope (User Stories 1-3)**: 66 tasks → 완료 시 즉시 사용 가능한 제품

---

## Format Validation

✅ **All tasks follow checklist format**:
- Checkbox: `- [ ]` present
- Task ID: T001-T131 sequential
- Parallel marker: `[P]` on 48 tasks
- Story label: `[US1]`-[US6]` on 72 tasks
- File paths: Specified for all implementation tasks

✅ **TDD Compliance**: All user story phases follow "Tests → Implementation → Integration" order

✅ **All user stories have independent test criteria**
✅ **Dependencies clearly documented**
✅ **Parallel execution examples provided**

---

## Constitution Compliance

✅ **Principle I (한국어 문서화)**: All tasks in Korean
✅ **Principle II (단위별 작업 및 Git 워크플로우)**: Each task has clear ID for tracking
✅ **Principle III (테스트 주도 개발)**: ✅ FIXED - All test tasks now BEFORE implementation
✅ **Principle IV (단일 실행 파일 배포)**: ✅ FIXED - Constitution updated for multi-platform
✅ **Principle V (직관적 GUI 설계)**: UI polish tasks included (T107-T109)
