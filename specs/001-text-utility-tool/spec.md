# Feature Specification: 확장형 GUI 텍스트 유틸리티 툴

**Feature Branch**: `001-text-utility-tool`
**Created**: 2026-01-21
**Status**: Draft
**Input**: User description: "확장형 GUI 텍스트 유틸리티 툴: 인코딩/디코딩/해시 기능, 백그라운드 실행, 시스템 트레이, 글로벌 핫키 지원"

## Feature Overview

이 툴은 보안 전문가와 개발자를 위한 포괄적인 텍스트 변환 유틸리티입니다. 80개 이상의 변환 알고리즘을 제공하며, 백그라운드 실행과 글로벌 핫키로 빠른 접근성을 제공합니다.

### 1.1 Encoding / Decoding (인코딩/디코딩)

**Standard (표준):**
- Base64, URL Encoding, Hex (16진수)

**검색 기능**:
- 알고리즘 이름/카테고리로 실시간 필터링 (150ms 데바운스 타이머 적용)

**Advanced Base (확장 Base):**
- Base16, Base32, Base32Hex, Base58 (Bitcoin), Base62, Base85 (ASCII85), Base91

**Web & Programming (웹 및 프로그래밍):**
- HTML Entities (Encode/Decode), Punycode (IDN), JWT (Header/Payload Decode), Unicode Escape (\uXXXX), Quoted-Printable

**Representations (표현형식):**
- Binary (2진수), Octal (8진수), Decimal (10진수)

**Special (특수):**
- Morse Code (모스 부호), Braille (점자)

### 1.2 Hashing (Checksum & Crypto)

**MD Family:**
- MD2, MD4, MD5

**SHA Family:**
- SHA-1, SHA-224, SHA-256, SHA-384, SHA-512, SHA-512/224, SHA-512/256

**SHA-3 Family:**
- SHA3-224, SHA3-256, SHA3-384, SHA3-512, Keccak-256

**Secure Hashes (보안 해시):**
- BLAKE2s, BLAKE2b, RIPEMD-160, Whirlpool

**Checksums (체크섬):**
- CRC32, Adler32

### 1.3 Text Processing & Formatting (텍스트 처리 및 포맷팅)

**Formatters (포맷터):**
- JSON Beautify/Minify, XML Pretty Print, YAML Format, SQL Minify

**Case Conversion (대소문자 변환):**
- UPPERCASE, lowercase, Title Case, camelCase, snake_case, PascalCase, Kebab-Case

**Cleaning (데이터 정리):**
- Remove Duplicates, Sort Lines (Asc/Desc), Remove Empty Lines, Strip Whitespace

**Escaping (이스케이프):**
- C-Style String Escape, Shell Escape

### 1.4 Classical Ciphers (클래식 암호)

- ROT13, Caesar Cipher, Vigenère Cipher, Atbash Cipher

### 2. 시스템 제어 및 UX

**창 제어 (Window Control):**
- 'X' 버튼 클릭 시 시스템 트레이로 이동 (백그라운드 유지)

**트레이 메뉴 (Tray Menu):**
- `Info`: 프로그램 버전 및 정보 표시
- `Exit`: 프로그램 완전 종료

**글로벌 핫키 (Global Hotkey):**
- `Ctrl + .` 키로 창 Show/Hide 전환

**편의 기능 (Convenience Features):**
- 알고리즘 검색 필터링 기능 (방대한 알고리즘 빠른 찾기)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 기본 텍스트 변환 기능 (Priority: P1)

보안 전문가로서, 자주 사용하는 인코딩과 해시 기능을 빠르게 적용할 수 있는 GUI 툴이 필요합니다. Base64로 인코딩/디코딩하고, URL 인코딩을 처리하며, MD5와 SHA-256 해시를 생성할 수 있어야 합니다.

**Why this priority**: 이것이 툴의 핵심 기능입니다. 기본 변환 기능 없이는 다른 모든 기능이 무의미하며, 이 기능만으로도 즉시 실무에서 활용 가능한 MVP를 제공합니다. 보안 전문가들은 매일 이러한 기본 변환 작업을 수행합니다.

**Independent Test**: 텍스트 입력창에 문자열을 입력하고, Base64 Encode/Decode 버튼, URL Encode/Decode 버튼, Hex Encode/Decode 버튼을 각각 클릭하여 결과창에 정확한 변환 결과가 출력되는지 확인. MD5와 SHA-256 해시 생성 버튼을 클릭하여 해시값이 올바르게 생성되는지 확인. 모든 기능이 독립적으로 작동하며 실무에서 즉시 사용 가능합니다.

**Acceptance Scenarios**:

