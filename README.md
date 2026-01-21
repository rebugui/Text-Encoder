# Text Encoder - 확장형 GUI 텍스트 유틸리티 툴

보안 전문가와 개발자를 위한 포괄적인 텍스트 변환 유틸리티입니다. 80개 이상의 변환 알고리즘을 제공하며, 백그라운드 실행과 글로벌 핫키로 빠른 접근성을 제공합니다.

## 주요 기능

### 1. 인코딩/디코딩 (80+ 알고리즘)
- **Standard**: Base64, URL, Hex
- **Advanced Base**: Base16, Base32, Base58, Base62, Base85, Base91
- **Web & Programming**: HTML Entities, Punycode, Unicode Escape, Quoted-Printable
- **Representations**: Binary, Octal, Decimal
- **Special**: Morse Code, Braille

### 2. 해시 알고리즘
- **MD Family**: MD2, MD4, MD5
- **SHA Family**: SHA-1, SHA-224, SHA-256, SHA-384, SHA-512, SHA3-256, Keccak-256
- **Secure**: BLAKE2s, BLAKE2b, RIPEMD-160, Whirlpool
- **Checksums**: CRC32, Adler32

### 3. 텍스트 처리
- JSON/XML/YAML 포맷팅 (Beautify/Minify)
- 대소문자 변환 (UPPERCASE, lowercase, camelCase, snake_case 등)
- 중복 제거, 정렬, 공백 제거

### 4. 클래식 암호
- ROT13, Caesar Cipher, Vigenère Cipher, Atbash Cipher

## 시스템 요구사항

### 지원 플랫폼
- **Windows**: Windows 10/11 (x64)
- **macOS**: macOS 11+ (Intel + Apple Silicon)
- **Linux**: Ubuntu 20.04+, Fedora 35+, Debian 11+ (GNOME/KDE/XFCE)

### 설치 방법

#### 개발 환경 설정
```bash
# 1. Python 3.11+ 설치 확인
python --version

# 2. 가상 환경 생성 (권장)
python -m venv venv

# 3. 가상 환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 4. 의존성 설치
pip install -r requirements.txt
```

#### 애플리케이션 실행
```bash
python src/main.py
```

## 사용법

### 기본 변환
1. 좌측 사이드바에서 원하는 알고리즘 선택
2. 상단 입력창에 텍스트 입력
3. 변환 버튼 클릭 또는 Enter 키 누름
4. 하단 결과창에 변환 결과 표시
5. 복사 버튼으로 클립보드에 복사

### 글로벌 핫키
- **Windows/Linux**: `Ctrl + .`
- **macOS**: `Cmd + .`
- 창 숨김/표시 전환

### 시스템 트레이
- 창의 X 버튼 클릭 시 시스템 트레이로 최소화
- 트레이 아이콘 더블 클릭으로 창 복원
- 우클릭 메뉴에서 Info/Exit 선택

## 빌드

### 아이콘 생성
빌드하기 전에 애플리케이션 아이콘을 생성해야 합니다:

```bash
# 아이콘 생성 스크립트 실행
python scripts/generate_icons.py

# 생성되는 파일:
# - assets/icon.ico (Windows용 - 다중 사이즈 내장: 16, 32, 48, 64, 128, 256)
# - assets/icon.png (macOS/Linux용 - 256x256)
```

#### 아이콘 유틸리티 스크립트
```bash
# 아이콘 파일 검증
python scripts/verify_icons.py

# 아이콘 미리보기 (이미지 뷰어에서 표시)
python scripts/preview_icons.py
```

### Windows
```bash
pyinstaller build/encoder.spec --clean --onefile
# 출력: build/dist/TextEncoder.exe
```

### macOS
```bash
pyinstaller build/encoder.spec --clean --onefile --windowed
# 출력: build/dist/TextEncoder.app
```

### Linux
```bash
pyinstaller build/encoder.spec --clean --onefile
# 출력: build/dist/text-encoder
```

## 테스트

```bash
# 전체 테스트 실행
pytest tests/ -v

# 커버리지 리포트
pytest tests/ --cov=src --cov-report=html
```

## 라이선스

MIT License

## 기여

이 프로젝트에 기여하고 싶으시다면 Pull Request를 제출해주세요.
