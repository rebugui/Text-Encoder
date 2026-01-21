# Text Encoder - 확장형 GUI 텍스트 유틸리티 툴

<div align="center">

![Status](https://img.shields.io/badge/status-completed-success)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

보안 전문가와 개발자를 위한 포괄적인 텍스트 변환 유틸리티입니다.

**81개 변환 알고리즘** • **시스템 트레이** • **글로벌 핫키** • **오프라인 동작**

</div>

## ✨ 주요 기능

### 🔤 81개 변환 알고리즘

#### 인코딩/디코딩 (15개)
- **Standard**: Base64, URL, Hex
- **Advanced Base**: Base32, Base58, Base62, Base85, Base91
- **Representations**: Binary, Octal, ASCII
- **Web & Programming**: HTML Entities

#### 해시 알고리즘 (8개)
- **MD Family**: MD5
- **SHA Family**: SHA1, SHA256, SHA512
- **Secure**: BLAKE2s, BLAKE2b
- **Checksums**: CRC32, Adler32

#### 텍스트 처리 (30개)
- **Case Conversion**: UPPERCASE, lowercase, Title Case, camelCase, snake_case, PascalCase, Kebab-Case
- **Text Operations**: Invert Case, Swap Case, Remove Whitespace, Remove Extra Spaces, Trim Lines
- **Line Operations**: Remove Duplicates, Sort Lines, Reverse Lines, Reverse Text, Shuffle Lines, Number Lines
- **Format**: JSON Beautify/Minify, XML Beautify/Minify
- **Utilities**: Remove BOM, Count Characters/Words/Lines, Remove Numbers, Remove Punctuation

#### 특수 변환 (2개)
- Morse Code (Encode/Decode)
- Braille (Encode/Decode)

#### 특수 포맷 (7개)
- JWT (Encode/Decode)
- CSV Format/Unformat
- Markdown: Table, Bold, Italic, Code, Inline Code

#### 클래식 암호 (6개)
- ROT13, Caesar, Vigenère, Atbash (각각 Encode/Decode)

### 🎨 현대적 UI

- **CustomTkinter 기반** 다크 모드 인터페이스
- **사이드바** 카테고리 필터링 (Encoding, Hashing, Text_Processing, Special, Ciphers)
- **실시간 검색** 150ms 데바운스로 빠른 필터링
- **직관적 레이아웃** 좌측 사이드바 + 우측 컨텐츠 영역

### ⌨️ 글로벌 핫키

- **Windows/Linux**: `Ctrl + Alt + T`
- **macOS**: `Cmd + Alt + T`
- 창 숨김/표시 전환으로 작업 흐름 유지

### 🔔 시스템 트레이

- 백그라운드 실행으로 항상 대기
- 트레이 아이콘 더블 클릭으로 창 복원
- 우클릭 메뉴: Info, Exit

### 🚀 성능

- 10,000자 텍스트 변환 < 2초
- 검색 필터링 < 0.3초
- 백그라운드 스레딩으로 UI 응답성 유지
- 메모리 사용량 < 100MB (유휴 상태)

## 📦 설치

### 플랫폼별 실행 파일

**Windows**:
- `dist/Text Encoder.exe` 다운로드
- 별도 설치 불필요

**macOS/Linux**:
- GitHub Releases에서 다운로드
- GitHub Actions로 자동 빌드

### 개발 환경 설정

```bash
# 1. Python 3.11+ 설치 확인
python --version

# 2. 저장소 클론
git clone https://github.com/yourusername/encoder.git
cd encoder

# 3. 가상 환경 생성 (권장)
python -m venv venv

# 4. 가상 환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 5. 의존성 설치
pip install -r requirements.txt

# 6. 애플리케이션 실행
python src/main.py
```

## 🎯 사용법

### 기본 변환

1. 좌측 **사이드바**에서 카테고리 선택
2. 검색창에 알고리즘 이름 입력 (실시간 필터링)
3. 알고리즘 선택
4. 상단 **입력창**에 텍스트 입력
5. **Encode** 또는 **Decode** 버튼 클릭
6. 하단 **결과창**에 변환 결과 확인
7. 복사 버튼으로 클립보드에 복사

### 글로벌 핫키

- `Ctrl+Alt+T` (Windows/Linux) 또는 `Cmd+Alt+T` (macOS)
- 창 숨김/표시 전환
- 작업 중 빠른 접근

### 시스템 트레이

- 창의 **X 버튼** 클릭 → 시스템 트레이로 최소화
- 트레이 아이콘 **더블 클릭** → 창 복원
- 트레이 아이콘 **우클릭** → 메뉴 (Info, Exit)

## 🛠️ 빌드

### Windows

```bash
# PyInstaller로 단일 exe 빌드
pyinstaller "Text Encoder.spec" --clean

# 출력: dist/Text Encoder.exe
```

### macOS

```bash
# PyInstaller로 앱 번들 빌드
pyinstaller --onefile --windowed --icon=assets/icon.png --name="Text Encoder" --add-data="assets:assets" src/main.py --clean

# 출력: dist/Text Encoder.app
```

### Linux

```bash
# 의존성 설치
sudo apt-get install libxcb-xinerama0 libxcb-cursor0

# PyInstaller로 실행 파일 빌드
pyinstaller --onefile --windowed --icon=assets/icon.png --name="Text Encoder" --add-data="assets:assets" src/main.py --clean

# 출력: dist/Text Encoder
```

### GitHub Actions (자동 빌드)

1. GitHub에 코드 푸시
2. Release 생성 (태그: `v1.0.0`)
3. GitHub Actions가 자동으로 3개 플랫폼 빌드
4. Release 페이지에서 다운로드

## 🧪 테스트

```bash
# 전체 테스트 실행
pytest tests/ -v

# 커버리지 리포트
pytest tests/ --cov=src --cov-report=html
```

## 📂 프로젝트 구조

```
encoder/
├── src/
│   ├── main.py                 # 애플리케이션 진입점
│   ├── registry.py              # 알고리즘 등록 시스템
│   ├── ui/                      # UI 컴포넌트
│   │   ├── main_window.py       # 메인 윈도우
│   │   ├── sidebar.py           # 사이드바 (검색, 카테고리)
│   │   ├── content_area.py      # 컨텐츠 영역 (입력/출력)
│   │   └── system_tray.py       # 시스템 트레이
│   ├── hotkey/
│   │   └── global_hotkey.py     # 글로벌 핫키
│   ├── transformers/            # 81개 변환 알고리즘
│   │   ├── encoding/            # 인코딩/디코딩
│   │   ├── hashing/             # 해시 알고리즘
│   │   ├── text_processing/     # 텍스트 처리
│   │   ├── special/             # 특수 변환
│   │   └── special_formats.py   # 특수 포맷
│   └── utils/
│       └── transformation_worker.py  # 백그라운드 처리
├── assets/
│   ├── icon.ico                 # Windows 아이콘
│   └── icon.png                 # macOS/Linux 아이콘
├── .github/workflows/
│   └── build.yml                # CI/CD 워크플로우
├── specs/                       # 기술 문서
├── tests/                       # 유닛 테스트
├── requirements.txt             # Python 의존성
├── "Text Encoder.spec"          # PyInstaller 스펙
└── README.md                    # 본 파일
```

## 🔧 기술 스택

- **Python 3.13**
- **CustomTkinter**: 현대적 다크 모드 UI
- **pystray**: 크로스플랫폼 시스템 트레이
- **pynput**: 글로벌 핫키 리스너
- **PyInstaller**: 단일 실행 파일 패키징
- **GitHub Actions**: CI/CD 자동화

## 📋 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

## 🤝 기여

이 프로젝트에 기여하고 싶으시다면:

1. Fork 저장소
2. 기능 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Pull Request 제출

## 📞 지원

버그 신고 및 기능 요청:
- GitHub Issues: https://github.com/yourusername/encoder/issues

---

<div align="center">

**Made with ❤️ for Security Professionals & Developers**

</div>