1. **Given** 사용자가 텍스트 입력창에 "Hello World"를 입력하고 Base64 Encode 버튼을 클릭하면, **When** 변환이 실행되고, **Then** 결과창에 "SGVsbG8gV29ybGQ="가 표시된다
2. **Given** 사용자가 입력창에 "SGVsbG8gV29ybGQ="를 입력하고 Base64 Decode 버튼을 클릭하면, **When** 디코딩이 실행되고, **Then** 결과창에 "Hello World"가 표시된다
3. **Given** 사용자가 "hello@world.com"을 입력하고 URL Encode 버튼을 클릭하면, **When** 인코딩이 실행되고, **Then** 결과창에 "hello%40world.com"이 표시된다
4. **Given** 사용자가 "hello%40world.com"을 입력하고 URL Decode 버튼을 클릭하면, **When** 디코딩이 실행되고, **Then** 결과창에 "hello@world.com"이 표시된다
5. **Given** 사용자가 텍스트를 입력하고 MD5 해시 버튼을 클릭하면, **When** 해시가 생성되고, **Then** 결과창에 32자리 16진수 MD5 해시값이 표시된다
6. **Given** 사용자가 텍스트를 입력하고 SHA-256 해시 버튼을 클릭하면, **When** 해시가 생성되고, **Then** 결과창에 64자리 16진수 SHA-256 해시값이 표시된다
7. **Given** 사용자가 "ABC"를 입력하고 Hex Encode 버튼을 클릭하면, **When** 인코딩이 실행되고, **Then** 결과창에 "414243"이 표시된다
8. **Given** 사용자가 결과값을 복사하기 위해 복사 버튼을 클릭하면, **When** 클립보드에 복사되고, **Then** 다른 애플리케이션에서 붙여넣기 할 수 있다

---

### User Story 2 - 글로벌 핫키로 빠른 접근 (Priority: P2)

보안 전문가로서, 작업 중에 언제든지 `Ctrl + .` 핫키를 눌러 툴을 즉시 불러오고, 다시 눌러 숨길 수 있어야 합니다. 핫키로 프로그램을 빠르게 표시하고 숨겨서 작업 흐름을 중단하지 않고 계속 작업할 수 있어야 합니다.

**Why this priority**: 핫키는 이 툴의 핵심 사용성 요구사항입니다. 보안 전문가들은 여러 도구를 동시에 사용하며 빠르게 전환해야 합니다. 핫키가 없으면 매번 툴을 찾아 클릭해야 하므로 생산성이 크게 떨어집니다. 핫키 기능만으로도 툴의 사용성이 획기적으로 개선됩니다.

**Independent Test**: 프로그램이 실행 중인 상태에서 `Ctrl + .` 키를 누르면 창이 표시되고, 다시 `Ctrl + .` 키를 누르면 창이 숨겨지는지 확인. 창이 숨겨진 상태에서도 백그라운드에서 실행 중이며 핫키로 다시 불러올 수 있는지 확인. 이 기능만으로도 툴의 접근성이 크게 향상됩니다.

**Acceptance Scenarios**:

1. **Given** 프로그램이 실행 중이고 창이 표시된 상태에서, **When** 사용자가 `Ctrl + .` 키를 누르면, **Then** 창이 즉시 숨겨지고 백그라운드로 최소화된다
2. **Given** 프로그램이 백그라운드에서 실행 중인 상태에서, **When** 사용자가 `Ctrl + .` 키를 누르면, **Then** 창이 즉시 표시되고 포커스를 받는다
3. **Given** 창이 숨겨진 상태에서, **When** 사용자가 핫키를 눌러 창을 다시 표시하면, **Then** 이전에 입력한 텍스트와 결과가 그대로 유지된다
4. **Given** 사용자가 다른 애플리케이션을 사용 중일 때, **When** `Ctrl + .` 키를 누르면, **Then** 현재 작업을 중단하지 않고 툴 창이 위에 표시된다

---

### User Story 3 - 시스템 트레이 및 백그라운드 실행 (Priority: P3)

보안 전문가로서, 창의 X 버튼을 클릭해도 프로그램이 완전히 종료되지 않고 시스템 트레이로 최소화되어야 합니다. 트레이 아이콘을 통해 프로그램 정보를 확인하고 완전히 종료할 수 있어야 합니다.

**Why this priority**: 백그라운드 실행은 핫키 기능의 필수 전제 조건입니다. 사용자가 창을 닫아도 프로그램이 계속 실행되어야 핫키로 다시 불러올 수 있습니다. 시스템 트레이는 백그라운드 실행 상태를 시각적으로 표현하고 프로그램 제어를 제공합니다.

**Independent Test**: 창의 X 버튼을 클릭했을 때 창이 숨겨지고 시스템 트레이에 아이콘이 나타나는지 확인. 트레이 아이콘을 우클릭하여 메뉴가 표시되는지 확인. Info 메뉴를 클릭하여 프로그램 정보가 표시되는지 확인. Exit 메뉴를 클릭하여 프로그램이 완전히 종료되는지 확인. 이 기능만으로도 백그라운드 실행이 완벽하게 구현됩니다.

