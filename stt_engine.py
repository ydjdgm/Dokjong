import whisper
from logger import get_logger

logger = get_logger("STT_Engine")

class STTEngine:
    def __init__(self, model_size="base"):
        """
        model_size: 'tiny', 'base', 'small', 'medium', 'large' 중 선택 가능.
        성능과 속도의 타협점인 'base' 또는 'small' 권장.
        """
        logger.info(f"Whisper 모델({model_size}) 로드 중... (초기 1회 시간 소요)")
        try:
            self.model = whisper.load_model(model_size)
            logger.info("Whisper 모델 로드 완료")
        except Exception as e:
            logger.error(f"Whisper 모델 로드 실패: {e}")

    def transcribe(self, audio_filepath):
        """저장된 오디오 파일을 텍스트로 변환"""
        if not audio_filepath:
            return ""

        logger.info(f"음성 인식 분석 시작: {audio_filepath}")
        try:
            # 한국어로 고정하여 처리 속도 및 정확도 향상
            result = self.model.transcribe(audio_filepath, language="ko")
            text = result.get("text", "").strip()
            logger.info(f"STT 인식 결과: {text}")
            return text
        except Exception as e:
            logger.error(f"STT 변환 중 오류 발생: {e}")
            return ""