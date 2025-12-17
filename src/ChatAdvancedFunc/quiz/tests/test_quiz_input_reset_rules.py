import pytest
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from src.ChatAdvancedFunc.quiz.pages.quiz_create_page import QUIZCreatePage

@pytest.mark.xfail(reason="QUIZ 생성 화면 진입 시 입력값 자동 초기화 미구현")
def test_input_reset_rules(driver):
    """
    입력값 초기화 검증
    - QUIZ 생성 화면 재진입 시
      이전에 입력한 값(유형/난이도/주제)이 자동으로 초기화되어야 함
    - 현재는 초기화되지 않아 xfail로 관리
    """

    print("\n==============================")
    print("[TEST START] QUIZ Input Reset Rules Validation")

    login(driver, USERNAME1, PASSWORD1)
    print("[STEP] 관리자 로그인 완료")

    quiz_page = QUIZCreatePage(driver)

    quiz_page.click_tool_tab()
    assert "/tools" in driver.current_url
    
    print("[STEP] QUIZ 생성 탭 클릭")
    quiz_page.click_quiz_tab()
    
    print("[STEP] 입력값 초기화")
    quiz_page.clear_inputs()
    
    print("[STEP] 유형 선택")
    quiz_page.select_option_type()

    print("[STEP] 유형 선택: 객관식(단일)")
    quiz_page.select_option_type_single()

    print("[STEP] 난이도 선택")
    quiz_page.select_difficulty()
    
    print("[STEP] 난이도 선택: 중")
    quiz_page.select_difficulty_middle()

    print("[STEP] 주제 입력")
    quiz_page.enter_topic("운영체제의 기본 개념")

    print("[ASSERT] 생성 버튼 활성화 확인")
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

    # 다시 QUIZ 생성 화면 진입
    print("[STEP] 새 대화 진입")
    quiz_page.click_newchat_tab()
    
    print("[STEP] QUIZ 생성 탭 재진입")
    quiz_page.click_tool_tab()
    quiz_page.click_quiz_tab()

    # 입력값 초기화 여부 확인
    option_value = quiz_page.get_option_value()
    difficulty_value = quiz_page.get_difficulty_value()
    topic_value = quiz_page.get_topic_value()
    
    print(f"[RESULT] option_value: '{option_value}'")
    print(f"[RESULT] difficulty_value: '{difficulty_value}'")
    print(f"[RESULT] topic_value: '{topic_value}'")

    print("[EXPECT] 모든 입력값이 초기화되어 있어야 함")
    assert option_value == "", "유형 입력값이 초기화되지 않음"
    assert difficulty_value == "", "난이도 입력값이 초기화되지 않음"
    assert topic_value == "", "주제 입력값이 초기화되지 않음"

    print("[ASSERT PASS] 입력값 자동 초기화 확인")

    print("[TEST END] QUIZ Input Reset Rules Validation")
    print("==============================\n")