**Acceptance Scenarios**:

1. **Given** 프로그램이 실행 중일 때, **When** 사용자가 창의 X 버튼을 클릭하면, **Then** 창이 숨겨지고 시스템 트레이에 아이콘이 표시된다
2. **Given** 프로그램이 시스템 트레이에 있을 때, **When** 사용자가 트레이 아이콘을 더블 클릭하면, **Then** 창이 다시 표시된다
3. **Given** 시스템 트레이 아이콘을 우클릭했을 때, **When** 컨텍스트 메뉴가 표시되고, **Then** "Info", "Exit" 메뉴 항목이 포함되어 있다
4. **Given** 컨텍스트 메뉴에서 "Info"를 클릭했을 때, **When** 정보 다이얼로그가 표시되고, **Then** 프로그램 이름, 버전, 저작권 정보가 표시된다
5. **Given** 컨텍스트 메뉴에서 "Exit"를 클릭했을 때, **When** 프로그램이 종료되고, **Then** 시스템 트레이에서 아이콘이 사라진다
6. **Given** 프로그램이 시스템 트레이에 있을 때, **When** `Ctrl + .` 핫키를 누르면, **Then** 창이 다시 표시된다

---

### User Story 4 - 고급 인코딩 기능 (Priority: P4)

보안 전문가로서, Base32, Base85, HTML Entities와 같은 고급 인코딩 기능도 필요합니다. 특수한 상황에서 이러한 고급 인코딩을 처리할 수 있어야 합니다.

**Why this priority**: 고급 인코딩은 기본 인코딩보다 사용 빈도가 낮지만, 특정 보안 작업이나 CTF 챌린지, 데이터 분석에서 필수적입니다. P1-P3 기능으로 이미 완벽한 툴을 제공한 후 확장 기능으로 추가합니다.

**Independent Test**: 텍스트를 입력하고 Base32, Base85, HTML Entities의 인코딩/디코딩 버튼을 각각 클릭하여 정확한 결과가 출력되는지 확인. 각 인코딩 형식에 맞는 결과가 생성되는지 확인. 이 기능만으로도 고급 인코딩 요구사항을 충족합니다.

**Acceptance Scenarios**:

1. **Given** 사용자가 텍스트를 입력하고 Base32 Encode 버튼을 클릭하면, **When** 인코딩이 실행되고, **Then** 결과창에 Base32로 인코딩된 텍스트가 표시된다
2. **Given** 사용자가 Base32로 인코딩된 텍스트를 입력하고 Decode 버튼을 클릭하면, **When** 디코딩이 실행되고, **Then** 결과창에 원본 텍스트가 표시된다
3. **Given** 사용자가 "<script>alert('XSS')</script>"을 입력하고 HTML Entities Encode 버튼을 클릭하면, **When** 인코딩이 실행되고, **Then** 결과창에 "&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;"가 표시된다
4. **Given** 사용자가 HTML 엔티티로 인코딩된 텍스트를 입력하고 Decode 버튼을 클릭하면, **When** 디코딩이 실행되고, **Then** 결과창에 원본 HTML이 표시된다
5. **Given** 사용자가 텍스트를 입력하고 Base85 Encode 버튼을 클릭하면, **When** 인코딩이 실행되고, **Then** 결과창에 Base85로 인코딩된 텍스트가 표시된다

---

### User Story 5 - 고급 해시 및 텍스트 처리 기능 (Priority: P5)

보안 전문가로서, SHA-1, SHA-512, SHA-3, BLAKE2와 같은 고급 해시 알고리즘과 JSON 포맷팅, 대소문자 변환과 같은 텍스트 처리 기능이 필요합니다.

**Why this priority**: 고급 해시 알고리즘은 특정 보안 요구사항이나 레거시 시스템 호환성을 위해 필요합니다. 텍스트 처리 기능은 데이터 정리 작업에 유용합니다. 가장 사용 빈도가 낮은 확장 기능입니다.

**Independent Test**: 텍스트를 입력하고 SHA-1, SHA-512, SHA-3, BLAKE2 해시 버튼을 각각 클릭하여 올바른 해시값이 생성되는지 확인. JSON을 입력하고 Beautify/Minify 버튼을 클릭하여 포맷팅되는지 확인. 대소문자 변환 버튼을 클릭하여 텍스트가 변환되는지 확인.

**Acceptance Scenarios**:

