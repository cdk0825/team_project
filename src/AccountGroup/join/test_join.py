from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import pytest
import json
import os
import logging
from src.utils import go_to_join

#로깅설정하기
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

base_dir = os.path.dirname(__file__)  # 현재 test_join.py 위치
json_path = os.path.join(base_dir, "join_data.json")
with open(json_path, "r", encoding="utf-8") as f:
    join_data_list = json.load(f)

@pytest.mark.parametrize("data", join_data_list)
#해당 테스트 함수에 다양한 입력값 제공하여 여러번 실행될 수 있도록함.
def test_join_cases(driver,data):
    logger.info(f"테스트 시작: {data['loginId']} / 기대결과: {data['expected_result']}")

    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    driver.delete_all_cookies()
    driver.find_element(By.LINK_TEXT, "Create account").click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Create account with email']"))
    ).click()
    try:
        loginId = driver.find_element(By.NAME, "loginId")
        loginPw = driver.find_element(By.NAME, "password")
        loginNM = driver.find_element(By.NAME, "fullname")
        loginId.send_keys(data["loginId"])
        loginPw.send_keys(data["password"])
        loginNM.send_keys(data["name"])
        logger.info("회원가입 폼 입력 완료")

        agreechk = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][data-indeterminate="false"]')
        agreechk.click()
        logger.info("약관 동의 체크 완료")

        driver.find_element(By.XPATH, "//button[contains(text(),'Create account')]").click()
        logger.info("Create account 버튼 클릭")

        em_msg = driver.execute_script("return arguments[0].validationMessage;", loginId)
        pw_msg = driver.execute_script("return arguments[0].validationMessage;", loginPw)
        nm_msg = driver.execute_script("return arguments[0].validationMessage;", loginNM)

        if data["expected_result"] == 'success':
            driver.find_element(By.CSS_SELECTOR, '.MuiAvatar-root').click()
            welcome_id = driver.find_element(By.CSS_SELECTOR, "p.css-if9dpr").text
            welcome_email = driver.find_element(By.CSS_SELECTOR, "p.css-14lgytj").text
            logger.info(f"로그인 프로필 확인: ID={welcome_id}, Email={welcome_email}")

            assert data["name"] in welcome_id  # 환영 메시지가 포함되어 있는지 검증
            assert data["loginId"] in welcome_email  # 환영 메시지가 포함되어 있는지 검증
        
        else:
            if data["expected_result"] == 'failure_email':
                logger.warning(f"Validation Message(Email): {em_msg}")
            elif data["expected_result"] == 'failure_already':
                logger.warning(f"Validation Message(Email): {em_msg}")
            elif data["expected_result"] == 'failure_pw':
                logger.warning(f"Validation Message(Password): {pw_msg}")
            elif data["expected_result"] == 'failure_name_empty':
                logger.warning(f"Validation Message(Name): {nm_msg}")
            elif data["expected_result"] == 'failure_name_over':
                logger.warning(f"Validation Message(Name): {nm_msg}")
            assert data["expected_msg"] in driver.page_source
            logger.info(f"실패 케이스 검증 완료: {data['expected_msg']}")

    except Exception as error:
        # 실패 메시지와 함께 테스트를 즉시 실패 처리
        logger.error(f"테스트 중 오류 발생: {error}")
        pytest.fail(f"테스트 중 오류 발생하여 테스트 실패: {error}")
        
@pytest.mark.parametrize("agree_type", ["none","optional","required"])
def test_join_agree(driver, agree_type):
    go_to_join(driver)
    driver.find_element(By.NAME, "loginId").send_keys("tester.zu.digimon+f100@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("team01cheerup!")
    driver.find_element(By.NAME, "fullname").send_keys("박동의")

    checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"].PrivateSwitchBase-input')
    create_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Create account')]")

    if agree_type == 'none':
        assert not create_btn.is_enabled(), "PASS 버튼이 비활성화 상태입니다.회원가입이 불가합니다."
    elif agree_type == 'optional':
            
            for i in [1, 4]:
                if not checkboxes[i].is_selected():
                    checkboxes[i].click()
    elif agree_type == 'required':
            for i in [2, 3]:
                if not checkboxes[i].is_selected():
                    checkboxes[i].click()

    if agree_type == 'none':
        assert not create_btn.is_enabled(), "Fail:전체 미동의인데 버튼이 활성화 됨."
    elif agree_type=='optional':
        assert not create_btn.is_enabled(), "Fail:옵션만 동의인데 버튼이 활성화 됨."
    elif agree_type=='required':
        assert create_btn.is_enabled(), "Fail:필수약관 다 동의했는데 버튼이 비활성화 됨."