from datetime import datetime, timezone
import os
import webbrowser
import subprocess

from config import Config

class Executor:
    def __init__(self):
        # 자주 사용하는 프로그램 경로 예시 (본인 환경에 맞게 수정 가능)
        self.apps = {
            "유튜브": r"C:\Users\tonyt\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Brave 앱\YouTube.lnk",
            "브챗": r"C:\Users\tonyt\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Steam\VRChat.url",
            "인스타": r"C:\Users\tonyt\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Chrome-Apps\Instagram.lnk",
            "롤": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Riot Games\League of Legends.lnk",
            "피파": r"C:\Users\tonyt\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Steam\FIFA 22.url",
            "팰월드": r"C:\Users\tonyt\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Steam\Palworld  팰월드.url",
            "제미나이": r"https://gemini.google.com/app?hl=de"
        }

    def execute(self, intent):
        action = intent.get("action")
        target = intent.get("target")
        info = intent.get("info")
        reply = intent.get("reply")

        if action == "execute":
            app_path = self.apps.get(target)
            
            path_to_run = app_path if app_path else f"경로 미설정: {target}"
            
            if target == "제미나이":
                webbrowser.open(path_to_run)
                return

            if not os.path.exists(path_to_run):
                print(f"❌ 파일 경로가 잘못되었습니다: {path_to_run}")
                return

            try:
                print(f"🚀 실행 시도: {path_to_run}")
                os.startfile(path_to_run)

                if target == "롤":
                    webbrowser.open(f"https://lol.ps/statistics")

            except Exception as e:
                print(f"❌ 실행 실패: {e}") 
            
        elif action == "search":
            # 웹 검색 또는 유튜브 열기
            print(f"🌐 검색/이동: {target}")
            if "유튜브" in target:
                webbrowser.open(f"https://www.youtube.com/results?search_query={info}")
            else:
                webbrowser.open(f"https://www.google.com/search?q={info}")

        elif action == "shutdown":
            print("⚠️ 시스템 종료 명령 감지")
            if target == "timer":
                print(f"⏰ {info}초 후에 시스템이 종료됩니다.")
                os.system(f"shutdown /s /t {info}") # info에 지정된 시간 후 종료, 취소하려면 'shutdown /a' 명령 실행
            elif target == "alarm":
                now =  datetime.now()
                info = datetime.fromisoformat(info)
                delta = info - now
                seconds_remaining = int(delta.total_seconds())
                print(f"⏰ {seconds_remaining}초 후에 시스템이 종료됩니다.")
                os.system(f"shutdown /s /t {seconds_remaining}") # info에 지정된 시간 후 종료, 취소하려면 'shutdown /a' 명령 실행
            else:
                print("❌ 알 수 없는 shutdown 타겟입니다.")

        elif action == "unknown":
            print("❓ 알 수 없는 명령입니다.")