1. **Given** 사용자가 텍스트를 입력하고 SHA-1 해시 버튼을 클릭하면, **When** 해시가 생성되고, **Then** 결과창에 40자리 16진수 SHA-1 해시값이 표시된다
2. **Given** 사용자가 텍스트를 입력하고 SHA-512 해시 버튼을 클릭하면, **When** 해시가 생성되고, **Then** 결과창에 128자리 16진수 SHA-512 해시값이 표시된다
3. **Given** 사용자가 텍스트를 입력하고 SHA-3 해시 버튼을 클릭하면, **When** 해시가 생성되고, **Then** 결과창에 SHA-3 해시값이 표시된다
4. **Given** 사용자가 텍스트를 입력하고 BLAKE2 해시 버튼을 클릭하면, **When** 해시가 생성되고, **Then** 결과창에 BLAKE2 해시값이 표시된다
5. **Given** 사용자가 압축된 JSON을 입력하고 Beautify 버튼을 클릭하면, **When** 포맷팅이 실행되고, **Then** 결과창에 들여쓰기된 읽기 쉬운 JSON이 표시된다
6. **Given** 사용자가 포맷팅된 JSON을 입력하고 Minify 버튼을 클릭하면, **When** 압축이 실행되고, **Then** 결과창에 공백이 제거된 압축된 JSON이 표시된다
7. **Given** 사용자가 "hello world"를 입력하고 UPPERCASE 버튼을 클릭하면, **When** 변환이 실행되고, **Then** 결과창에 "HELLO WORLD"가 표시된다
8. **Given** 사용자가 "HELLO WORLD"를 입력하고 lowercase 버튼을 클릭하면, **When** 변환이 실행되고, **Then** 결과창에 "hello world"가 표시된다
9. **Given** 사용자가 "hello world"를 입력하고 Title Case 버튼을 클릭하면, **When** 변환이 실행되고, **Then** 결과창에 "Hello World"가 표시된다

---

### User Story 6 - 특수 변환 기능 (Priority: P6)

보안 전문가로서, JWT 디코딩과 모스 부호 변환과 같은 특수한 변환 기능이 필요합니다. JWT 토큰을 디코딩하여 내용을 확인하고, 모스 부호로 변환할 수 있어야 합니다.

**Why this priority**: JWT 디코딩은 웹 보안 작업에서 자주 필요하지만 디코딩만 필요합니다. 모스 부호는 매우 특수한 use case로 CTF나 교육용으로 사용됩니다. 가장 낮은 우선순위입니다.

**Independent Test**: JWT 토큰을 입력하고 Decode 버튼을 클릭하여 헤더, 페이로드, 시그니처가 분리되어 표시되는지 확인. 텍스트를 입력하고 모스 부호로 인코딩/디코딩하여 올바른 결과가 출력되는지 확인.

**Acceptance Scenarios**:

1. **Given** 사용자가 JWT 토큰을 입력하고 JWT Decode 버튼을 클릭하면, **When** 디코딩이 실행되고, **Then** 결과창에 헤더, 페이로드, 시그니처가 각각 JSON 형식으로 표시된다
2. **Given** 사용자가 "SOS"를 입력하고 Morse Code Encode 버튼을 클릭하면, **When** 인코딩이 실행되고, **Then** 결과창에 "... --- ..."가 표시된다
3. **Given** 사용자가 "... --- ..."를 입력하고 Morse Code Decode 버튼을 클릭하면, **When** 디코딩이 실행되고, **Then** 결과창에 "SOS"가 표시된다

---

### Edge Cases

- **빈 입력 처리**: 사용자가 빈 텍스트를 입력하고 변환 버튼을 클릭할 경우, 시스템은 에러 메시지를 표시하고 빈 결과를 반환하지 않아야 한다
- **잘못된 입력 처리**: Base64 Decode 시 잘못된 Base64 문자열을 입력하면, 시스템은 "잘못된 Base64 형식입니다"와 같은 친절한 에러 메시지를 표시해야 한다
- **대용량 텍스트 처리**: 사용자가 10,000자 이상의 대용량 텍스트를 입력할 경우, 시스템은 2초 이내에 변환을 완료하고 UI가 응답하지 않는 현상이 발생하지 않아야 한다 (UI 스레드 블록 없이 백그라운드에서 처리, 응답 지연 < 500ms)
- **특수 문자 처리**: HTML 엔티티 인코딩 시 모든 특수 문자와 유니코드 문자가 올바르게 변환되어야 한다
- **해시 입력 제한**: 해시 생성은 빈 텍스트에 대해서도 가능해야 하며(빈 문자열의 해시), 빈 텍스트 입력 시 에러를 표시하지 않아야 한다
- **JWT 무효 토큰**: 무효하거나 손상된 JWT 토큰을 디코딩하려 할 경우, "잘못된 JWT 형식입니다" 에러 메시지를 표시해야 한다
- **모스 부호 미지원 문자**: 모스 부호로 변환할 수 없는 문자(예: 한글, 특수 기호)가 입력되면, 지원 가능한 문자로 제한하거나 에러를 표시해야 한다
- **핫키 충돌**: `Ctrl + .` 핫키가 다른 애플리케이션에서 사용 중일 경우, 사용자는 설정 메뉴에서 대체 핫키를 설정할 수 있다 (Priority: P5)
- **멀티모니터 환경**: 멀티모니터 환경에서 핫키로 창을 표시할 때, 마지막으로 활성화된 모니터에 창이 표시되어야 한다
- **시스템 트레이 아이콘 누락**:
  - **Windows**: Windows 특정 버전에서 시스템 트레이 아이콘이 보이지 않는 문제가 발생할 경우, 알림 영역 설정을 통해 아이콘이 항상 표시되도록 안내해야 한다
  - **macOS**: macOS Menu Bar 아이콘이 16개 이상일 경우 자동으로 숨겨질 수 있으므로, 사용자 설정에 따라 표시되어야 한다
  - **Linux**: Linux 데스크톱 환경(GNOME, KDE, XFCE 등)마다 시스템 트레이 구현이 다르므로, Qt6가 자동으로 각 환경에 맞는 트레이 아이콘을 표시해야 한다
