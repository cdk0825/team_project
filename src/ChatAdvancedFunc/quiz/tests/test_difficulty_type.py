import pytest
from src.utils import login
from src.ChatAdvancedFunc.quiz.pages.quiz_create_page import QUIZCreatePage

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
    print("\n==============================")
    print(f"[TEST START] Quiz Difficulty Test - {difficulty.upper()}")

    # given
    login(driver, "qa3team01@elicer.com", "20qareset25elice!")
    print("[STEP] 관리자 로그인 완료")

    quiz_page = QUIZCreatePage(driver)
    
    quiz_page.click_tool_tab()
    assert "/tools" in driver.current_url

    print("[STEP] QUIZ 생성 탭 클릭")
    quiz_page.click_quiz_tab()

    print("[STEP] 입력값 초기화")
    quiz_page.clear_inputs()

    # 유형 선택
    print("[STEP] 유형 선택: 객관식(단일)")
    quiz_page.select_option_type()
    quiz_page.select_option_type_single()

    # 난이도 선택
    print(f"[STEP] 난이도 선택: {difficulty}")
    quiz_page.select_difficulty()
    if difficulty == "high":
        quiz_page.select_difficulty_high()
    elif difficulty == "middle":
        quiz_page.select_difficulty_middle()
    elif difficulty == "low":
        quiz_page.select_difficulty_low()

    print("[STEP] 주제 입력")
    quiz_page.enter_topic("강아지와 개의 차이")

    assert quiz_page.is_create_button_enabled() is True
    print("[ASSERT PASS] 생성 버튼 활성화")

    print("[STEP] 생성 버튼 클릭")
    quiz_page.click_create()
    print("[STEP] 다시 생성 버튼 클릭")
    quiz_page.click_regenerate()
    
    print("[WAIT] QUIZ 생성 완료 대기 (STOP 아이콘 사라질 때까지)")
    quiz_page.wait_generation_complete()

    print("[ASSERT] 생성 완료 메시지 확인")
    assert quiz_page.wait_success_message().is_displayed()
    
    print("[ASSERT] 생성 결과 확인")
    assert quiz_page.is_question_displayed()
    assert quiz_page.is_learning_goal_displayed()
    assert quiz_page.is_option_displayed()
    assert quiz_page.is_explanation_displayed()

    print(f"[TEST END] Quiz Difficulty Test - {difficulty.upper()}")
    print("==============================\n")
