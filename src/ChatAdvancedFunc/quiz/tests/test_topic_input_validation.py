import pytest
from src.utils import login
from src.ChatAdvancedFunc.quiz.pages.quiz_create_page import QUIZCreatePage

def test_topic_input_validation(driver):
    """
    QUIZ 생성 시 주제를 입력하지 않으면
    - '1자 이상 입력해주세요.' 메시지가 표시됨
    """
    print("\n==============================")
    print("[TEST START] Quiz Topic Input Validation")
    
    # 로그인
    login(driver, "qa3team01@elicer.com", "20qareset25elice!")
    print("[STEP] 로그인 완료")

    quiz_page = QUIZCreatePage(driver)

    quiz_page.click_tool_tab()
    print("[STEP] 도구 탭 클릭")
    quiz_page.click_quiz_tab()
    print("[STEP] 퀴즈 생성 탭 클릭")

    quiz_page.clear_inputs()
    print("[STEP] 입력값 초기화 완료")

    # 유형/난이도는 선택해서 메시지 발생 조건만 충족
    quiz_page.select_option_type()
    quiz_page.select_option_type_single()
    quiz_page.select_difficulty()
    quiz_page.select_difficulty_middle()
    print("[STEP] 유형/난이도 선택 완료")

    # 주제 입력 에러 메시지 확인
    topic_error_text = quiz_page.get_topic_error_text()
    print(f"[RESULT] 주제 에러 메시지: {topic_error_text}")
    assert topic_error_text == "1자 이상 입력해주세요.", "주제 미입력 시 에러 메시지가 표시되지 않음!"

    print("[ASSERT PASS] 주제 필수 입력값 검증 성공")
    print("[TEST END] Quiz Topic Input Validation")
    print("==============================\n")