- **플랫폼별 핫키 동작**: `Ctrl + .` 핫키가 macOS에서는 `Cmd + .`로 자동 변환되어야 할 수 있다 (macOS 사용성 관습)
- **파일 권한 문제 (Linux/macOS)**: Linux/macOS에서 실행 파일을 다운로드 후 실행 권한(x)이 없을 경우, 사용자에게 친절한 안내 메시지를 표시해야 한다

## Requirements *(mandatory)*

### Functional Requirements

**사용자 인터페이스**:
- **FR-001**: System MUST provide a GUI window with input text area, output text area, and transformation buttons arranged in a clear layout
- **FR-002**: System MUST display transformation categories (Encoding, Hash, Text Processing, Classical Ciphers) in a left sidebar panel
- **FR-003**: System MUST provide input text area at the top of the right panel
- **FR-004**: System MUST provide output text area at the bottom of the right panel
- **FR-005**: System MUST provide transformation buttons in the middle section between input and output areas
- **FR-006**: System MUST provide a copy button to copy output text to clipboard
- **FR-007**: System MUST provide clear transformation buttons for each encoding, decoding, hash, and text processing function
- **FR-008**: System MUST provide a search/filter box at the top of the left sidebar to quickly find algorithms by name (실시간 필터링)
- **FR-009**: System MUST organize algorithms into expandable category groups in the sidebar (Encoding, Hash, Text Processing, Classical Ciphers)

**기본 인코딩/디코딩 (P1)**:
- **FR-010**: System MUST support Base64 encoding and decoding
- **FR-011**: System MUST support URL encoding and decoding (percent-encoding)
- **FR-012**: System MUST support Hex (16진수) encoding and decoding
- **FR-013**: System MUST display encoding/decoding results in the output text area within 1 second for text up to 10,000 characters

**기본 해시 (P1)**:
- **FR-014**: System MUST support MD5 hash generation
- **FR-015**: System MUST support SHA-256 hash generation
- **FR-016**: System MUST display hash results as hexadecimal strings
- **FR-017**: System MUST generate hash for empty string (should not show error for empty input)

**글로벌 핫키 (P2)**:
- **FR-018**: System MUST register `Ctrl + .` as a global hotkey that works even when the window is not focused
- **FR-019**: System MUST toggle window visibility (show/hide) when global hotkey is pressed
- **FR-020**: System MUST preserve input and output text when window is hidden and shown again
- **FR-021**: System MUST bring window to foreground and focus when shown via hotkey
- **FR-022**: System MUST provide a Settings menu where users can customize the global hotkey combination (Priority: P5)
- **FR-023**: System MUST validate hotkey combinations to prevent conflicts with common system shortcuts (e.g., Ctrl+C, Ctrl+V)

**시스템 트레이 및 백그라운드 실행 (P3)**:
- **FR-024**: System MUST minimize to system tray instead of closing when X button is clicked
- **FR-025**: System MUST display an icon in the system tray when minimized
- **FR-026**: System MUST provide a context menu when system tray icon is right-clicked
- **FR-027**: System MUST provide "Info" menu item in tray context menu that shows program name, version, and copyright
- **FR-028**: System MUST provide "Exit" menu item in tray context menu that completely terminates the program
- **FR-029**: System MUST restore window when system tray icon is double-clicked

