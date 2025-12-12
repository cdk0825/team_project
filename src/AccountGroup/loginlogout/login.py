# loginlogout/login.py
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

@pytest.fixture
def driver():
    """크롬 브라우저를 열고 테스트 후 닫는 pytest fixture"""
    options = webdriver.ChromeOptions()
    # Headless 모드 실행 (UI 없이 백그라운드 실행, 필요에 따라 활성화)
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)  # Chrome 브라우저 열기
    driver.implicitly_wait(5)  # 암묵적 대기: 요소 로딩 최대 5초까지 대기
    yield driver
    driver.quit()  # 테스트 완료 후 브라우저 닫기

def test_login_admin_success(driver):
    # 1. 로그인 페이지 접속
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    # 2. 사용자명과 비밀번호 입력
    driver.find_element(By.NAME, "loginId").send_keys("qa3team01@elicer.com")
    driver.find_element(By.NAME, "password").send_keys("20qareset25elice!")
    # 3. 로그인 버튼 클릭
    driver.find_element(By.ID, ":r3:").click()
    # 4. 결과 확인: 대시보드로 이동하여 환영 메시지 표시 확인
    driver.find_element(By.CSS_SELECTOR, '.MuiAvatar-root').click()
    welcome_id = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/ul/div/div[1]/button/div/div/div[2]/div/p').text
    welcome_email = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/ul/div/div[1]/button/div/div/div[2]/p').text
    print("ID:", welcome_id)
    print("Email:", welcome_email)

    assert "team01" in welcome_id  # 환영 메시지가 포함되어 있는지 검증
    assert "qa3team01@elicer.com" in welcome_email  # 환영 메시지가 포함되어 있는지 검증


# def test_login_fail_wrong_password(driver):
#     driver.get("http://example.com/login")
#     driver.find_element(By.NAME, "username").send_keys("testuser")
#     driver.find_element(By.NAME, "password").send_keys("wrong_password")
#     driver.find_element(By.ID, "login-btn").click()
#     error_msg = driver.find_element(By.CSS_SELECTOR, ".error-msg").text
#     assert "비밀번호가 올바르지 않습니다" in error_msg  # 오류 메시지 검증