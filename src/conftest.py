# pytest fixture 및 공통 설정 정의
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest


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