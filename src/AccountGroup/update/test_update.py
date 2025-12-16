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
        page.send_code().click()
        assert data["expected_msg"] in driver.page_source

    ## 인증 횟수때메 일단 보류 
    elif data['category']=='wrong_code':
        page.send_code().click()
        driver.find_element(By.NAME, "code").send_keys('000000')
        page.ok_btn().click()
        assert data["expected_msg"] in driver.page_source

    elif data['category']=='wrong_form':
        #page.ok_btn().click()
        assert data["expected_msg"] in driver.page_source
