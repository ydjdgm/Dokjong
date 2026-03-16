from konlpy.tag import Okt
from logger import get_logger

logger = get_logger("NLP_Processor")

class NLPProcessor:
    def __init__(self):
        logger.info("KoNLPy (Okt) 형태소 분석기 초기화 중...")
        try:
            self.okt = Okt()
            logger.info("KoNLPy 초기화 완료")
        except Exception as e:
            logger.error(f"KoNLPy 초기화 실패 (Java 환경 변수 확인 필요): {e}")

    def extract_keywords(self, text):
        """문장에서 명사, 동사, 형용사 등 유의미한 형태소만 추출 후 어간 추출(stemming) 적용"""
        if not text:
            return ""
        
        try:
            # 주요 품사만 추출 및 어간(기본형) 추출 처리
            pos_tags = self.okt.pos(text, stem=True)
            keywords = [word for word, pos in pos_tags if pos in ['Noun', 'Verb', 'Adjective', 'Alpha']]
            
            processed_text = " ".join(keywords)
            logger.debug(f"텍스트 전처리 완료: '{text}' -> '{processed_text}'")
            return processed_text
        except Exception as e:
            logger.error(f"형태소 분석 중 오류 발생: {e}")
            return text