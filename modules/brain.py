import whisper
from google import genai  # 최신 라이브러리로 변경
import json
import torch # 경고 제어용
from config import Config

class Brain:
    def __init__(self):
        print("🤖 Whisper 모델 로딩 중...")
        # CPU 환경에서 FP16 경고가 뜨지 않게 장치 설정
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.stt_model = whisper.load_model("base", device=device)
        
        # 2. 최신 Gemini API 설정
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model_id = "gemini-2.5-flash-lite"
        
        self.system_prompt = """
        너의 이름은 'Dokjong'이며, 윈도우 비서야.
        반드시 아래 JSON 형식으로만 답해.

        실행 가능한 프로그램 목록(target에 이 이름들을 우선적으로 사용해):
        [크롬, 메모장, 계산기, 유튜브, 브챗, 인스타]

        목록에 있는 이름과 비슷한 단어가 명령어에 포함되어 있다면, 목록 안의 단어로 인식해서 target에 넣어줘.
        예시: 부챗 -> 브챗, 유투부 -> 유튜브

        검색이라는 말이 포함되어 있다면 action은 "search"로 해주고, target에는 검색어를 넣어줘.
        예시: "인터넷에서 고양이 검색해줘" -> action: "search", target: "고양이 영상"

        {
        "action": "execute" | "shutdown" | "search" | "unknown",
        "target": "위 목록에 있는 이름 또는 검색어",
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
            initial_prompt="독종아 유튜브 켜줘, 크롬 실행해줘, 컴퓨터 종료해줘, 브챗 열어줘" 
        )
        return result['text']

    def understand_intent(self, text):
        full_prompt = f"{self.system_prompt}\n\n사용자 명령: {text}"
        
        # 최신 라이브러리 호출 방식
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=full_prompt
        )
        
        try:
            # JSON만 정제해서 추출
            clean_json = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(clean_json)
        except Exception as e:
            print(f"JSON 파싱 에러: {e}")
            return {"action": "unknown", "target": None, "reply": "명령을 이해하지 못했어요."}