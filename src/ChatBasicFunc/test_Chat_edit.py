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

def test_chat_edit(driver):
    chat_basic_page = chatBasicPage(driver)

    print("\n [SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USER_EMAIL, PASSWORD)