import os
import webbrowser
import subprocess

class Executor:
    def __init__(self):
        # 자주 사용하는 프로그램 경로 예시 (본인 환경에 맞게 수정 가능)
        self.apps = {
            "크롬": "chrome.exe",
            "메모장": "notepad.exe",
            "계산기": "calc.exe",
            "유튜브": r"C:\Users\tonyt\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Brave 앱\YouTube.lnk",
            "브챗": r"C:\Users\tonyt\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Steam\VRChat.url",
            "인스타": r"C:\Users\tonyt\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Chrome-Apps\Instagram.lnk"
        }

    def execute(self, intent):
        action = intent.get("action")
        target = intent.get("target")

        if action == "execute":
            # 1. 별칭(예: 카카오톡)이 등록되어 있는지 확인
            app_path = self.apps.get(target)
            
            # 2. 등록되지 않았다면 Gemini가 준 target을 그대로 경로로 사용
            path_to_run = app_path if app_path else target
            
            if not os.path.exists(path_to_run):
                print(f"❌ 파일 경로가 잘못되었습니다: {path_to_run}")
                return

            try:
                print(f"🚀 실행 시도: {path_to_run}")
                os.startfile(path_to_run) # os.system보다 훨씬 안정적!
            except Exception as e:
                print(f"❌ 실행 실패: {e}") 
            
        elif action == "search":
            # 웹 검색 또는 유튜브 열기
            print(f"🌐 검색/이동: {target}")
            if "유튜브" in target:
                webbrowser.open("https://www.youtube.com")
            else:
                webbrowser.open(f"https://www.google.com/search?q={target}")

        elif action == "shutdown":
            # 시스템 종료 (실수 방지를 위해 주석 처리 해둠, 테스트 후 해제)
            print("⚠️ 시스템 종료 명령 감지")
            os.system("shutdown /s /t 60") # 60초 후 종료, 취소하려면 'shutdown /a' 명령 실행
            
        elif action == "unknown":
            print("❓ 알 수 없는 명령입니다.")