import pytest
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from src.ChatAdvancedFunc.quiz.pages.quiz_create_page import QUIZCreatePage

@pytest.mark.parametrize("option_type", ["single", "multi", "subjective"])
def test_quiz_option_type_result(driver, option_type):
    """
    QUIZ 유형별 생성 결과 검증
    - 난이도/주제는 동일 입력
    - 생성 완료 메시지/문제/학습목표/해설 확인
    - 보기와 체크 아이콘 개수 검증
    """
    print("\n==============================")
    print(f"[TEST START] Quiz Option Type: {option_type}")

    login(driver, USERNAME1, PASSWORD1)
    print("[STEP] 로그인 완료")

    quiz_page = QUIZCreatePage(driver)
    
    quiz_page.click_tool_tab()
    print("[STEP] QUIZ 생성 탭 클릭")
    quiz_page.click_quiz_tab()
    
    print("[STEP] 입력값 초기화")
    quiz_page.clear_inputs()

    print("[STEP] 유형 선택")
    quiz_page.select_option_type()
    if option_type == "single":
        quiz_page.select_option_type_single()
    elif option_type == "multi":
        quiz_page.select_option_type_multi()
    else:
        quiz_page.select_option_type_subjective()

    print("[STEP] 난이도 선택: 중")
    quiz_page.select_difficulty()
    quiz_page.select_difficulty_middle()

    print("[STEP] 주제 입력")
    quiz_page.enter_topic("운영체제 기본 개념")

    print("[ASSERT] 생성 버튼 활성화 확인")
    assert quiz_page.is_create_button_enabled() is True
    quiz_page.click_create()
    quiz_page.click_regenerate()
    print("[WAIT] QUIZ 생성 완료 대기 (STOP 아이콘 사라질 때까지)")
    quiz_page.wait_generation_complete()

    print("[ASSERT] 생성 완료 메시지 확인")
    assert quiz_page.wait_success_message().is_displayed()
    print("[ASSERT] 문제 영역 확인")
    assert quiz_page.is_question_displayed()
    print("[ASSERT] 학습 목표 확인")
    assert quiz_page.is_learning_goal_displayed()
    print("[ASSERT] 해설 영역 확인")
    assert quiz_page.is_explanation_displayed()

    print("[ASSERT] 보기/답 영역 확인")
    option_b_displayed = quiz_page.is_option_b_displayed()
    check_count = quiz_page.get_check_icon_count()

    if option_type == "single":
        assert option_b_displayed is True
        assert check_count == 1
    elif option_type == "multi":
        assert option_b_displayed is True
        assert check_count >= 2
    else:
        assert option_b_displayed is False
        assert check_count == 1

    print(f"[RESULT] Option B displayed: {option_b_displayed}, Check icon count: {check_count}")
    print(f"[TEST END] Quiz Option Type Result: {option_type}")
    print("==============================\n")
