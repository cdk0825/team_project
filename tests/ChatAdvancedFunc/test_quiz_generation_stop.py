import pytest
from src.utils.logger import get_logger 
from src.utils import login
from data.config import USERNAME1, PASSWORD1
from src.pages.quiz_create_page import QUIZCreatePage

logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T144")
def test_quiz_generation_stop(driver):
    """
    QUIZ 생성 중지 기능 테스트
    - 유형/난이도 선택
    - 주제 입력
    - 생성 → 다시 생성
    - STOP 아이콘 클릭
    - 중지 안내 멘트 노출 확인
    """

    logger.info("\n==============================")
    logger.info("[TEST START] QUIZ Generation Stop")

    login(driver, USERNAME1, PASSWORD1)
    logger.info("[STEP] 관리자 로그인 완료")

    quiz_page = QUIZCreatePage(driver)
    
    quiz_page.click_tool_tab()
    quiz_page.click_quiz_tab()
    logger.info("[STEP] QUIZ 생성 화면 진입")
    
    quiz_page.clear_inputs()
    logger.info("[STEP] 입력값 초기화")
    
    quiz_page.select_option_type()
    quiz_page.select_option_type_single()
    logger.info("[STEP] 유형 선택: 객관식(단일)")

    quiz_page.select_difficulty()    
    quiz_page.select_difficulty_middle()
    logger.info("[STEP] 난이도 선택: 중")

    quiz_page.enter_topic("운영체제의 기본 개념")
    logger.info("[STEP] 주제 입력")

    logger.info("[ASSERT] 생성 버튼 활성화 확인")
    assert quiz_page.is_create_button_enabled() is True
    logger.info("[ASSERT PASS] 생성 버튼 활성화")

    quiz_page.click_create()
    quiz_page.click_regenerate()
    logger.info("[STEP] 생성->다시 생성 클릭")

    quiz_page.click_stop_icon()
    logger.info("[STEP] 생성 중지(STOP) 클릭")

    stop_message = quiz_page.get_stop_message_text()
    logger.info(f"[RESULT] 중지 멘트: {stop_message}")

    logger.info("[ASSERT] 중지 안내 멘트 존재 확인")
    if stop_message is None:
        logger.error("[ASSERT FAIL] 중지 안내 멘트 미노출")
    assert stop_message is not None
    logger.info("[ASSERT PASS] 중지 안내 멘트 노출 확인")

    logger.info("[ASSERT] 중지 안내 멘트 내용 확인")
    if "요청에 의해 답변 생성을 중지했습니다." not in stop_message:
        logger.error(f"[ASSERT FAIL] 중지 멘트 불일치: {stop_message}")
    assert "요청에 의해 답변 생성을 중지했습니다." in stop_message

    logger.info("[ASSERT PASS] 중지 안내 멘트 정상 노출")
    logger.info("[TEST END] QUIZ Generation Stop")
    logger.info("==============================\n")
