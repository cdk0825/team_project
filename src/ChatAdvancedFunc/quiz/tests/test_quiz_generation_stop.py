import pytest
from src.utils import login
from src.ChatAdvancedFunc.quiz.pages.quiz_create_page import QUIZCreatePage


def test_quiz_generation_stop(driver):
    """
    QUIZ 생성 중지 기능 테스트
    - 유형/난이도 선택
    - 주제 입력
    - 생성 → 다시 생성
    - STOP 아이콘 클릭
    - 중지 안내 멘트 노출 확인
    """

    print("\n==============================")
    print("[TEST START] QUIZ Generation Stop")

    login(driver, "qa3team01@elicer.com", "20qareset25elice!")
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

    quiz_page.click_stop_icon()
    print("[STEP] 생성 중지(STOP) 클릭")

    stop_message = quiz_page.get_stop_message_text()
    print(f"[RESULT] 중지 멘트: {stop_message}")

    assert stop_message is not None
    assert "요청에 의해 답변 생성을 중지했습니다." in stop_message

    print("[ASSERT PASS] 중지 안내 멘트 정상 노출")
    print("[TEST END] QUIZ Generation Stop")
    print("==============================\n")
