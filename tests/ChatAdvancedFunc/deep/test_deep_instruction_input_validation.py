import pytest
from src.utils import login
from src.utils.logger import get_logger 
from data.config import USERNAME4, PASSWORD4
from src.pages.deep_create_page import DEEPCreatePage

logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T127", "F1HEL_T129") 
@pytest.mark.parametrize(
    "instruction_input, expect_enabled, expect_error",
    [
        ("", True, False),          # 미입력 → 활성화(필수값 아님)
        ("정상 지시사항 입력", True, False),  # 정상 입력 → 버튼 활성화
        ("a" * 2001, False, True),      # 2000자 초과 → 버튼 비활성화 + 에러
    ]
)
def test_deep_instruction_input_validation(
    driver, instruction_input, expect_enabled, expect_error
):
    """
    DEEP 지시사항 입력값 검증
    1. 지시사항은 필수 아님
       - 미입력 → 버튼 비활성화
       - 정상 입력 → 버튼 활성화
    2. 2000자 초과 입력 시
       - 버튼 비활성화
       - '2000자 이하로 입력해주세요.' 에러 메시지 표시
    """

    logger.info("\n==============================")
    logger.info("[TEST START] DEEP Instruction Input Validation")
    
    try:
        login(driver, USERNAME4, PASSWORD4)
        logger.info("[STEP] 로그인 완료")

        deep_page = DEEPCreatePage(driver)

        deep_page.click_tool_tab()
        deep_page.click_deep_tab()
        logger.info("[STEP] 심층 조사 화면 진입")

        deep_page.clear_inputs()
        logger.info("[STEP] 입력값 초기화")

        # 필수 입력값: 주제
        deep_page.enter_topic("AI 모델 성능 비교")
        deep_page.blur_topic()
        logger.info("[STEP] 주제 입력 완료")

        deep_page.enter_instruction(instruction_input)
        deep_page.blur_instruction()
        logger.info(f"[STEP] 지시사항 입력값 길이: {len(instruction_input)}")

        is_enabled = deep_page.is_create_button_enabled()
        logger.info(f"[RESULT] 생성 버튼 활성화 여부: {is_enabled}")
        
        if is_enabled is not expect_enabled:
            logger.error(
                f"[ASSERT FAIL] 생성 버튼 상태 불일치 "
                f"(expect={expect_enabled}, actual={is_enabled})"
            )
        assert is_enabled is expect_enabled

        if expect_error:
            error_text = deep_page.get_instruction_error_text()
            logger.info(f"[RESULT] 지시사항 에러 메시지: {error_text}")
            
            if error_text != "2000자 이하로 입력해주세요.":
                logger.error(
                    "[ASSERT FAIL] 지시사항 길이 초과 에러 메시지 불일치"
                )
            assert error_text == "2000자 이하로 입력해주세요."
            
        logger.info("[ASSERT PASS] 지시사항 입력값 검증 완료")

    except Exception:
        logger.exception("[TEST ERROR] 테스트 중 예외 발생")
        raise
    
    finally:
        logger.info("[TEST END] DEEP Instruction Input Validation")
        logger.info("==============================\n")
