import pytest
from src.utils import login
from src.config import USERNAME4, PASSWORD4
from src.ChatAdvancedFunc.quiz.pages.quiz_create_page import QUIZCreatePage

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
    print("\n==============================")
    print("[TEST START] Quiz Input Validation")
    
    # 로그인(초기화 기능 이슈로 이전 퀴즈 생성 기록이 없는 계정이어야함)
    login(driver, USERNAME4, PASSWORD4)
    print("[STEP] 로그인 완료")

    quiz_page = QUIZCreatePage(driver)

    quiz_page.click_tool_tab()
    print("[STEP] 도구 탭 클릭")
    quiz_page.click_quiz_tab()
    print("[STEP] 퀴즈 생성 탭 클릭")

    quiz_page.clear_inputs()
    print("[STEP] 입력값 초기화 완료")
    
    if not skip_topic:
        quiz_page.enter_topic("테스트 퀴즈 주제")
        print("[STEP] 주제 입력 완료")
    else:
        print("[STEP] 주제 입력 생략")
        quiz_page.trigger_topic_validation()

    if not skip_option:
        quiz_page.select_option_type()
        quiz_page.select_option_type_single()
        print("[STEP] 유형 선택 완료")
    else:
        print("[STEP] 유형 선택 생략")

    if not skip_difficulty:
        quiz_page.select_difficulty()
        quiz_page.select_difficulty_middle()
        print("[STEP] 난이도 선택 완료")
    else:
        print("[STEP] 난이도 선택 생략")

    is_enabled = quiz_page.is_create_button_enabled()
    print(f"[RESULT] 생성 버튼 활성화 상태: {is_enabled}")
    assert is_enabled is False, "생성 버튼이 활성화 되어 있음! 필수 입력값 검증 실패"
    
    if expect_topic_error:
        topic_error_text = quiz_page.get_topic_error_text()
        print(f"[RESULT] 주제 에러 메시지: {topic_error_text}")
        assert topic_error_text == "1자 이상 입력해주세요.", \
            "주제 미입력 시 에러 메시지가 표시되지 않음"

    print("[ASSERT PASS] 필수 입력값 유효성 검증 성공")
    print("[TEST END] Quiz Input Validation")
    print("==============================\n")