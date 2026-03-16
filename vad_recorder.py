import webrtcvad
import pyaudio
import wave
from logger import get_logger

logger = get_logger("VAD_Recorder")

class VADRecorder:
    def __init__(self, sample_rate=16000, chunk_duration_ms=30):
        self.sample_rate = sample_rate
        self.chunk_duration_ms = chunk_duration_ms
        self.chunk_size = int(sample_rate * chunk_duration_ms / 1000)
        self.vad = webrtcvad.Vad(3) # 공격성 레벨 (0~3, 3이 가장 묵음에 민감함)
        self.pa = pyaudio.PyAudio()

    def record_until_silence(self, output_filename="temp_audio.wav", silence_duration_sec=1.5):
        stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        logger.info("발화 대기 및 녹음 시작...")
        frames = []
        silence_chunks = 0
        max_silence_chunks = int(silence_duration_sec * 1000 / self.chunk_duration_ms)
        has_spoken = False

        try:
            while True:
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                is_speech = self.vad.is_speech(data, self.sample_rate)

                if is_speech:
                    has_spoken = True
                    silence_chunks = 0
                    frames.append(data)
                else:
                    if has_spoken:
                        silence_chunks += 1
                        frames.append(data)
                    
                    if has_spoken and silence_chunks > max_silence_chunks:
                        logger.info("묵음 감지됨. 녹음 종료.")
                        break
        except Exception as e:
            logger.error(f"녹음 중 오류 발생: {e}")
        finally:
            stream.stop_stream()
            stream.close()

        if frames:
            self._save_wave(output_filename, frames)
            return output_filename
        return None

    def _save_wave(self, filename, frames):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.pa.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        logger.info(f"임시 오디오 저장 완료: {filename}")