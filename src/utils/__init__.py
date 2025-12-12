# loginlogout/login.py
# 공통 유틸리티 함수 및 헬퍼 모듈
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pytest

# 드라이버

options = Options()
# Headless 모드 실행 (UI 없이 백그라운드 실행, 필요에 따라 활성화)
# options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options, service=service)  # Chrome 브라우저 열기
driver.implicitly_wait(5)  # 암묵적 대기: 요소 로딩 최대 5초까지 대기
driver.get("https://qaproject.elice.io/ai-helpy-chat")

@pytest.fixture
def test_login_admin_success():
    # 사용자명과 비밀번호 입력
    driver.find_element(By.NAME, "loginId").send_keys("qa3team01@elicer.com")
    driver.find_element(By.NAME, "password").send_keys("20qareset25elice!")
    # 로그인 버튼 클릭
    driver.find_element(By.ID, ":r3:").click()
    # 결과 확인: 대시보드로 이동하여 환영 메시지 표시 확인
    driver.find_element(By.CSS_SELECTOR, '.MuiAvatar-root').click()
    welcome_id = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/ul/div/div[1]/button/div/div/div[2]/div/p').text
    welcome_email = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/ul/div/div[1]/button/div/div/div[2]/p').text
    print("ID:", welcome_id)
    print("Email:", welcome_email)

    assert "team01" in welcome_id  # 환영 메시지가 포함되어 있는지 검증
    assert "qa3team01@elicer.com" in welcome_email  # 환영 메시지가 포함되어 있는지 검증