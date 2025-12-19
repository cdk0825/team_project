import pytest
from src.utils.logger import get_logger 
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from src.ChatAdvancedFunc.quiz.pages.quiz_create_page import QUIZCreatePage

logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T103")
def test_success_create(driver):
    """
    QUIZ 정상 생성 테스트
    - 유형/난이도 선택
    - 주제 입력
    - 생성 → 다시 생성
    - 생성 결과 확인 (문제/학습목표/보기/답/해설)
    """
    
    logger.info("\n==============================")
    logger.info("[TEST START] QUIZ Success Create")
    
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

    logger.info("[ASSERT] 문제 영역 확인")
    assert quiz_page.is_question_displayed()

    logger.info("[ASSERT] 학습 목표 확인")
    assert quiz_page.is_learning_goal_displayed()

    logger.info("[ASSERT] 보기/답 영역 확인")
    assert quiz_page.is_option_displayed()

    logger.info("[ASSERT] 해설 영역 확인")
    assert quiz_page.is_explanation_displayed()

    logger.info("[TEST END] QUIZ Success Create")
    logger.info("==============================\n")