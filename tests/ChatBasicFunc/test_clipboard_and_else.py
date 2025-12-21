import os
import time
from src.utils.logger import get_logger
from src.utils import login
from src.pages.chat_basic_page import ChatBasicPage
from data.config import USERNAME1, PASSWORD1
from data.chat_basic_data import TEXT9, TEXT10

# === logger 설정 시작 ===
logger  = get_logger(__file__)
# === logger 설정 끝 ===

# === 환경 변수 설정 ===
BASE_URL = os.environ.get("BASE_URL", "https://qaproject.elice.io")
WAIT_TIMEOUT = 200

## 클립보드 기능 테스트
def test_chat_clipboard(driver):
    
    chat_basic_page = ChatBasicPage(driver)

    logger.info(" [SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USERNAME1, PASSWORD1)
    
    logger.info(" [SETUP] ⚙️ 액션: 1. 클립보드 복사 시작")
    chat_basic_page.send_message(TEXT9)
    chat_basic_page.clipboard_capy_for_text()
    logger.info(" ✅ 검증 성공: 1. 클립보드 복사 완료")
    
## 스크롤 이동 기능 테스트
def test_chat_edit(driver):
    chat_basic_page = ChatBasicPage(driver)

    logger.info(" [SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USERNAME1, PASSWORD1)
    
    logger.info(" [SETUP] ⚙️ 액션: 1. 대화중 상단으로 스크롤 이동 시작")
    chat_basic_page.send_message(TEXT10)
    chat_basic_page.screenshot("before")
    chat_basic_page.scroll_up()
    time.sleep(5)
    chat_basic_page.screenshot("after")
    logger.info(" ✅ 검증 성공: 1. 대화중 상단으로 스크롤 이동 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 2. 대화중 상단으로 스크롤 이동후 화살표 클릭 스크롤 아래로 이동 시작")
    chat_basic_page.send_message(TEXT10)
    chat_basic_page.scroll_up()
    time.sleep(5)
    chat_basic_page.screenshot("before")
    chat_basic_page.scroll_down()
    time.sleep(2)
    chat_basic_page.screenshot("after")
    logger.info(" ✅ 검증 성공: 2. 대화중 상단으로 스크롤 이동후 화살표 클릭 스크롤 아래로 이동 완료")