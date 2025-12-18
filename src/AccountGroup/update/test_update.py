from selenium.webdriver.support import expected_conditions as EC
import logging
from src.pages.update_page import UpdatePage
from src.utils import login
from src.config import USERNAME5, PASSWORD5
import pytest
import os
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


#로깅설정하기
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

base_dir = os.path.dirname(__file__)  # 현재 test_join.py 위치
json_path = os.path.join(base_dir, "update_data.json")
with open(json_path, "r", encoding="utf-8") as f:
    update_data = json.load(f)

@pytest.mark.parametrize("data", update_data["name_tests"])
def test_update_name(driver,data):
    wait = WebDriverWait(driver, 10)
    page = UpdatePage(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.go_to_setting()

    update_name = page.update_name(data['name'])

    if data['category']=='success':
        page.ok_btn().click()
        wait.until(EC.text_to_be_present_in_element(
        (By.XPATH, "//h6[contains(@class,'MuiTypography-subtitle2')]"),data['name']))
        assert update_name == data['name']

    elif data['category']=='none':
        assert not page.ok_btn().is_enabled(), "Fail: 완료 버튼이 활성화 됨."

    elif data['category']=='over':
        page.ok_btn().click()
        element = wait.until(
        EC.visibility_of_element_located((By.ID, "notistack-snackbar")))
        assert element.is_displayed(), "Fail: notistack div가 보이지 않음"


@pytest.mark.parametrize("data", update_data["email_tests"])
def test_update_email(driver,data):
    page = UpdatePage(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.go_to_setting()
    page.update_email(data['email'])
    if data['category']=='already':
        page.btn_send_code().click()
        print(page.error_mag())
        assert data["expected_msg"] == page.error_mag()
    ##### 인증 횟수때메 일단 보류 
    elif data['category']=='wrong_code':
        page.btn_send_code().click()
        page.wait_and_send_input_code()
        page.ok_btn().click()
        print(page.error_mag())
        assert data["expected_msg"] == page.error_mag()
    elif data['category']=='wrong_form':
        #page.ok_btn().click()
        print(page.error_mag())
        assert data["expected_msg"] == page.error_mag()

@pytest.mark.parametrize("data", update_data["phone_tests"])
def test_update_phone(driver,data):
    page = UpdatePage(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.go_to_setting()
    page.update_phone(data['num'])
    
    if data['category']=='short':
        assert data["expected_msg"] == page.error_mag()
    elif data['category']=='over':
        value = page.phone_input().get_attribute("value")
        print(value)
        assert data["expected_result"] == value
    elif data['category']=='none':
        assert not page.btn_send_code_phone().is_enabled(), "Fail: 완료 버튼이 활성화 됨."
        assert not page.ok_btn().is_enabled(), "Fail: 완료 버튼이 활성화 됨."

@pytest.mark.parametrize("data", update_data["password_tests"])
def test_update_password(driver,data):
    wait = WebDriverWait(driver, 10)
    page = UpdatePage(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.go_to_setting()
    page.update_password(data['pw'], data['new_pw'])
    
    if data['category']=='wrong_form':    
        assert data["expected_msg"] == page.error_new_password()
    elif data['category']=='already':
        page.ok_btn().click()
        assert data["expected_msg"] == page.error_now_password()
    elif data['category']=='wrong_pw':
        page.ok_btn().click()
        assert data["expected_msg"] == page.error_now_password()
    elif data['category']=='success':
        page.ok_btn().click()
        element = wait.until(
        EC.visibility_of_element_located((By.ID, "notistack-snackbar")))
        # page.update_env(data["new_pw"])
        assert element.is_displayed(), "Fail: 변경완료 notistack div가 보이지 않음"