**확장 인코딩/디코딩 (P4-P6)**:
- **FR-030**: System MUST support Base16, Base32, Base32Hex encoding and decoding
- **FR-031**: System MUST support Base58 (Bitcoin) encoding and decoding
- **FR-032**: System MUST support Base62 encoding and decoding
- **FR-033**: System MUST support Base85 (Ascii85) encoding and decoding
- **FR-034**: System MUST support Base91 encoding and decoding
- **FR-035**: System MUST support HTML Entities encoding and decoding
- **FR-036**: System MUST handle all special characters and Unicode in HTML Entity encoding
- **FR-037**: System MUST support Punycode (IDN) encoding and decoding
- **FR-038**: System MUST support Unicode Escape (\uXXXX) encoding and decoding
- **FR-039**: System MUST support Quoted-Printable encoding and decoding
- **FR-040**: System MUST support Binary (2진수), Octal (8진수), Decimal (10진수) representation encoding and decoding
- **FR-041**: System MUST support Morse Code encoding and decoding
- **FR-042**: System MUST support Braille (점자) encoding and decoding

**확장 해시 알고리즘 (P4-P6)**:
- **FR-043**: System MUST support SHA-1, SHA-224, SHA-384, SHA-512 hash generation
- **FR-044**: System MUST support SHA-512/224, SHA-512/256 hash generation
- **FR-045**: System MUST support SHA3-224, SHA3-256, SHA3-384, SHA3-512 hash generation
- **FR-046**: System MUST support Keccak-256 hash generation
- **FR-047**: System MUST support BLAKE2s and BLAKE2b hash generation
- **FR-048**: System MUST support RIPEMD-160 hash generation
- **FR-049**: System MUST support Whirlpool hash generation
- **FR-050**: System MUST support MD2, MD4 hash generation
- **FR-051**: System MUST support CRC32 checksum generation
- **FR-052**: System MUST support Adler32 checksum generation

**텍스트 처리 및 포맷팅 (P4-P6)**:
- **FR-053**: System MUST support JSON Beautify (formatting with indentation)
- **FR-054**: System MUST support JSON Minify (removing whitespace)
- **FR-055**: System MUST validate JSON format before Beautify/Minify and show error if invalid
- **FR-056**: System MUST support XML Pretty Print formatting
- **FR-057**: System MUST support YAML formatting
- **FR-058**: System MUST support SQL Minify (removing whitespace)
- **FR-059**: System MUST support case conversion: UPPERCASE, lowercase, Title Case
- **FR-060**: System MUST support case conversion: camelCase, snake_case, PascalCase, Kebab-Case
- **FR-061**: System MUST support Remove Duplicates (line-based)
- **FR-062**: System MUST support Sort Lines (Ascending/Descending)
- **FR-063**: System MUST support Remove Empty Lines
- **FR-064**: System MUST support Strip Whitespace (leading/trailing)
- **FR-065**: System MUST support C-Style String Escape/Unescape
- **FR-066**: System MUST support Shell Escape/Unescape

**클래식 암호 (P6)**:
- **FR-067**: System MUST support ROT13 cipher encoding and decoding
- **FR-068**: System MUST support Caesar Cipher (with configurable shift)
- **FR-069**: System MUST support Vigenère Cipher encoding and decoding
- **FR-070**: System MUST support Atbash Cipher encoding and decoding

**JWT 디코딩 (P6)**:
- **FR-071**: System MUST support JWT decoding (header, payload, signature separation)
- **FR-072**: System MUST display JWT header and payload as formatted JSON

**에러 처리**:
- **FR-073**: System MUST display user-friendly error messages in Korean when decoding fails (invalid input format)
- **FR-074**: System MUST show error message when empty input is provided for encoding/decoding operations
- **FR-075**: System MUST handle invalid Base64 input and show specific error message
- **FR-076**: System MUST handle invalid JSON input and show specific error message with line number
- **FR-077**: System MUST handle invalid JWT input and show specific error message
- **FR-078**: System MUST handle unsupported characters in Morse Code and Braille conversion

**성능**:
- **FR-079**: System MUST complete transformations within 2 seconds for text up to 10,000 characters
- **FR-080**: System MUST remain responsive during transformation operations (UI thread block < 500ms, background processing for large text)
- **FR-081**: System MUST use less than 100MB memory when idle
- **FR-082**: System MUST update search filter results within 0.3 seconds when user types in search box (with 150ms debouncing)

**배포**:
- **FR-083**: System MUST be packaged as a single executable file for each platform (Windows .exe, macOS .app, Linux binary)
- **FR-084**: System MUST run without requiring Python or any dependencies to be installed separately
- **FR-085**: System MUST be compatible with:
  - **Windows**: Windows 10 and Windows 11 (x64)
  - **macOS**: macOS 11+ (Big Sur and later, both Intel and Apple Silicon)
  - **Linux**: Ubuntu 20.04+, Fedora 35+, Debian 11+ with GNOME, KDE, or XFCE desktop environments (x64)

### Key Entities

