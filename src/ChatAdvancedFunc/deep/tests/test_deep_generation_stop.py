import pytest
from src.utils.logger import get_logger 
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from src.ChatAdvancedFunc.deep.pages.deep_create_page import DEEPCreatePage

logger = get_logger(__file__)

def test_deep_generation_stop(driver):
    """
    심층 조사 중지 기능 테스트
    - 주제 / 지시사항 입력
    - 생성 → 다시 생성
    - STOP 아이콘 클릭
    - 중지 안내 멘트 노출 확인
    """

    logger.info("\n==============================")
    logger.info("[TEST START] DEEP Generation Stop")

    login(driver, USERNAME1, PASSWORD1)
    logger.info("[STEP] 관리자 로그인 완료")
    
    deep_page = DEEPCreatePage(driver)

    deep_page.click_tool_tab()
    logger.info("[STEP] 도구 탭 클릭")

    deep_page.click_deep_tab()
    logger.info("[STEP] 심층 조사 탭 클릭")

    deep_page.clear_inputs()
    logger.info("[STEP] 주제 / 지시사항 입력값 초기화")

    deep_page.enter_topic("AI 모델의 성능 비교")
    logger.info("[STEP] 주제 입력 완료")

    deep_page.enter_instruction(
        "최신 GPT, Gemini 모델의 차이를 표로 정리하라. "
        "참고한 근거를 단계별로 제시하라."
    )
    logger.info("[STEP] 지시사항 입력 완료")

    is_enabled = deep_page.is_create_button_enabled()
    logger.info(f"[ASSERT] 생성 버튼 활성화 여부: {is_enabled}")
    assert is_enabled is True, "생성 버튼이 활성화되지 않음"

    deep_page.click_create()
    logger.info("[STEP] 생성 버튼 클릭")

    deep_page.click_regenerate()
    logger.info("[STEP] 다시 생성 버튼 클릭")

    deep_page.click_stop_icon()
    logger.info("[STEP] 생성 중지(STOP) 클릭")

    stop_message = deep_page.get_stop_message_text()
    logger.info(f"[RESULT] 중지 멘트: {stop_message}")

    assert stop_message is not None
    assert "요청에 의해 답변 생성을 중지했습니다." in stop_message

    logger.info("[ASSERT PASS] 중지 안내 멘트 정상 노출")
    logger.info("[TEST END] DEEP Generation Stop")
    logger.info("==============================\n")
