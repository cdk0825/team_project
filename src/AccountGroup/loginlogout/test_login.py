# loginlogout/login.py
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from src.utils import login


def test_login_admin_success(driver):
    login(driver, "qa3team01@elicer.com", "20qareset25elice!")
    # 로그인 완료 검증
    driver.find_element(By.CSS_SELECTOR, '.MuiAvatar-root').click()
    welcome_id = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/ul/div/div[1]/button/div/div/div[2]/div/p').text
    welcome_email = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/ul/div/div[1]/button/div/div/div[2]/p').text
    print("ID:", welcome_id)
    print("Email:", welcome_email)

    assert "team01" in welcome_id  # 환영 메시지가 포함되어 있는지 검증
    assert "qa3team01@elicer.com" in welcome_email  # 환영 메시지가 포함되어 있는지 검증