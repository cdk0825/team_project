# loginlogout/login.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from src.utils import login
from src.pages.joinlogin_page import JoinPage
from src.config import USERNAME, PASSWORD 
import os
import json
import pytest
import logging
import time


#로깅설정하기
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

base_dir = os.path.dirname(__file__)  # 현재 test_join.py 위치
json_path = os.path.join(base_dir, "login_data.json")
with open(json_path, "r", encoding="utf-8") as f:
    login_data_list = json.load(f)

@pytest.mark.parametrize("data", login_data_list)
def test_login_cases(driver, data):
    page = JoinPage(driver)
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    driver.delete_all_cookies()

    try:
        loginId = page.get_login_id()
        loginPw = page.get_password()
        page.set_login_id(data["loginId"])
        page.set_password(data["password"])
        logger.info("로그인 폼 입력 완료")

        em_msg = driver.execute_script("return arguments[0].validationMessage;", loginId)
        pw_msg = driver.execute_script("return arguments[0].validationMessage;", loginPw)

        page.login_btn_click()

        if data["expected_result"] == 'success':
            page.profile_click()
            welcome_id = page.get_welcome_name()
            welcome_email = page.get_welcome_email()

            assert data["name"] in welcome_id  # 환영 메시지가 포함되어 있는지 검증
            assert data["loginId"] in welcome_email  # 환영 메시지가 포함되어 있는지 검증
        else:
            if data["expected_result"] == 'failure_notmatch':
                time.sleep(3)
                assert data["expected_msg"] in driver.page_source
            elif data["expected_result"] == 'failure_empty_em':
                logger.warning(f"Validation Message(Email): {em_msg}")
                assert data["expected_msg"] in driver.page_source
            elif data["expected_result"] == 'failure_empty_pw':
                logger.warning(f"Validation Message(Password): {pw_msg}")
                assert data["expected_msg"] in driver.page_source
            elif data["expected_result"] == 'failure_em':
                logger.warning(f"Validation Message(Email): {em_msg}")
                assert data["expected_msg"] in driver.page_source
    except Exception as error:
        #실패 메시지와 함께 테스트를 즉시 실패 처리
        logger.error(f"테스트 중 오류 발생: {error}")
        pytest.fail(f"테스트 중 오류 발생하여 테스트 실패: {error}")