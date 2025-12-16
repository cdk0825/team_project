# pytest fixture 및 공통 설정 정의
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from src.pages.main_page import MainPage
from src.utils import login
from src.config import USERNAME, PASSWORD

@pytest.fixture
def driver():
    """크롬 브라우저를 열고 테스트 후 닫는 pytest fixture"""
    options = webdriver.ChromeOptions()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)  # Chrome 브라우저 열기
    driver.implicitly_wait(5)  # 암묵적 대기: 요소 로딩 최대 5초까지 대기
    yield driver
    driver.delete_all_cookies()
    driver.quit()  # 테스트 완료 후 브라우저 닫기

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