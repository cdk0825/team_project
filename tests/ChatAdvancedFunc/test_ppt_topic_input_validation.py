import pytest
from src.utils.logger import get_logger 
from src.pages.ppt_create_page import PPTCreatePage
from src.utils import login
from data.config import USERNAME1, PASSWORD1

# 로깅 설정
logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T41", "F1HEL_T76")
@pytest.mark.parametrize("topic, expect_error, expect_enabled", [
    ("", True, False),              # 미입력
    ("A", False, True),             # 최소값
    ("Valid Topic", False, True),   # 정상
    ("a" * 501, True, False),      # 500자 초과
])
def test_topic_input_validation(driver, topic, expect_error, expect_enabled):
    """
    주제 입력 필드 유효성 검증
    - 미입력, 최소값 1자, 정상값, 500자 초과 값 테스트
    - 오류 메시지 발생 여부 확인
    """
    
    logger.info("\n==============================")
    logger.info("[TEST START] Topic Input Validation")

    login(driver, USERNAME1, PASSWORD1)
    logger.info("[STEP] 관리자 로그인 완료")

    ppt_page = PPTCreatePage(driver)

    ppt_page.click_tool_tab()
    ppt_page.click_ppt_tab()
    logger.info("[STEP] PPT 생성 화면 진입")

    ppt_page.clear_inputs()
    logger.info("[STEP] 입력값 초기화")

    ppt_page.enter_topic(topic)
    logger.info(f"[STEP] 주제 입력값 길이: {len(topic)}")

    error_text = ppt_page.get_topic_error_text()
    logger.info(f"[RESULT] error_text: {error_text}")
    
    is_enabled = ppt_page.is_create_button_enabled()
    logger.info(f"[RESULT] 생성 버튼 활성화 상태: {is_enabled}")

    # 오류 메시지 검증
    if expect_error:
        if error_text != "1자 이상 500자 이하로 입력해주세요.":
            logger.error(
                "[ERROR] 주제 오류 메시지 불일치 "
                f"(topic_length={len(topic)}, error_text={error_text})"
            )

        assert error_text == "1자 이상 500자 이하로 입력해주세요.", \
            f"오류 메시지 불일치: {error_text}"

        logger.info("[ASSERT PASS] 오류 메시지 정상 노출")

    else:
        if error_text is not None:
            logger.error(
                "[ERROR] 오류 메시지가 노출되면 안 되는 케이스에서 노출됨 "
                f"(topic_length={len(topic)}, error_text={error_text})"
            )

        assert error_text is None, \
            f"불필요한 오류 메시지 노출: {error_text}"

        logger.info("[ASSERT PASS] 오류 메시지 미노출 정상")

    # 생성 버튼 상태 검증
    if is_enabled is not expect_enabled:
        logger.error(
            "[ERROR] 생성 버튼 상태 불일치 "
            f"(topic_length={len(topic)}, "
            f"expect_enabled={expect_enabled}, actual={is_enabled})"
        )

    assert is_enabled is expect_enabled, \
        f"생성 버튼 상태 불일치: expect={expect_enabled}, actual={is_enabled}"

    logger.info("[ASSERT PASS] 생성 버튼 상태 검증 완료")
    logger.info("[TEST END] Topic Input Validation")
    logger.info("==============================\n")