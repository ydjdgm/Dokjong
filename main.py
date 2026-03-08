from modules.listener import Listener
from modules.brain import Brain
from modules.executor import Executor
from modules.speaker import Speaker

def main():
    listener = Listener()
    brain = Brain()
    executor = Executor()
    speaker = Speaker()
    
    speaker.say("독종이 시작되었습니다.")

    try:
        while True:
            if listener.listen_for_wake_word():
                # 1. 녹음 (6초)
                speaker.say("네.")
                audio_file = listener.record_command(seconds=6)
                
                # 2. 텍스트 변환
                text = brain.speech_to_text(audio_file)
                print(f"💬 인식된 문장: {text}")
                
                if text.strip():
                    # 3. 의도 파악
                    intent = brain.understand_intent(text)
                    print(f"🧠 판단 결과: {intent}")
                    
                    # 4. 음성 응답
                    speaker.say(intent.get("reply", "네, 알겠습니다."))
                    
                    # 5. 실제 실행
                    executor.execute(intent)
                else:
                    speaker.say("말씀이 없으셔서 대기 모드로 돌아갑니다.")
                
    except KeyboardInterrupt:
        speaker.say("시스템을 종료합니다. 다음에 뵙겠습니다.")
    finally:
        listener.cleanup()

if __name__ == "__main__":
    main()