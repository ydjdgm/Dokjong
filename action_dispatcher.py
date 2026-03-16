from system_controller import SystemController
from app_controller import AppController
from logger import get_logger

logger = get_logger("ActionDispatcher")

class ActionDispatcher:
    def __init__(self):
        self.system_ctrl = SystemController()
        self.app_ctrl = AppController()
        
        # commands.json의 'action' 값과 실행할 메서드를 딕셔너리로 매핑
        self.action_map = {
            "execute_shutdown": self.system_ctrl.execute_shutdown,
            # "execute_discord_mute": self.app_ctrl.execute_discord_mute,
            "execute_youtube_open": self.app_ctrl.execute_youtube_open,
            "execute_youtube_search": self.app_ctrl.execute_youtube_search,
            "execute_youtube_play_target": self.app_ctrl.execute_youtube_play_target,
            "execute_youtube_play_pause": self.app_ctrl.execute_youtube_play_pause
        }

    def dispatch(self, action_name, user_text=""):
        """action 문자열을 받아 매핑된 함수를 실행"""
        if not action_name:
            logger.warning("실행할 액션 이름이 전달되지 않았습니다.")
            return False

        action_func = self.action_map.get(action_name)
        
        if action_func:
            logger.info(f"액션 매핑 성공 및 실행: {action_name}")
            try:
                action_func(user_text)
            except TypeError:
                action_func()
            return True
        else:
            logger.error(f"등록되지 않은 액션입니다: {action_name}")
            return False