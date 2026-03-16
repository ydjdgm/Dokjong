import sys
import time
from logger import get_logger
from tts_engine import TTSManager
from wake_word import WakeWordDetector
from vad_recorder import VADRecorder
from stt_engine import STTEngine
from intent_analyzer import IntentAnalyzer
from action_dispatcher import ActionDispatcher
import os
from dotenv import load_dotenv

load_dotenv()
logger = get_logger("MainApp")

# TODO: 본인의 Picovoice Access Key 및 모델 경로로 변경 필요
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")
KEYWORD_PATH = "Dokjong_ko_windows_v4_0_0.ppn"
MODEL_PATH = "porcupine_params_ko.pv"

def main():
    logger.info("=== 프로젝트 '독종' 시스템 초기화 시작 ===")
    
    # 1. 시스템 모듈 초기화
    tts = TTSManager()
    wake_word = WakeWordDetector(access_key=PORCUPINE_ACCESS_KEY, keyword_path=KEYWORD_PATH, model_path=MODEL_PATH)
    vad = VADRecorder()
    stt = STTEngine(model_size="base")
    analyzer = IntentAnalyzer()
    dispatcher = ActionDispatcher()

    if not wake_word.initialize():
        logger.critical("호출어 모듈 초기화 실패. 시스템을 종료합니다.")
        sys.exit(1)

    tts.speak("독종 시스템이 준비되었습니다.")
    logger.info("=== 시스템 초기화 완료. 호출어 대기 모드 진입 ===")

    # 2. 메인 이벤트 루프
    try:
        while True:
            # 호출어 대기 (블로킹 함수)
            if wake_word.listen():
                # 호출어 감지 성공 시 피드백
                tts.speak("네, 말씀하세요.")
                
                # VAD 기반 녹음
                audio_file = vad.record_until_silence(output_filename="temp_command.wav", silence_duration_sec=1.5)
                
                if audio_file:
                    # STT 변환
                    text = stt.transcribe(audio_file)
                    
                    if text:
                        # 의도 추론
                        result = analyzer.analyze_intent(text)
                        
                        if result:
                            action = result["action"]
                            # 액션 실행
                            success = dispatcher.dispatch(action, text)
                            if success:
                                tts.speak("명령을 수행했습니다.")
                            else:
                                tts.speak("명령 실행 중 문제가 발생했습니다.")
                        else:
                            tts.speak("무슨 말씀인지 잘 이해하지 못했어요.")
                    else:
                        logger.warning("음성이 텍스트로 변환되지 않았습니다.")
                
                logger.info("명령 처리 완료. 다시 호출어 대기 모드로 돌아갑니다.")
                time.sleep(1) # 루프 안정성을 위한 짧은 대기

    except KeyboardInterrupt:
        logger.info("사용자에 의해 시스템이 종료됩니다.")
    except Exception as e:
        logger.critical(f"시스템 실행 중 치명적인 오류 발생: {e}")
    finally:
        # 3. 자원 해제
        wake_word.cleanup()
        logger.info("=== 독종 시스템이 안전하게 종료되었습니다. ===")

if __name__ == "__main__":
    main()