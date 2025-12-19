import pytest
import json
import os
from src.utils.logger import get_logger
from src.utils import go_to_join
from src.pages.joinlogin_page import JoinLoginPage
from pathlib import Path


# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===

# json 파일 테스트 데이터로 활용
base_dir = os.path.dirname(__file__)  # 현재 test_join.py 위치
json_path = Path(__file__).resolve().parents[2] / "data" / "join_data.json"
with open(json_path, "r", encoding="utf-8") as f:
    join_data_list = json.load(f)

# ===== 회원가입 테스트 =====
'''
[관련 TC]
F1HEL_T1 : 회원가입 성공
F1HEL_T17 : 회원가입 실패(잘못된 Email 입력)
F1HEL_T22 : 회원가입 실패(잘못된 Password 입력)
F1HEL_T24 : 회원가입 실패(잘못된 Name 입력_공백)
F1HEL_T28 : 회원가입 실패(이미 있는 계정으로 시도)
F1HEL_T119 : 회원가입 실패(500자 이상 이름 입력)
'''
@pytest.mark.parametrize("data", join_data_list)
#해당 테스트 함수에 다양한 입력값 제공하여 여러번 실행될 수 있도록함.
def test_join_cases(driver,data):
    page = JoinLoginPage(driver)
    logger.info(f"테스트 시작: {data['loginId']}")

    driver.get("https://qaproject.elice.io/ai-helpy-chat")


    page.get_create_btn().click() # 첫번째 create account 클릭
    page.click_create_account_with_email() # 두번째 create accocut with email 클릭
    logger.info("==회원가입 페이지 접속==")

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

        # 입력값 인증 피드백 메세지가 발생한 경우 캐치하기 위한 변수 설정
        em_msg = driver.execute_script("return arguments[0].validationMessage;", loginId)
        pw_msg = driver.execute_script("return arguments[0].validationMessage;", loginPw)
        nm_msg = driver.execute_script("return arguments[0].validationMessage;", loginNM)

        # 유효한 형식으로 회원가입한 경우
        if data["expected_result"] == 'success':

            # 프로필에서 이름과 email 추출하여 확인
            page.profile_click()
            welcome_id = page.get_welcome_name()
            welcome_email = page.get_welcome_email()
            logger.info(f"로그인 프로필 확인: ID={welcome_id}, Email={welcome_email}")

            assert data["name"] in welcome_id  # 환영 메시지가 포함되어 있는지 검증
            assert data["loginId"] in welcome_email  # 환영 메시지가 포함되어 있는지 검증
        
        # 잘못된 형식으로 회원가입 시도한 경우
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

# ===== 회원가입 약관 동의 여부에 따른 회원가입 기능 테스트 =====
'''
[관련 TC]
F1HEL_T27 : 전체 미동의 실패 테스트
F1HEL_T238 : 필수항목만 동의 후 회원가입 테스트
F1HEL_T239 : 선택약관만 동의 후 회원가입 테스트
'''
@pytest.mark.parametrize("agree_type", ["none","optional","required"])
def test_join_agree(driver, agree_type):
    go_to_join(driver)
    page = JoinLoginPage(driver)
    
    # 약관 위주 테스트로 테스트 계정 하드코딩 처리
    page.set_login_id("tester.zu.digimon+f100@gmail.com")
    page.set_password("team01cheerup!")
    page.set_name("박동의")

    create_btn = page.get_create_btn_2()

    if agree_type == 'none':
        logger.info("전체 미동의 상태")
        assert not create_btn.is_enabled(), "Fail:전체 미동의인데 버튼이 활성화 됨."
    elif agree_type == 'optional':
        logger.info("선택 약관만 동의 상태")
        for i in [1, 4]:
            page.click_chkbox(i)
        assert not create_btn.is_enabled(), "Fail:옵션만 동의인데 버튼이 활성화 됨."       
    elif agree_type == 'required':
        logger.info("필수 약관만 동의 상태")
        for i in [2, 3]:
            page.click_chkbox(i)
        assert create_btn.is_enabled(), "Fail:필수약관 다 동의했는데 버튼이 비활성화 됨."