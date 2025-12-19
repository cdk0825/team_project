import pytest
from src.utils.logger import get_logger 
from src.ChatAdvancedFunc.ppt.pages.ppt_create_page import PPTCreatePage
from src.utils import login
from src.config import USERNAME1, PASSWORD1

# 로깅 설정
logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T41", "F1HEL_T158")
@pytest.mark.parametrize("instruction, expect_error, expect_enabled", [
    ("", False, True),                 # 미입력 → 버튼 활성
    ("간단한 지시사항", False, True),   # 정상 입력 → 버튼 활성
    ("a" * 2001, True, False),          # 2000자 초과 → 버튼 비활성
])
def test_instruction_input_validation(driver, instruction, expect_error, expect_enabled):
    """
    지시사항 입력 필드 유효성 검증
    - 지시사항은 필수 입력값이 아님
    - 2000자 초과 시 오류 메시지 노출 + 버튼 비활성화
    """

    logger.info("\n==============================")
    logger.info("[TEST START] Instruction Input Validation")

    login(driver, USERNAME1, PASSWORD1)
    logger.info("[STEP] 관리자 로그인 완료")

    ppt_page = PPTCreatePage(driver)

    ppt_page.click_tool_tab()
    logger.info("[STEP] 도구 탭 클릭")

    ppt_page.click_ppt_tab()
    logger.info("[STEP] PPT 생성 탭 클릭")

    ppt_page.clear_inputs()
    logger.info("[STEP] 입력값 초기화")
    
    ppt_page.enter_topic("지시사항 테스트용 주제")

    ppt_page.enter_instruction(instruction)
    logger.info("[STEP] 지시사항 입력 완료")

    error_text = ppt_page.get_instruction_error_text()
    logger.info(f"[RESULT] error_text: {error_text}")
    
    is_enabled = ppt_page.is_create_button_enabled()
    logger.info(f"[RESULT] 생성 버튼 활성화 상태: {is_enabled}")

    if expect_error:
        assert error_text == "2000자 이하로 입력해주세요.", (
            f"[ASSERT FAIL] Expected error but got: {error_text}"
        )
        logger.info("[ASSERT PASS] 오류 메시지 정상 노출")
    else:
        assert error_text is None, (
            f"[ASSERT FAIL] Expected no error but got: {error_text}"
        )
        logger.info("[ASSERT PASS] 오류 메시지 미노출 정상")
    assert is_enabled is expect_enabled, (
        f"버튼 상태 불일치: expect={expect_enabled}, actual={is_enabled}"
    )

    logger.info("[TEST END] Instruction Input Validation")
    logger.info("==============================\n")
