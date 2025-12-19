import pytest
from src.utils import login
from src.utils.logger import get_logger 
from src.config import USERNAME4, PASSWORD4
from src.ChatAdvancedFunc.deep.pages.deep_create_page import DEEPCreatePage

logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T127", "F1HEL_T128") 
@pytest.mark.parametrize(
    "topic_input, expect_error",
    [
        ("", False),         # 미입력
        ("a" * 501, True),      # 500자 초과
    ]
)
def test_deep_topic_input_validation(driver, topic_input, expect_error):
    """
    DEEP 주제 입력값 검증
    1. 미입력 → 생성 버튼 비활성화(필수입력값)
    2. 500자 초과 입력 → 생성 버튼 비활성화 + 에러 메시지 표시
    """

    logger.info("\n==============================")
    logger.info("[TEST START] DEEP Topic Input Validation")

    login(driver, USERNAME4, PASSWORD4)
    logger.info("[STEP] 로그인 완료")

    deep_page = DEEPCreatePage(driver)

    deep_page.click_tool_tab()
    logger.info("[STEP] 도구 탭 클릭")

    deep_page.click_deep_tab()
    logger.info("[STEP] 심층 조사 탭 클릭")

    deep_page.clear_inputs()
    logger.info("[STEP] 입력값 초기화")

    if topic_input:
        deep_page.enter_topic(topic_input)
    logger.info(f"[STEP] 주제 입력값 길이: {len(topic_input)}")
    
    deep_page.blur_topic()

    is_enabled = deep_page.is_create_button_enabled()
    logger.info(f"[RESULT] 생성 버튼 활성화 상태: {is_enabled}")
    assert is_enabled is False, "생성 버튼이 활성화됨 (입력값 검증 실패)"
    
    if expect_error:
        error_text = deep_page.get_topic_error_text()
        logger.info(f"[RESULT] 주제 에러 메시지: {error_text}")
        assert error_text == "1자 이상 500자 이하로 입력해주세요.", \
            "주제 길이 초과 시 에러 메시지가 표시되지 않음"

    logger.info("[TEST END] DEEP Topic Input Validation")
    logger.info("==============================\n")
