import pytest
from src.utils.logger import get_logger 
from src.utils import login
from f1_helpychat.data.config import USERNAME4, PASSWORD4
from f1_helpychat.src.pages.quiz_create_page import QUIZCreatePage

logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T109")
@pytest.mark.parametrize("skip_option, skip_difficulty, skip_topic, expect_topic_error", [
    (True, False, False, False),    # 유형 미선택
    (False, True, False, False),    # 난이도 미선택
    (False, False, True, True),    # 주제 미입력
])
def test_option_difficulty_input_validation(driver, skip_option, skip_difficulty, skip_topic, expect_topic_error):
    """
    QUIZ 생성 필수 입력값 유효성 검증
    - 유형, 난이도, 주제 각각 필수 입력
    - 선택/입력하지 않은 경우 생성 버튼이 비활성화 상태임
    - 주제 미입력 시 '1자 이상 입력해주세요.' 에러 메시지 표시
    """
    logger.info("\n==============================")
    logger.info("[TEST START] Quiz Input Validation")
    
    # 로그인(초기화 기능 이슈로 이전 퀴즈 생성 기록이 없는 계정이어야함)
    login(driver, USERNAME4, PASSWORD4)
    logger.info("[STEP] 로그인 완료")

    quiz_page = QUIZCreatePage(driver)

    quiz_page.click_tool_tab()
    quiz_page.click_quiz_tab()
    logger.info("[STEP] 퀴즈 생성 화면 진입")

    quiz_page.clear_inputs()
    logger.info("[STEP] 입력값 초기화 완료")
    
    if not skip_topic:
        quiz_page.enter_topic("테스트 퀴즈 주제")
        logger.info("[STEP] 주제 입력 완료")
    else:
        logger.info("[STEP] 주제 입력 생략")
        quiz_page.trigger_topic_validation()

    if not skip_option:
        quiz_page.select_option_type()
        quiz_page.select_option_type_single()
        logger.info("[STEP] 유형 선택 완료")
    else:
        logger.info("[STEP] 유형 선택 생략")

    if not skip_difficulty:
        quiz_page.select_difficulty()
        quiz_page.select_difficulty_middle()
        logger.info("[STEP] 난이도 선택 완료")
    else:
        logger.info("[STEP] 난이도 선택 생략")

    is_enabled = quiz_page.is_create_button_enabled()
    logger.info(f"[RESULT] 생성 버튼 활성화 상태: {is_enabled}")
    
    logger.info("[ASSERT] 필수 입력값 누락 시 생성 버튼 비활성화 확인")
    if is_enabled:
        logger.error(
            "[ASSERT FAIL] 필수 입력값 누락 상태에서 생성 버튼이 활성화됨 "
            f"(skip_option={skip_option}, skip_difficulty={skip_difficulty}, skip_topic={skip_topic})"
        )
    assert is_enabled is False
    logger.info("[ASSERT PASS] 생성 버튼 비활성화 정상")
    
    if expect_topic_error:
        topic_error_text = quiz_page.get_topic_error_text()
        logger.info(f"[RESULT] 주제 에러 메시지: {topic_error_text}")
        
        logger.info("[ASSERT] 주제 미입력 에러 메시지 확인")
        if topic_error_text != "1자 이상 입력해주세요.":
            logger.error(
                f"[ASSERT FAIL] 주제 에러 메시지 불일치: {topic_error_text}"
            )
        assert topic_error_text == "1자 이상 입력해주세요."
        logger.info("[ASSERT PASS] 주제 에러 메시지 정상 노출")

    logger.info("[ASSERT PASS] 필수 입력값 유효성 검증 성공")
    logger.info("[TEST END] Quiz Input Validation")
    logger.info("==============================\n")