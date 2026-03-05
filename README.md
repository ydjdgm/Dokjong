# 🤖 Dokjong: Personalized Windows AI Butler

> **Dokjong**은 사용자의 음성을 상시 모니터링하여 Windows 시스템을 제어하는 지능형 AI 비서 솔루션입니다.
> 사용자의 호출어(Wake Word)에 반응하며, Google Gemini의 강력한 추론 능력을 바탕으로 자연어 명령을 시스템 액션으로 변환합니다.

---

## 🌟 Key Features

* **Always-on Listening:** 오프라인 호출어 감지 엔진을 통한 상시 대기 및 시스템 리소스 최적화.
* **Intelligent Intent Analysis:** Gemini 1.5/2.5 Flash 모델을 활용한 고수준 문맥 파악 및 구조화된 명령어(JSON) 생성.
* **Automated OS Control:** 브라우저 자동화, 애플리케이션 실행 및 시스템 제어 기능.
* **Voice Feedback:** Windows 내장 TTS 엔진을 통한 실시간 상태 보고 및 상호작용.

---

## 🏗 System Architecture

본 프로젝트는 유지보수와 기능 확장을 위해 **4개의 독립적인 모듈**로 설계되었습니다.

1. **Listener (`modules/listener.py`):** 호출어 감지(Porcupine) 및 오디오 데이터 스트리밍.
2. **Brain (`modules/brain.py`):** 음성 텍스트 변환(Whisper) 및 LLM 기반 의도 파악(Gemini).
3. **Executor (`modules/executor.py`):** 파싱된 명령에 따른 윈도우 프로세스 제어 및 자동화.
4. **Speaker (`modules/speaker.py`):** 사용자 피드백을 위한 TTS 음성 출력.

---

## 🛠 Tech Stack

| Category | Technology | Description |
| --- | --- | --- |
| **Language** | Python 3.12+ | 프로젝트 메인 엔진 및 모듈 관리 |
| **Wake Word** | Picovoice Porcupine | 가벼운 오프라인 호출어 감지 엔진 |
| **STT** | OpenAI Whisper | 로컬 기반의 고성능 다국어 음성 인식 모델 |
| **LLM** | Google Gemini API | 자연어 명령어 해석 및 JSON 데이터 생성 |
| **TTS** | pyttsx3 | 윈도우 SAPI5 기반 오프라인 음성 출력 |
| **OS Control** | Subprocess / OS | 시스템 레벨의 애플리케이션 및 브라우저 제어 |

---

## ⚙️ Installation & Setup

### 1. Prerequisites

* **Python 3.12+** 설치
* **FFmpeg** 설치 및 시스템 환경 변수(PATH) 등록 (필수)
* Google AI Studio 및 Picovoice Console에서 API 키 발급

### 2. Dependency Installation

```bash
git clone https://github.com/your-repo/Dokjong.git
cd Dokjong
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Environment Configuration

루트 폴더에 `.env` 파일을 생성하고 아래 형식을 따릅니다.

```env
GEMINI_API_KEY=your_key_here
PICOVOICE_ACCESS_KEY=your_key_here

```

---

## 🚀 Usage

1. `main.py`를 실행합니다.
2. **"독종"**이라고 불러 비서를 활성화합니다.
3. 호출 성공 후, 명령어를 말씀하세요. (예: "유튜브 켜줘", "메모장 열어줘")

### Application Mapping (Customizable)

`modules/executor.py`의 `self.apps` 딕셔너리에 실행하려는 프로그램의 경로를 추가하여 기능을 확장할 수 있습니다.

```python
self.apps = {
    "브챗": r"C:\Path\To\VRChat.url",
    "메모장": "notepad.exe"
}

```

---

## 📈 Roadmap & Future Work

* [ ] **Multi-turn Conversation:** 이전 대화 문맥을 기억하는 메모리 기능 추가.
* [ ] **GUI Dashboard:** 현재 상태 및 음성 인식 텍스트를 시각화하는 대시보드 개발.
* [ ] **Custom Automation:** 특정 시간에 뉴스 요약이나 날씨 정보를 읽어주는 스케줄링 기능.