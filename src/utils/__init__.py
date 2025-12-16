# loginlogout/login.py
# 공통 유틸리티 함수 및 헬퍼 모듈
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import os

def login(driver, USERNAME, PASSWORD):
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    driver.find_element(By.NAME, "loginId").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Login']"))
    ).click()

def go_to_join(driver):
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    driver.delete_all_cookies()
    driver.find_element(By.LINK_TEXT, "Create account").click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Create account with email']"))
    ).click()

def capture_screenshot(driver, save_path="reports/screenshots", title="screenshot"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{title}_{timestamp}.png"

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    full_path = os.path.join(save_path, file_name)

    try:
        driver.save_screenshot(full_path)
        print(f"✅ 스크린샷이 성공적으로 저장되었습니다: {full_path}")
    except Exception as e:
        print(f"❌ 스크린샷 저장 중 오류 발생: {e}")

