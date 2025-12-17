import pytest
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from src.ChatAdvancedFunc.deep.pages.deep_create_page import DEEPCreatePage


@pytest.mark.xfail(reason="심층조사 생성 화면 진입 시 입력값 자동 초기화 미구현")
def test_deep_input_reset_rules(driver):
    """
    입력값 초기화 검증
    - 심층조사 생성 화면 재진입 시
      이전에 입력한 값(주제/지시사항)이 자동으로 초기화되어야 함
    - 현재는 초기화되지 않아 xfail로 관리
    """

    print("\n==============================")
    print("[TEST START] DEEP Input Reset Rules Validation")

    login(driver, USERNAME1, PASSWORD1)
    print("[STEP] 관리자 로그인 완료")

    deep_page = DEEPCreatePage(driver)

    deep_page.click_tool_tab()
    print("[STEP] 도구 탭 클릭")

    deep_page.click_deep_tab()
    print("[STEP] 심층 조사 탭 클릭")

    deep_page.clear_inputs()
    print("[STEP] 주제 / 지시사항 입력값 초기화")

    deep_page.enter_topic("AI 모델의 성능 비교")
    print("[STEP] 주제 입력 완료")

    deep_page.enter_instruction(
        "최신 GPT, Gemini 모델의 차이를 표로 정리하라. "
        "참고한 근거를 단계별로 제시하라."
    )
    print("[STEP] 지시사항 입력 완료")
    
    is_enabled = deep_page.is_create_button_enabled()
    print(f"[ASSERT] 생성 버튼 활성화 여부: {is_enabled}")
    assert is_enabled is True, "생성 버튼이 활성화되지 않음"

    deep_page.click_create()
    print("[STEP] 생성 버튼 클릭")

    deep_page.click_regenerate()
    print("[STEP] 다시 생성 버튼 클릭")

    print("[WAIT] 심층 조사 생성 완료 대기 (STOP 아이콘 사라질 때까지)")
    deep_page.wait_generation_complete()
    
    print("[ASSERT] 생성 완료 메시지 확인")
    assert deep_page.wait_success_message().is_displayed()

    # 다시 심층조사 생성 화면 진입
    print("[STEP] 새 대화 진입")
    deep_page.click_newchat_tab()
    
    print("[STEP] 심층조사 탭 재진입")
    deep_page.click_tool_tab()
    deep_page.click_deep_tab()

    # 입력값 초기화 여부 확인
    topic_value = deep_page.get_topic_value()
    instruction_value = deep_page.get_instruction_value()

    print(f"[RESULT] topic_value: '{topic_value}'")
    print(f"[RESULT] instruction_value: '{instruction_value}'")

    print("[EXPECT] 모든 입력값이 초기화되어 있어야 함")
    assert topic_value == "", "주제 입력값이 초기화되지 않음"
    assert instruction_value == "", "지시사항 입력값이 초기화되지 않음"

    print("[ASSERT PASS] 입력값 자동 초기화 확인")

    print("[TEST END] DEEP Input Reset Rules Validation")
    print("==============================\n")
