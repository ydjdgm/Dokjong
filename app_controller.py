import os
import time
import keyboard
import Levenshtein
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger import get_logger

logger = get_logger("AppController")

class AppController:
    def __init__(self):
        # 브라우저 세션 유지를 위한 드라이버 인스턴스 변수
        self.driver = None

    def _get_or_create_driver(self):
        """드라이버가 없으면 생성하고, 있으면 재사용합니다."""
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            profile_dir = os.path.join(os.getcwd(), "chrome_profile")
            chrome_options.add_argument(f"user-data-dir={profile_dir}")

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": " Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) "
            })
        return self.driver

    def _extract_keyword(self, text):
        """발화에서 불필요한 명령어 키워드를 제거하여 타겟 명사만 추출합니다."""
        stopwords = ["유튜브", "검색", "해줘", "찾아", "영상", "틀어", "재생", "채널", "에서", "줘"]
        words = text.split()
        filtered_words = [word for word in words if not any(stop in word for stop in stopwords)]
        return " ".join(filtered_words).strip()

    def execute_youtube_open(self, user_text=""):
        logger.info("유튜브 기본 브라우저 실행")
        driver = self._get_or_create_driver()
        driver.get("https://www.youtube.com")

    def execute_youtube_search(self, user_text):
        keyword = self._extract_keyword(user_text)
        if not keyword:
            logger.warning("검색할 키워드가 추출되지 않았습니다.")
            return

        logger.info(f"유튜브 검색 실행: {keyword}")
        driver = self._get_or_create_driver()
        
        if "youtube.com" not in driver.current_url:
            driver.get("https://www.youtube.com")
            
        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_query"))
            )
            # 입력 전 기존 텍스트 지우기 (Ctrl+A -> Backspace)
            search_box.send_keys(Keys.CONTROL + "a")
            search_box.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.RETURN)
        except Exception as e:
            logger.error(f"유튜브 검색 실패: {e}")

    def execute_youtube_play_target(self, user_text):
        keyword = self._extract_keyword(user_text)
        logger.info(f"유튜브 타겟 영상 탐색 및 재생: {keyword}")
        driver = self._get_or_create_driver()

        try:
            time.sleep(2) # 검색 결과 DOM 렌더링 대기
            videos = driver.find_elements(By.TAG_NAME, "ytd-video-renderer") # 검색 결과창 기준
            if not videos:
                videos = driver.find_elements(By.TAG_NAME, "ytd-rich-item-renderer") # 홈 화면 기준

            best_match = None
            highest_score = 0.0

            for video in videos:
                try:
                    title_elem = video.find_element(By.ID, "video-title")
                    title_text = title_elem.text
                    
                    try:
                        channel_elem = video.find_element(By.ID, "channel-name")
                        channel_text = channel_elem.text
                    except:
                        channel_text = ""

                    combined_text = f"{title_text} {channel_text}"
                    
                    # Levenshtein 유사도 계산
                    distance = Levenshtein.distance(keyword, combined_text)
                    max_len = max(len(keyword), len(combined_text))
                    score = 1.0 - (distance / max_len) if max_len > 0 else 0

                    # 키워드가 텍스트 안에 포함되어 있으면 가산점 부여 (정확도 향상)
                    if keyword.replace(" ", "") in combined_text.replace(" ", ""):
                        score += 0.5

                    if score > highest_score:
                        highest_score = score
                        best_match = title_elem
                except:
                    continue

            if best_match:
                logger.info(f"가장 유사한 영상 클릭 (Score: {highest_score:.2f})")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", best_match)
                time.sleep(0.5) # 스크롤 이동 후 렌더링 안정화 대기
                driver.execute_script("arguments[0].click();", best_match)
            else:
                logger.warning("화면에서 일치하는 영상을 찾지 못했습니다.")
        except Exception as e:
            logger.error(f"영상 타겟팅 재생 중 오류 발생: {e}")

    def execute_youtube_play_pause(self, user_text=""):
        logger.info("유튜브 재생/일시정지 토글")
        keyboard.send("k")