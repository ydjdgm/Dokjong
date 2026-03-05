import pyttsx3

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        # 목소리 설정 (한국어 음성 선택)
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "Korean" in voice.name or "Heami" in voice.name:
                self.engine.setProperty('voice', voice.id)
                break
        
        self.engine.setProperty('rate', 180) # 말하기 속도

    def say(self, text):
        print(f"📢 Dokjong: {text}")
        self.engine.say(text)
        self.engine.runAndWait()