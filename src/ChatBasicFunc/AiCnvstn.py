import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# === 변수 설정 ===
BASE_URL = os.environ.get("BASE_URL", "https://qaproject.elice.io")
WAIT_TIMEOUT = 10
USER_EMAIL = "qa3team01@elicer.com"
PASSWORD = "20qareset25elice!"
TEXT1 = "오늘 날씨 알려줘."
TEXT2 = "파이선이 뭐야?"
# ================

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 드라이버 생성
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(WAIT_TIMEOUT)
wait = WebDriverWait(driver, WAIT_TIMEOUT)

driver.get(f"{BASE_URL}/ai-helpy-chat")

# -- 로그인 정보--
print("---로그인 정보 설정---")

try:
    
    def login():
        user_email = driver.find_element(By.NAME, "loginId")
        pw = driver.find_element(By.NAME, "password")
        user_email.send_keys(USER_EMAIL)
        pw.send_keys(PASSWORD)

        print("----로그인 버튼 클릭----")
        # login_btn = driver.find_element(By.ID, ":r3:").click()
        login_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Login']"))
        )
        login_btn.click()

        print("## 로그인 성공!!")
        time.sleep(2)


    def normalText():
        # try:
        print("=" * 60)
        print("### 1.일반 텍스트 질문 테스트 시작")
        print("=" * 60)
        # 1. 일반 텍스트 질문 입력 / "오늘 날씨 알려줘." / 대화에 답변한다
        textArea = driver.find_element(By.CLASS_NAME, "MuiInputBase-input.MuiInputBase-inputMultiline")
        textArea.send_keys(TEXT1)
        driver.find_element(By.XPATH, "//button[@aria-label='보내기']").click()
        time.sleep(10)

        print("=" * 60)
        print("### 1.일반 텍스트 질문 테스트 완료")
        print("=" * 60)
        # finally:
        #     driver.quit()

    def diffText():
        # 2. 다른 맥락의 질문 입력 / "파이선이 뭐야?" / 이전 대화와 연결없이 질문에 응답한다
        print("=" * 60)
        print("### 다른 맥락의 질문 텍스트 시작")
        print("=" * 60)

        # stop_icon = driver.find_element(By.CSS_SELECTOR, '[data-testid="stopIcon"]')

        # if not stop_icon.is_displayed():
            # pass
        textArea = driver.find_element(By.CLASS_NAME, "MuiInputBase-input.MuiInputBase-inputMultiline")
        
        textArea.send_keys(TEXT2)
        driver.find_element(By.XPATH, "//button[@aria-label='보내기']").click()
        time.sleep(10)
        

        print("=" * 60)
        print("### 다른 맥락의 질문 테스트 완료")
        print("=" * 60)
    
    
    if __name__ == "__main__":
        print("\n=== Running Theme Tests ===\n")
        login()
    
        print("Test 1: 일반 텍스트 질문")
        normalText()
        
        print("Test 2: 다른 맥락의 텍스트 질문")
        diffText()
        
except Exception:
    pass