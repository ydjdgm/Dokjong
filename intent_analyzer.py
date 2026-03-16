import json
from sentence_transformers import SentenceTransformer, util
import Levenshtein
from logger import get_logger

logger = get_logger("IntentAnalyzer")

class IntentAnalyzer:
    def __init__(self, commands_file="commands.json", model_name="snunlp/KR-SBERT-V40K-klueNLI-augSTS"):
        self.commands = self._load_commands(commands_file)
        
        logger.info(f"S-BERT 모델({model_name}) 로드 중...")
        try:
            self.model = SentenceTransformer(model_name)
            logger.info("S-BERT 모델 로드 완료")
        except Exception as e:
            logger.error(f"S-BERT 모델 로드 실패: {e}")
        
        # 명령어의 임베딩 텐서를 미리 계산하여 응답 속도 최적화
        self.intent_embeddings = self._precompute_embeddings()

    def _load_commands(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("system_controls", [])
        except Exception as e:
            logger.error(f"명령어 맵 로드 실패: {e}")
            return []

    def _precompute_embeddings(self):
        """각 intent의 예상 발화들에 대한 임베딩을 초기화 시점에 미리 계산"""
        embeddings = {}
        for item in self.commands:
            intent = item["intent"]
            utterances = item["expected_utterances"]
            if utterances:
                embeddings[intent] = self.model.encode(utterances, convert_to_tensor=True)
        return embeddings

    def analyze_intent(self, user_text, threshold=0.5):
        """S-BERT 의미 유사도와 Levenshtein 형태 유사도를 종합하여 사용자 의도 파악"""
        if not user_text:
            return None

        best_intent = None
        highest_score = 0.0
        best_action = None

        user_embedding = self.model.encode(user_text, convert_to_tensor=True)

        for item in self.commands:
            intent = item["intent"]
            action = item["action"]
            
            # 1. 의미적 유사도 계산 (S-BERT)
            if intent in self.intent_embeddings:
                cosine_scores = util.pytorch_cos_sim(user_embedding, self.intent_embeddings[intent])
                max_semantic_score = cosine_scores.max().item()
            else:
                max_semantic_score = 0.0

            # 2. 형태적 유사도 계산 (Levenshtein)
            max_lexical_score = 0.0
            for utterance in item["expected_utterances"]:
                distance = Levenshtein.distance(user_text, utterance)
                max_len = max(len(user_text), len(utterance))
                lexical_score = 1.0 - (distance / max_len) if max_len > 0 else 0
                if lexical_score > max_lexical_score:
                    max_lexical_score = lexical_score

            # 종합 점수 산정: 의미 유사도와 형태 유사도 중 더 높은 값을 채택
            combined_score = max(max_semantic_score, max_lexical_score)

            if intent == "youtube_search" and any(w in user_text for w in ["검색", "찾아"]):
                combined_score += 0.25
            elif intent == "youtube_play_target" and any(w in user_text for w in ["틀어", "재생"]):
                # "유튜브 재생해"(play_pause)와 겹치는 것을 막기 위해 "영상"이나 "채널" 등 목적어가 있는 경우에만 타겟 재생으로 간주
                if not ("유튜브 재생해" in user_text or "멈춰" in user_text):
                    combined_score += 0.25
            elif intent == "youtube_play_pause" and any(w in user_text for w in ["멈춰", "정지"]):
                combined_score += 0.25

            if combined_score > highest_score:
                highest_score = combined_score
                best_intent = intent
                best_action = action

        highest_score = min(highest_score, 1.0)
        logger.info(f"의도 추론 결과: '{user_text}' -> {best_intent} (Score: {highest_score:.2f})")

        # 설정된 임계치(기본 80%) 이상일 경우에만 유효 명령으로 반환
        if highest_score >= threshold:
            return {
                "intent": best_intent, 
                "action": best_action, 
                "score": highest_score
            }
        else:
            logger.warning(f"유효 임계치({threshold}) 도달 실패. 일치하는 명령어를 찾지 못했습니다.")
            return None