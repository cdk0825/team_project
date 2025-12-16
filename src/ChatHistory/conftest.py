import pytest
from src.pages.main_page import MainPage
from src.utils import login
from src.config import USERNAME, PASSWORD

@pytest.fixture
def logged_in_main_page_setup(driver):
    print("\n[SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USERNAME, PASSWORD)
    print("[SETUP] ✅ 액션: 관리자 로그인 완료")

    main = MainPage(driver)

    return main

@pytest.fixture
def logged_in_driver(driver):
    print("\n[SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USERNAME, PASSWORD)
    print("[SETUP] ✅ 액션: 관리자 로그인 완료")

    MainPage(driver)

    return driver