import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name="Dokjong"):
    logger = logging.getLogger(name)
    
    # 이미 핸들러가 설정되어 있다면 중복 추가 방지
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    # 로그 포맷 정의
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. 콘솔 출력 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 2. 파일 출력 핸들러 (logs 폴더 생성)
    if not os.path.exists("logs"):
        os.makedirs("logs")
        
    file_handler = RotatingFileHandler(
        filename="logs/dokjong.log", 
        maxBytes=5 * 1024 * 1024, # 5MB
        backupCount=3, 
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# 사용 예시
# logger = get_logger()
# logger.info("로깅 시스템 초기화 완료")