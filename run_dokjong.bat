@echo off
:: 프로젝트 폴더로 이동
cd /d "C:\Users\tonyt\Documents\GitHub\Dokjong"

:: 가상환경의 일반 python.exe를 사용하여 실행
:: start 명령어를 제거하거나 /b 옵션을 빼면 창이 유지됩니다.
"venv\Scripts\python.exe" main.py

pause