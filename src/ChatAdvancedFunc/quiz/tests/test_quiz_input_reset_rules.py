import pytest
from src.utils.logger import get_logger 
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from src.ChatAdvancedFunc.quiz.pages.quiz_create_page import QUIZCreatePage

logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T161")
@pytest.mark.xfail(reason="QUIZ 생성 화면 진입 시 입력값 자동 초기화 미구현")
def test_input_reset_rules(driver):
    """
    입력값 초기화 검증
    - QUIZ 생성 화면 재진입 시
      이전에 입력한 값(유형/난이도/주제)이 자동으로 초기화되어야 함
    - 현재는 초기화되지 않아 xfail로 관리
    """

    logger.info("\n==============================")
    logger.info("[TEST START] QUIZ Input Reset Rules Validation")

    login(driver, USERNAME1, PASSWORD1)
    logger.info("[STEP] 관리자 로그인 완료")

    quiz_page = QUIZCreatePage(driver)

    quiz_page.click_tool_tab()
    assert "/tools" in driver.current_url
    
    logger.info("[STEP] QUIZ 생성 탭 클릭")
    quiz_page.click_quiz_tab()
    
    logger.info("[STEP] 입력값 초기화")
    quiz_page.clear_inputs()
    
    logger.info("[STEP] 유형 선택")
    quiz_page.select_option_type()

    logger.info("[STEP] 유형 선택: 객관식(단일)")
    quiz_page.select_option_type_single()

    logger.info("[STEP] 난이도 선택")
    quiz_page.select_difficulty()
    
    logger.info("[STEP] 난이도 선택: 중")
    quiz_page.select_difficulty_middle()

    logger.info("[STEP] 주제 입력")
    quiz_page.enter_topic("운영체제의 기본 개념")

    logger.info("[ASSERT] 생성 버튼 활성화 확인")
    assert quiz_page.is_create_button_enabled() is True
    logger.info("[ASSERT PASS] 생성 버튼 활성화")

    logger.info("[STEP] 생성 버튼 클릭")
    quiz_page.click_create()

    logger.info("[STEP] 다시 생성 버튼 클릭")
    quiz_page.click_regenerate()

    logger.info("[WAIT] QUIZ 생성 완료 대기 (STOP 아이콘 사라질 때까지)")
    quiz_page.wait_generation_complete()

    logger.info("[ASSERT] 생성 완료 메시지 확인")
    assert quiz_page.wait_success_message().is_displayed()

    # 다시 QUIZ 생성 화면 진입
    logger.info("[STEP] 새 대화 진입")
    quiz_page.click_newchat_tab()
    
    logger.info("[STEP] QUIZ 생성 탭 재진입")
    quiz_page.click_tool_tab()
    quiz_page.click_quiz_tab()

    # 입력값 초기화 여부 확인
    option_value = quiz_page.get_option_value()
    difficulty_value = quiz_page.get_difficulty_value()
    topic_value = quiz_page.get_topic_value()
    
    logger.info(f"[RESULT] option_value: '{option_value}'")
    logger.info(f"[RESULT] difficulty_value: '{difficulty_value}'")
    logger.info(f"[RESULT] topic_value: '{topic_value}'")

    logger.info("[EXPECT] 모든 입력값이 초기화되어 있어야 함")
    assert option_value == "", "유형 입력값이 초기화되지 않음"
    assert difficulty_value == "", "난이도 입력값이 초기화되지 않음"
    assert topic_value == "", "주제 입력값이 초기화되지 않음"

    logger.info("[ASSERT PASS] 입력값 자동 초기화 확인")

    logger.info("[TEST END] QUIZ Input Reset Rules Validation")
    logger.info("==============================\n")
