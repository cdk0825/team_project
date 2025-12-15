# loginlogout/login.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from src.utils import login
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
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    driver.delete_all_cookies()

    try:
        loginId = driver.find_element(By.NAME, "loginId")
        loginPw = driver.find_element(By.NAME, "password")
        loginId.send_keys(data["loginId"])
        loginPw.send_keys(data["password"])
        logger.info("로그인 폼 입력 완료")

        em_msg = driver.execute_script("return arguments[0].validationMessage;", loginId)
        pw_msg = driver.execute_script("return arguments[0].validationMessage;", loginPw)

        driver.find_element(By.XPATH, "//button[normalize-space(text())='Login']").click()

        if data["expected_result"] == 'success':
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.MuiAvatar-root'))
            ).click()
            #driver.find_element(By.CSS_SELECTOR, '.MuiAvatar-root').click()
            welcome_id = driver.find_element(By.CSS_SELECTOR, "p.css-if9dpr").text
            welcome_email = driver.find_element(By.CSS_SELECTOR, "p.css-14lgytj").text

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