import pyttsx3
from logger import get_logger

logger = get_logger("TTS")

class TTSManager:
    def __init__(self, rate=150, volume=1.0):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            
            # 한국어 음성 보장 (Windows 기본 설정에 따라 다를 수 있음)
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'Korean' in voice.name or 'KR' in voice.id:
                    self.engine.setProperty('voice', voice.id)
                    break
                    
            logger.info("TTS 엔진 초기화 성공")
        except Exception as e:
            logger.error(f"TTS 엔진 초기화 실패: {e}")

    def speak(self, text):
        """텍스트를 음성으로 출력합니다."""
        logger.info(f"TTS 출력: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS 출력 중 오류 발생: {e}")

# 사용 예시
# tts = TTSManager()
# tts.speak("독종 시스템을 시작합니다.")