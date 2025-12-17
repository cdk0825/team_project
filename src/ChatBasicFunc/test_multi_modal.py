import os
import time
import pytest

from src.utils import login
from src.pages.chat_basic_page import ChatBasicPage
from src.config import USERNAME1, PASSWORD1


# === 환경 변수 설정 ===
BASE_URL = os.environ.get("BASE_URL", "https://qaproject.elice.io")
WAIT_TIMEOUT = 200

def test_multi_modal(driver):
    chat_basic_page = ChatBasicPage(driver)
    
    print("\n [SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USERNAME1, PASSWORD1)
    
    print("\n [SETUP] ⚙️ 액션: 1. 채팅창 배지 확인 시작")
    chat_basic_page.chat_badge_check()
    print("✅ 검증 성공: 1. 채팅창 배지 확인 완료")