**변환 작업 (Transformation Operation)**:
- 작업 유형 (Operation Type): Encoding, Decoding, Hash, Text Processing, Cipher
- 알고리즘 (Algorithm): Base64, URL, Hex, Base16, Base32, Base32Hex, Base58, Base62, Base85, Base91, HTML Entities, Punycode, JWT, Unicode Escape, Quoted-Printable, Binary, Octal, Decimal, Morse Code, Braille, MD2, MD4, MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512, SHA-512/224, SHA-512/256, SHA3-224, SHA3-256, SHA3-384, SHA3-512, Keccak-256, BLAKE2s, BLAKE2b, RIPEMD-160, Whirlpool, CRC32, Adler32, JSON Beautify, JSON Minify, XML Pretty Print, YAML Format, SQL Minify, UPPERCASE, lowercase, Title Case, camelCase, snake_case, PascalCase, Kebab-Case, Remove Duplicates, Sort Lines, Remove Empty Lines, Strip Whitespace, C-Style Escape, Shell Escape, ROT13, Caesar Cipher, Vigenère Cipher, Atbash Cipher
- 입력 텍스트 (Input Text): 사용자가 입력한 원본 텍스트
- 출력 텍스트 (Output Text): 변환 결과 텍스트
- 성공 여부 (Success): 변환 성공 또는 실패
- 에러 메시지 (Error Message): 실패 시 사용자에게 표시할 에러 내용

**프로그램 상태 (Application State)**:
- 창 가시성 (Window Visibility): Visible, Hidden
- 백그라운드 실행 상태 (Background State): Running in background, Terminated
- 현재 선택된 변환 (Current Transformation): 마지막으로 사용한 변환 알고리즘
- 검색 필터 (Search Filter): 현재 검색어
- 입력 텍스트 보존 (Preserved Input): 창이 숨겨진 동안 유지된 입력 텍스트
- 출력 텍스트 보존 (Preserved Output): 창이 숨겨진 동안 유지된 출력 텍스트

**UI 구성 요소 (UI Components)**:
- 좌측 사이드바 (Left Sidebar): 카테고리 트리, 검색창
- 우측 컨텐츠 영역 (Right Content Area): 입력창, 옵션 패널, 출력창
- 카테고리 (Categories): Encoding, Hash, Text Processing, Classical Ciphers
- 검색 필터 (Search Filter): 실시간 알고리즘 필터링

**시스템 트레이 메뉴 (System Tray Menu)**:
- 메뉴 항목 (Menu Items): Info, Exit
- 프로그램 정보 (Program Info): 이름, 버전, 저작권

**핫키 설정 (Hotkey Configuration)**:
- 핫키 조합 (Key Combination): Ctrl + .
- 핫키 동작 (Action): Toggle window visibility

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 사용자는 텍스트를 입력하고 변환 버튼을 클릭하여 1초 이내에 변환 결과를 확인할 수 있다
- **SC-002**: 사용자는 `Ctrl + .` 핫키를 눌러 0.5초 이내에 창을 표시하거나 숨길 수 있다
- **SC-003**: 사용자는 창의 X 버튼을 클릭하여 백그라운드로 최소화하고, 시스템 트레이에서 프로그램이 계속 실행 중임을 확인할 수 있다
- **SC-004**: 사용자는 모든 기본 변환(Base64, URL, Hex)과 해시(MD5, SHA-256) 기능을 에러 없이 100회 연속 실행할 수 있다
- **SC-005**: 사용자는 결과창의 복사 버튼을 클릭하여 클립보드에 텍스트를 복사하고 다른 애플리케이션에 붙여넣기 할 수 있다
- **SC-006**: 사용자는 10,000자의 대용량 텍스트를 변환할 때 UI 응답 지연(프리징) 없이 2초 이내에 결과를 확인할 수 있다
- **SC-007**: 사용자는 잘못된 형식의 입력(예: 유효하지 않은 Base64)을 제공했을 때, 한국어로 된 친절한 에러 메시지를 확인할 수 있다
- **SC-008**: 사용자는 단일 .exe 파일을 다운로드하여 별도 설치 과정 없이 실행할 수 있다
- **SC-009**: 사용자는 프로그램 첫 실행 후 30초 이내에 모든 기본 기능(P1)을 성공적으로 테스트할 수 있다
- **SC-010**: 사용자는 시스템 트레이 메뉴를 통해 프로그램 정보를 확인하고 프로그램을 완전히 종료할 수 있다

## Assumptions

### 플랫폼 환경
- 사용자는 **Windows 10/11**, **macOS 11+**, 또는 **Ubuntu 20.04+** (또는 동등한 Linux 배포판) 운영체제를 사용한다
- Linux 데스크톱 환경: GNOME, KDE, 또는 XFCE 지원

### 사용자 특성
- 사용자는 기본적인 GUI 애플리케이션 사용 방법을 이해하고 있다
- 사용자는 인코딩, 디코딩, 해시의 기본 개념을 알고 있다 (보안 전문가 대상)
- 사용자는 한글을 읽고 이해할 수 있다

