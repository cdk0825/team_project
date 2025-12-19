# loginlogout/login.py
from src.utils import login
from src.pages.joinlogin_page import JoinLoginPage
from data.config import USERNAME, PASSWORD 
import os
import json
import pytest
import time
from src.utils.logger import get_logger
from pathlib import Path


# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===

base_dir = os.path.dirname(__file__)  # 현재 test_join.py 위치
json_path = Path(__file__).resolve().parents[2] / "data" / "login_data.json"

with open(json_path, "r", encoding="utf-8") as f:
    login_data_list = json.load(f)

# 로그인 테스트
'''
[관련 TC]
F1HEL-T30 : 로그인 성공 및 상태 유지 테스트
F1HEL-T31 : 없는 계정으로 로그인 테스트
F1HEL-T32 : 유효한 계정의 비밀번호 불일치 로그인 테스트
'''
@pytest.mark.parametrize("data", login_data_list)
def test_login_cases(driver, data):
    page = JoinLoginPage(driver)
    driver.get("https://qaproject.elice.io/ai-helpy-chat")

    try:
        loginId = page.get_login_id()
        loginPw = page.get_password()
        page.set_login_id(data["loginId"])
        page.set_password(data["password"])
        logger.info("로그인 폼 입력 완료")

        # 입력값 인증 피드백 메세지가 발생한 경우 캐치하기 위한 변수 설정
        em_msg = driver.execute_script("return arguments[0].validationMessage;", loginId)
        pw_msg = driver.execute_script("return arguments[0].validationMessage;", loginPw)

        page.login_btn_click()

        # 로그인 예상결과가 성공인 경우
        if data["expected_result"] == 'success':
            page.profile_click()
            welcome_id = page.get_welcome_name()
            welcome_email = page.get_welcome_email()
            assert data["name"] in welcome_id  # 환영 메시지가 포함되어 있는지 검증
            assert data["loginId"] in welcome_email  # 환영 메시지가 포함되어 있는지 검증

        else:
            # Email과 password 중 하나가 틀린 경우
            if data["expected_result"] == 'failure_notmatch':
                time.sleep(3)
                assert data["expected_msg"] in driver.page_source
            # Email 공백 로그인 하는 경우
            elif data["expected_result"] == 'failure_empty_em':
                logger.warning(f"Validation Message(Email): {em_msg}")
                assert data["expected_msg"] in driver.page_source
            # Password 공백 로그인인 경우
            elif data["expected_result"] == 'failure_empty_pw':
                logger.warning(f"Validation Message(Password): {pw_msg}")
                assert data["expected_msg"] in driver.page_source
            # 잘못된 Email 형식인 경우
            elif data["expected_result"] == 'failure_em':
                logger.warning(f"Validation Message(Email): {em_msg}")
                assert data["expected_msg"] in driver.page_source

    except Exception as error:
        #실패 메시지와 함께 테스트를 즉시 실패 처리
        logger.error(f"테스트 중 오류 발생: {error}")
        pytest.fail(f"테스트 중 오류 발생하여 테스트 실패: {error}")