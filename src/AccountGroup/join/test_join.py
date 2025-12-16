from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import pytest
import json
import os
import logging
from src.utils import go_to_join
from src.pages.joinlogin_page import JoinPage


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
    page = JoinPage(driver)
    logger.info(f"테스트 시작: {data['loginId']} / 기대결과: {data['expected_result']}")

    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    driver.delete_all_cookies()

    page.get_create_btn().click()
    page.click_create_account_with_email()

    try:
        loginId = page.get_login_id()
        loginPw = page.get_password()
        loginNM = page.get_name()
        page.set_login_id(data["loginId"])
        page.set_password(data["password"])
        page.set_name(data["name"])

        logger.info("회원가입 폼 입력 완료")

        agreechk = page.get_all_agr_chkboxes()
        agreechk.click()
        logger.info("약관 동의 체크 완료")

        page.get_create_btn_2().click()
        logger.info("Create account 버튼 클릭")

        em_msg = driver.execute_script("return arguments[0].validationMessage;", loginId)
        pw_msg = driver.execute_script("return arguments[0].validationMessage;", loginPw)
        nm_msg = driver.execute_script("return arguments[0].validationMessage;", loginNM)

        if data["expected_result"] == 'success':
            page.profile_click()
            
            welcome_id = page.get_welcome_name()
            welcome_email = page.get_welcome_email()
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
        logger.error(f"에러발생: {error}")
        pytest.fail(f"테스트 에러 발생하여 테스트 실패: {error}")
        
@pytest.mark.parametrize("agree_type", ["none","optional","required"])
def test_join_agree(driver, agree_type):
    go_to_join(driver)
    page = JoinPage(driver)
    page.set_login_id("tester.zu.digimon+f100@gmail.com")
    page.set_password("team01cheerup!")
    page.set_name("박동의")

    create_btn = page.get_create_btn_2()

    if agree_type == 'none':
        assert not create_btn.is_enabled(), "PASS 버튼이 비활성화 상태입니다.회원가입이 불가합니다."
    elif agree_type == 'optional':
            for i in [1, 4]:
                page.click_chkbox(i)
    elif agree_type == 'required':
            for i in [2, 3]:
                page.click_chkbox(i)

    if agree_type == 'none':
        assert not create_btn.is_enabled(), "Fail:전체 미동의인데 버튼이 활성화 됨."
    elif agree_type=='optional':
        assert not create_btn.is_enabled(), "Fail:옵션만 동의인데 버튼이 활성화 됨."
    elif agree_type=='required':
        assert create_btn.is_enabled(), "Fail:필수약관 다 동의했는데 버튼이 비활성화 됨."