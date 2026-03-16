import os
from logger import get_logger

logger = get_logger("SystemController")

class SystemController:
    @staticmethod
    def execute_shutdown():
        """PC 시스템 종료 수행"""
        logger.info("시스템 종료 명령 실행")
        # Windows OS 기준 즉시 종료 명령어
        os.system("shutdown /s /t 0")

    @staticmethod
    def execute_restart():
        """PC 시스템 재부팅 수행"""
        logger.info("시스템 재부팅 명령 실행")
        os.system("shutdown /r /t 0")