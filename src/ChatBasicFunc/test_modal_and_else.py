import os
import time
import pytest

from src.utils import login
from src.pages.chat_basic_page import chatBasicPage


# === 환경 변수 설정 ===
BASE_URL = os.environ.get("BASE_URL", "https://qaproject.elice.io")
WAIT_TIMEOUT = 200

USER_EMAIL = "qa3team01@elicer.com"
PASSWORD = "20qareset25elice!"



TEXT1 = "파이선에 대해 설명해줘"

def test_chat_edit(driver):
    chat_basic_page = chatBasicPage(driver)

    print("\n [SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USER_EMAIL, PASSWORD)
    
    print("\n [SETUP] ⚙️ 액션: 1. 대화중 상단으로 스크롤 이동 시작")
    chat_basic_page.send_message(TEXT1)
    chat_basic_page.screenshot("before")
    chat_basic_page.scroll_up()
    time.sleep(5)
    chat_basic_page.screenshot("after")
    print("✅ 검증 성공: 1. 대화중 상단으로 스크롤 이동 완료")
    
    print("\n [SETUP] ⚙️ 액션: 2. 대화중 상단으로 스크롤 이동후 화살표 클릭 스크롤 아래로 이동 시작")
    chat_basic_page.send_message(TEXT1)
    chat_basic_page.scroll_up()
    time.sleep(5)
    chat_basic_page.screenshot("before")
    chat_basic_page.scroll_down()
    time.sleep(2)
    chat_basic_page.screenshot("after")
    print("✅ 검증 성공: 2. 대화중 상단으로 스크롤 이동후 화살표 클릭 스크롤 아래로 이동 완료")