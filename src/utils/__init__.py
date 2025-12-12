# loginlogout/login.py
# 공통 유틸리티 함수 및 헬퍼 모듈
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def login(driver, username, password):
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    driver.find_element(By.NAME, "loginId").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Login']"))
    ).click()
