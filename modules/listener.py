import pvporcupine
import pyaudio
import struct
from config import Config
import wave

class Listener:
    def __init__(self):
        # Picovoice 설정 및 호출어 경로 지정
        self.porcupine = pvporcupine.create(
            access_key=Config.PICOVOICE_KEY,
            keyword_paths=[Config.WAKE_WORD_PATH],
            model_path=Config.MODEL_PATH
        )
        
        # 마이크 스트림 설정
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def listen_for_wake_word(self):
        """호출어가 들릴 때까지 대기하는 루프"""
        print(f"👂 'Dokjong' 호출을 기다리는 중...")
        
        try:
            while True:
                # 마이크에서 데이터 읽기
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack(f"{self.porcupine.frame_length}h", pcm)

                # 호출어 감지 여부 확인
                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    print("🔥 호출어 감지! 명령을 들을 준비가 되었습니다.")
                    return True
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return False

    def cleanup(self):
        """리소스 해제"""
        if self.audio_stream is not None:
            self.audio_stream.close()
        if self.pa is not None:
            self.pa.terminate()
        if self.porcupine is not None:
            self.porcupine.delete()

    def record_command(self, seconds=6):
        """호출어 감지 후 사용자의 명령을 녹음하여 파일로 저장"""
        output_path = "command.wav"
        print(f"🎤 듣고 있습니다... ({seconds}초)")
        
        frames = []
        # 초당 프레임 수를 계산하여 지정된 시간만큼 녹음
        for _ in range(0, int(self.porcupine.sample_rate / self.porcupine.frame_length * seconds)):
            data = self.audio_stream.read(self.porcupine.frame_length)
            frames.append(data)
            
        print("✅ 녹음 완료.")

        # WAV 파일로 저장
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.pa.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.porcupine.sample_rate)
            wf.writeframes(b''.join(frames))
            
        return output_path

if __name__ == "__main__":
    # 독립 테스트용 코드
    listener = Listener()
    try:
        if listener.listen_for_wake_word():
            print("동작 확인 완료!")
    finally:
        listener.cleanup()