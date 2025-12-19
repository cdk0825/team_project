import pytest
from src.utils.logger import get_logger 
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from src.ChatAdvancedFunc.quiz.pages.quiz_create_page import QUIZCreatePage

logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T114")
@pytest.mark.parametrize("difficulty", [
    "high",    # 상
    "middle",  # 중
    "low",     # 하
])
def test_quiz_difficulty(driver, difficulty):
    """
    난이도별 정상 생성 테스트
    - 유형: 객관식(단일)
    - 주제: 강아지와 개의 차이
    - 난이도: 상/중/하 각각 테스트
    - 생성 결과 확인 (문제/학습목표/보기/답/해설)
    """
    logger.info("\n==============================")
    logger.info(f"[TEST START] Quiz Difficulty Test - {difficulty.upper()}")

    login(driver, USERNAME1, PASSWORD1)
    logger.info("[STEP] 관리자 로그인 완료")

    quiz_page = QUIZCreatePage(driver)
    
    quiz_page.click_tool_tab()
    quiz_page.click_quiz_tab()
    logger.info("[STEP] QUIZ 생성 화면 진입")

    logger.info("[STEP] 입력값 초기화")
    quiz_page.clear_inputs()

    # 유형 선택
    logger.info("[STEP] 유형 선택: 객관식(단일)")
    quiz_page.select_option_type()
    quiz_page.select_option_type_single()

    # 난이도 선택
    logger.info(f"[STEP] 난이도 선택: {difficulty}")
    quiz_page.select_difficulty()
    if difficulty == "high":
        quiz_page.select_difficulty_high()
    elif difficulty == "middle":
        quiz_page.select_difficulty_middle()
    elif difficulty == "low":
        quiz_page.select_difficulty_low()

    logger.info("[STEP] 주제 입력")
    quiz_page.enter_topic("강아지와 개의 차이")
    
    is_enabled = quiz_page.is_create_button_enabled()
    logger.info(f"[RESULT] 생성 버튼 활성화 상태: {is_enabled}")

    if is_enabled is not True:
        logger.error(
            "[ERROR] 생성 버튼 비활성화됨 "
            f"(difficulty={difficulty})"
        )

    assert is_enabled is True
    logger.info("[ASSERT PASS] 생성 버튼 활성화")

    quiz_page.click_create()
    logger.info("[STEP] 생성 버튼 클릭")
    quiz_page.click_regenerate()
    logger.info("[STEP] 다시 생성 버튼 클릭")
    
    logger.info("[WAIT] QUIZ 생성 완료 대기 (STOP 아이콘 사라질 때까지)")
    quiz_page.wait_generation_complete()

    success_msg = quiz_page.wait_success_message()
    if not success_msg.is_displayed():
        logger.error(
            "[ERROR] 생성 완료 메시지 미노출 "
            f"(difficulty={difficulty})"
        )

    assert success_msg.is_displayed()
    logger.info("[ASSERT PASS] 생성 완료 메시지 노출")

    # 생성 결과 영역 검증
    if not quiz_page.is_question_displayed():
        logger.error("[ERROR] 문제 영역 미노출")
    assert quiz_page.is_question_displayed()

    if not quiz_page.is_learning_goal_displayed():
        logger.error("[ERROR] 학습목표 영역 미노출")
    assert quiz_page.is_learning_goal_displayed()

    if not quiz_page.is_option_displayed():
        logger.error("[ERROR] 보기 영역 미노출")
    assert quiz_page.is_option_displayed()

    if not quiz_page.is_explanation_displayed():
        logger.error("[ERROR] 해설 영역 미노출")
    assert quiz_page.is_explanation_displayed()

    logger.info(f"[TEST END] Quiz Difficulty Test - {difficulty.upper()}")
    logger.info("==============================\n")