### 운영 환경
- 단일 사용자 환경에서 사용되며, 다중 사용자 동시 접속은 고려하지 않는다
- 인터넷 연결 없이 오프라인 환경에서 실행 가능해야 한다
- 프로그램은 관리자 권한 없이 실행 가능해야 한다 (root/sudo 불필요)

### 시스템 요구사항
- 사용자의 시스템에 최소 100MB의 여유 디스크 공간이 있다고 가정한다
- **UI 일관성**: Qt6가 자동으로 각 OS의 네이티브 look & feel를 제공하므로 사용자 경험에 큰 차이가 없다

## UI/UX Design Requirements

### 1. UI 구조 (레이아웃)

알고리즘의 수가 방대하므로 단순 드롭다운 방식이 아닌 **사이드바 분류 방식**을 사용한다.

**좌측 사이드바 (Left Sidebar)**:
- 카테고리 트리 뷰: Encoding, Hash, Text Processing, Classical Ciphers
- 상단 검색창: 알고리즘 이름으로 실시간 필터링
- 확장/축소 가능한 카테고리 그룹
- 선택된 알고리즘 하이라이트

**우측 컨텐츠 영역 (Right Content Area)**:
- 상단: Input Text (대용량 텍스트 지원, 스크롤 가능)
- 중단: 변환 옵션 패널 (Base64 Padding 여부, Hash Salt, Caesar Cipher Shift 등)
- 하단: Output Text 및 Copy 버튼

**UX 요구사항**:
- **FR-UX-001**: 사용자는 검색창에 알고리즘 이름을 입력하여 0.3초 이내에 필터링 결과를 확인할 수 있다
- **FR-UX-002**: 사용자는 카테고리 그룹을 확장/축소하여 원하는 알고리즘을 빠르게 찾을 수 있다
- **FR-UX-003**: 사용자는 입력창에 텍스트를 입력하고 엔터키 또는 변환 버튼으로 즉시 변환 결과를 확인할 수 있다
- **FR-UX-004**: 사용자는 결과창 옆 복사 버튼으로 원클릭으로 결과를 클립보드에 복사할 수 있다

### 2. 실시간 변환 모드 검토 (Optional)

입력 시 자동으로 변환 결과를 표시하는 기능을 고려할 수 있으나, 성능 영향 평가 필요:
- 대용량 텍스트(10,000자 이상) 입력 시 UI 지연 가능성
- 사용자 옵션으로 제공: "실시간 변환" on/off 토글

## Architecture Requirements

### 1. 모듈화 설계 (Plugin Architecture)

각 알고리즘을 독립적인 모듈로 구현하여 확장성을 확보한다.

**구조**:
- `transformers/` 디렉토리: 각 알고리즘별 파이썬 모듈/클래스
- `registry.py`: 알고리즘 등록 시스템
- 신규 알고리즘 추가 시 `registry.py`에 등록만으로 UI 자동 반영

**아키텍처 요구사항**:
- **FR-ARCH-001**: 각 변환 알고리즘은 독립적인 클래스로 구현되어야 한다
- **FR-ARCH-002**: 알고리즘은 `transform(base_algorithm: str, input_text: str, options: dict) -> str` 인터페이스를 구현해야 한다
- **FR-ARCH-003**: 신규 알고리즘 추가 시 UI 코드 수정 없이 `registry.py` 등록만으로 자동 반영되어야 한다
- **FR-ARCH-004**: 알고리즘 모듈은 독립적으로 테스트 가능해야 한다

### 2. 백그라운드 및 시스템 연동

**핫키 엔진 (Hotkey Engine)**:
- 저수준 키보드 이벤트 리스너로 전역 핫키 지원
- 백그라운드 스레드에서 실행되어 UI 응답성 유지

**트레이 엔진 (Tray Engine)**:
- Windows 네이티브 시스템 트레이 아이콘 지원
- 컨텍스트 메뉴 및 더블 클릭 이벤트 처리

**아키텍처 요구사항**:
- **FR-ARCH-005**: 핫키 리스너는 백그라운드 스레드에서 실행되어 UI 응답성에 영향을 주지 않아야 한다
- **FR-ARCH-006**: 시스템 트레이 기능은 OS 네이티브 API를 사용하여 안정적이어야 한다
- **FR-ARCH-007**: 창 상태 전환(Show/Hide)은 스레드 세이프하게 처리되어야 한다

### 3. 검색 및 필터링

**검색 엔진 (Search Engine)**:
- 알고리즘 이름, 카테고리, 별칭으로 검색
- 실시간 필터링 (0.3초 이내 응답)
- 대소문자 구분 없는 검색

**아키텍처 요구사항**:
- **FR-ARCH-008**: 검색은 인메모리 인덱스를 사용하여 빠르게 수행되어야 한다
- **FR-ARCH-009**: 검색 결과는 하이라이트되어 사용자에게 명확히 표시되어야 한다
