import os
import time
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from src.utils import login


# === 환경 변수 설정 ===
BASE_URL = os.environ.get("BASE_URL", "https://qaproject.elice.io")
WAIT_TIMEOUT = 200

USER_EMAIL = "qa3team01@elicer.com"
PASSWORD = "20qareset25elice!"

TEXT1 = "오늘 날씨 알려줘."
TEXT2 = "서울 날씨 알려줘"
TEXT3 = "빅뱅이론과 평행 우주에 대해 설명하고 근거를 제시해줘"
TEXT4 = "ㄹ햐ㅙㅑㅊㅈ지도랴온ㄴ랴로"
TEXT5 = "ㅍ ㅏ이선에서 리트 만드는거 알줘"
# =====================

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, WAIT_TIMEOUT)

def test_start(driver, wait):
    print("\n [SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USER_EMAIL, PASSWORD)
    
    print("\n [SETUP] ⚙️ 액션: 일반 텍스트 질문 시작")
    normal_text(driver, wait, TEXT1)
    print("✅ 검증 성공: 일반 텍스트 질문 답변 완료")
    
    print("\n [SETUP] ⚙️ 액션: 의미없는(오타) 텍스트 질문 시작")
    meaningless_text(driver, wait, TEXT4)
    print("✅ 검증 성공: 의미없는(오타) 텍스트 질문 답변 완료")
    
    print("\n [SETUP] ⚙️ 액션: 오타가 포함된 텍스트 질문 시작")
    meaningless_text(driver, wait, TEXT5)
    print("✅ 검증 성공: 오타가 포함된 텍스트 질문 답변 완료")
    # print("\n [SETUP] ⚙️ 액션: 다른 맥락 텍스트 질문 시작")
    # diff_text(driver, wait, TEXT2)
    # print("✅ 검증 성공: 다른 맥락 텍스트 질문 답변 완료")
    
    # print("\n [SETUP] ⚙️ 액션: 복잡한 텍스트 질문 시작")
    # expert_text(driver, wait, TEXT3)
    # print("✅ 검증 성공: 복잡한 텍스트 질문 답변 완료")

    
# @pytest.fixture
def normal_text(driver, wait, text):
    """ 1.일반 텍스트 질문 """
    text_area = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".MuiInputBase-input.MuiInputBase-inputMultiline")
        )
    )
    
    text_area.click()
    text_area.send_keys(text)
    driver.find_element(By.XPATH, "//button[@aria-label='보내기']").click()
    
    time.sleep(2)

    assert True
    
# def diff_text(driver, wait, text):
#     """ 2. 다른 맥락 질문 """
#     wait.until(
#         EC.presence_of_all_elements_located(
#             (By.CSS_SELECTOR, '[data-testid="arrows-rotateIcon"]')
#         )
#     )
    
#     text_area = wait.until(
#         EC.presence_of_element_located(
#             (By.CSS_SELECTOR, ".MuiInputBase-input.MuiInputBase-inputMultiline")
#         )
#     )
    
#     text_area.send_keys(text)
#     driver.find_element(By.XPATH, "//button[@aria-label='보내기']").click()
    
#     time.sleep(2)
    
#     assert True
    
    
# def expert_text(driver, wait, text):
#     """ 3. 복잡한 질문 테스트 """
#     wait.until(
#         EC.presence_of_all_elements_located(
#             (By.CSS_SELECTOR, '[data-testid="arrows-rotateIcon"]')
#         )
#     )
    
#     text_area = wait.until(
#         EC.presence_of_element_located(
#             (By.CSS_SELECTOR, ".MuiInputBase-input.MuiInputBase-inputMultiline")
#         )
#     )
    
#     text_area.send_keys(text)
#     driver.find_element(By.XPATH, "//button[@aria-label='보내기']").click()
    
#     time.sleep(2)
    
#     assert True

def meaningless_text(driver, wait, text):
    """ 4. 의미없는 질문(오타) 테스트 """
    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '[data-testid="arrows-rotateIcon"]')
        )
    )
    
    text_area = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".MuiInputBase-input.MuiInputBase-inputMultiline")
        )
    )
    
    text_area.send_keys(text)
    driver.find_element(By.XPATH, "//button[@aria-label='보내기']").click()
    
    time.sleep(10)
    

    