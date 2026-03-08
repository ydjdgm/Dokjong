import whisper
from google import genai
import json
import torch
from config import Config
from datetime import datetime, timezone

class Brain:
    def __init__(self):
        print("🤖 Whisper 모델 로딩 중...")
        # CPU 환경에서 FP16 경고가 뜨지 않게 장치 설정
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.stt_model = whisper.load_model("base", device=device)
        
        # 2. Gemini API 설정
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model_id1 = "gemini-3.1-flash-lite-preview"
        self.model_id2 = "gemini-2.5-flash-lite"
        self.model_id3 = "gemini-2.5-flash"
        
        self.system_prompt = """
        너의 이름은 'Dokjong'이며, 윈도우 비서야.
        반드시 아래 JSON 형식으로만 답해.

        action은 "execute", "search", "shutdown", "unknown" 중 하나로 해줘.
        - "execute": 프로그램 실행 명령. target에는 프로그램 이름, info는 null로 해줘.
          예시: "인스타 켜줘" -> action: "execute", target: "인스타", info: null
        - "search": 웹 검색 명령. target에는 "크롬" 또는 "유튜브", info에는 검색어를 넣어줘.
          예시: "Obsidian 다운로드 검색해줘" -> action: "search", target: "크롬", info: "Obsidian 다운로드"
          예시: "유튜브에 고양이 영상 검색해줘" -> action: "search", target: "유튜브", info: "고양이 영상"
        - "shutdown": 시스템 종료 명령. 몇초 후에 (ex. 3600초 후) 종료이면 target에 timer 특정한 시간에 (ex. 오후 1시반) 종료이면 target에 alarm이라고 넣어줘.
        info에는 target이 timer면 시간을 초 단위로 바꿔서 넣어주고, alarm이면 종료 시각을 ISO 8601 형식(YYYY-MM-DDTHH:MM:SS)으로 넣어줘. reply에는 "컴퓨터를 종료합니다."라고 넣어줘.
          예시: "컴퓨터 1시간 후에 꺼줘" -> action: "shutdown", target: "timer", info: 3600, reply: "컴퓨터를 종료합니다."
          예시: "컴퓨터 오늘 오후 1시반에 꺼줘" -> action: "shutdown", target: "alarm", info: "2026-03-06T13:30:00", reply: "컴퓨터를 종료합니다."
        - "unknown": 명령을 이해하지 못했을 때. target과 info는 null로 해주고, reply에는 명령어에 대한 자연스러운 대답을 넣어줘.
    
        명령어가 부자연스러울 경우 아래의 자주 사용하는 단어 리스트를 참고해서 명령어를 보정하여 위 조건에 맞게 JSON을 작성해줘.

        자주 사용하는 단어 리스트:
        [유튜브, 브챗, 인스타, 롤, 피파, 팰월드, 제미나이, 켜줘, 실행해줘, 열어줘, 검색해줘, 컴퓨터, 꺼줘, 몇분 후, 몇시에, 오전, 오후]

        {
        "action": "execute" | "shutdown" | "search" | "unknown",
        "target": "위 목록에 있는 이름 또는 검색어",
        "info": "action에 따라 필요한 추가 정보",
        "reply": "응답 메시지"
        }
        """

    def speech_to_text(self, audio_path):
        print("📝 음성 분석 중...")
        # initial_prompt를 주면 한국어 명령어를 더 정확하게 인식합니다.
        result = self.stt_model.transcribe(
            audio_path, 
            language="ko", 
            fp16=False,
            initial_prompt="유튜브, 브챗, 인스타, 롤, 피파, 팰월드, 제미나이, 켜줘, 실행해줘, 검색해줘, 컴퓨터, 꺼줘, 몇분 후, 몇시에" 
        )
        return result['text']

    def understand_intent(self, text):
        full_prompt = f"현재 시각: {datetime.now()}\n\n{self.system_prompt}\n\n사용자 명령: {text}"
        
        # 최신 라이브러리 호출 방식
        try:
            response = self.client.models.generate_content(
                model=self.model_id1,
                contents=full_prompt
            )
        except Exception as e:
            print(f"Model: {self.model_id1} Gemini API 호출 에러: {e}")
            try:
                response = self.client.models.generate_content(
                    model=self.model_id2,
                    contents=full_prompt
                )
            except Exception as e:
                print(f"Model: {self.model_id2} Gemini API 재시도 실패: {e}")
                try:
                    response = self.client.models.generate_content(
                        model=self.model_id3,
                        contents=full_prompt
                    )
                except Exception as e:
                    print(f"Model: {self.model_id3} Gemini API 재시도 실패: {e}")
                    return {"action": "unknown", "target": None, "reply": "명령을 이해하지 못했어요."}
        
        try:
            # JSON만 정제해서 추출
            clean_json = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(clean_json)
        except Exception as e:
            print(f"JSON 파싱 에러: {e}")
            return {"action": "unknown", "target": None, "reply": "명령을 이해하지 못했어요."}