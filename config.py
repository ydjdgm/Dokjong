import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    """프로젝트 설정값을 관리하는 클래스"""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PICOVOICE_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
    
    # 경로 설정
    WAKE_WORD_PATH = os.path.join("models", "Dokjong_ko_windows_v4_0_0.ppn") # 한국어로 만든 .ppn 파일
    MODEL_PATH = os.path.join("models", "porcupine_params_ko.pv") # 다운로드한 한국어 모델 파일
    
    @classmethod
    def validate(cls):
        """필수 API 키가 있는지 확인"""
        if not cls.GEMINI_API_KEY or not cls.PICOVOICE_KEY:
            raise ValueError("API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")

if __name__ == "__main__":
    # 테스트용: 정상적으로 로드되는지 확인
    try:
        Config.validate()
        print("✅ 설정 로드 완료!")
    except Exception as e:
        print(f"❌ 설정 오류: {e}")