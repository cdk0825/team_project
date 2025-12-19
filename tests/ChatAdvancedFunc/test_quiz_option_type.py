import pytest
from src.utils.logger import get_logger 
from src.utils import login
from f1_helpychat.data.config import USERNAME1, PASSWORD1
from f1_helpychat.src.pages.quiz_create_page import QUIZCreatePage

logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T115")
@pytest.mark.parametrize("option_type", ["single", "multi", "subjective"])
def test_quiz_option_type_result(driver, option_type):
    """
    QUIZ 유형별 생성 결과 검증
    - 난이도/주제는 동일 입력
    - 생성 완료 메시지/문제/학습목표/해설 확인
    - 보기와 체크 아이콘 개수 검증
    """
    logger.info("\n==============================")
    logger.info(f"[TEST START] Quiz Option Type: {option_type}")

    login(driver, USERNAME1, PASSWORD1)
    logger.info("[STEP] 로그인 완료")

    quiz_page = QUIZCreatePage(driver)
    
    quiz_page.click_tool_tab()
    quiz_page.click_quiz_tab()
    logger.info("[STEP] QUIZ 화면 진입")
    
    quiz_page.clear_inputs()
    logger.info("[STEP] 입력값 초기화")

    quiz_page.select_option_type()
    if option_type == "single":
        quiz_page.select_option_type_single()
        logger.info("[STEP] 유형 선택: 객관식(단일)")
    elif option_type == "multi":
        quiz_page.select_option_type_multi()
        logger.info("[STEP] 유형 선택: 객관식(복수)")
    else:
        quiz_page.select_option_type_subjective()
        logger.info("[STEP] 유형 선택: 주관식")

    quiz_page.select_difficulty()
    quiz_page.select_difficulty_middle()
    logger.info("[STEP] 난이도 선택: 중")

    quiz_page.enter_topic("운영체제 기본 개념")
    logger.info("[STEP] 주제 입력")

    is_enabled = quiz_page.is_create_button_enabled()
    logger.info(f"[RESULT] 생성 버튼 활성화 상태: {is_enabled}")

    if is_enabled is not True:
        logger.error(
            "[ERROR] 생성 버튼 비활성화됨 "
            f"- option_type={option_type}"
        )

    assert is_enabled is True
    logger.info("[ASSERT PASS] 생성 버튼 활성화")
    
    quiz_page.click_create()
    quiz_page.click_regenerate()
    logger.info("[STEP] 생성 -> 다시 생성 클릭")
    
    logger.info("[WAIT] QUIZ 생성 완료 대기 (STOP 아이콘 사라질 때까지)")
    quiz_page.wait_generation_complete()

    success_msg = quiz_page.wait_success_message()
    if not success_msg.is_displayed():
        logger.error("[ERROR] 생성 완료 메시지 미노출")

    assert success_msg.is_displayed()
    logger.info("[ASSERT PASS] 생성 완료 메시지 노출")
    
    # 생성 결과 영역 검증
    if not quiz_page.is_question_displayed():
        logger.error("[ERROR] 문제 영역 미노출")
    assert quiz_page.is_question_displayed()

    if not quiz_page.is_learning_goal_displayed():
        logger.error("[ERROR] 학습 목표 영역 미노출")
    assert quiz_page.is_learning_goal_displayed()

    if not quiz_page.is_explanation_displayed():
        logger.error("[ERROR] 해설 영역 미노출")
    assert quiz_page.is_explanation_displayed()
    
    option_b_displayed = quiz_page.is_option_b_displayed()
    check_count = quiz_page.get_check_icon_count()

    logger.info(
        f"[RESULT] option_b_displayed={option_b_displayed}, "
        f"check_icon_count={check_count}"
    )

    if option_type == "single":
        if option_b_displayed is not True or check_count != 1:
            logger.error(
                "[ERROR] 객관식(단일) 결과 오류 "
                f"- option_b={option_b_displayed}, check_count={check_count}"
            )
        assert option_b_displayed is True
        assert check_count == 1

    elif option_type == "multi":
        if option_b_displayed is not True or check_count < 2:
            logger.error(
                "[ERROR] 객관식(복수) 결과 오류 "
                f"- option_b={option_b_displayed}, check_count={check_count}"
            )
        assert option_b_displayed is True
        assert check_count >= 2

    else:  # subjective
        if option_b_displayed is not False or check_count != 1:
            logger.error(
                "[ERROR] 주관식 결과 오류 "
                f"- option_b={option_b_displayed}, check_count={check_count}"
            )
        assert option_b_displayed is False
        assert check_count == 1
        
    logger.info("[ASSERT PASS] 문제 유형 별 결과 생성 확인")
    logger.info(f"[TEST END] Quiz Option Type Result: {option_type}")
    logger.info("==============================\n")
