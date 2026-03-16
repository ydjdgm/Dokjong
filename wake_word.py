import pvporcupine
import pyaudio
import struct
from logger import get_logger

logger = get_logger("WakeWord")

class WakeWordDetector:
    def __init__(self, access_key, keyword_path, model_path):
        self.access_key = access_key
        self.keyword_path = keyword_path
        self.model_path = model_path
        self.porcupine = None
        self.pa = None
        self.audio_stream = None

    def initialize(self):
        """Porcupine 및 오디오 스트림 초기화"""
        try:
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keyword_paths=[self.keyword_path],
                model_path=self.model_path
            )
            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            logger.info("호출어 감지 모듈 초기화 완료")
            return True
        except Exception as e:
            logger.error(f"호출어 감지 모듈 초기화 실패: {e}")
            return False

    def listen(self):
        """마이크 입력을 모니터링하며 호출어 대기"""
        if not self.audio_stream:
            logger.error("오디오 스트림이 초기화되지 않았습니다.")
            return False

        logger.info("호출어('독종') 대기 중...")
        try:
            while True:
                pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                
                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    logger.info("호출어 감지됨!")
                    return True
        except KeyboardInterrupt:
            logger.info("호출어 대기 중단")
            return False

    def cleanup(self):
        """리소스 해제"""
        if self.audio_stream:
            self.audio_stream.close()
        if self.pa:
            self.pa.terminate()
        if self.porcupine:
            self.porcupine.delete()
        logger.info("호출어 감지 리소스 해제 완료")

# 사용 예시
# detector = WakeWordDetector(access_key="YOUR_ACCESS_KEY", keyword_path="dokjong_windows.ppn")
# if detector.initialize():
#     detector.listen()