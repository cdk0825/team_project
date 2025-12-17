import pytest
from src.utils import login
from src.config import USERNAME4, PASSWORD4
from src.ChatAdvancedFunc.deep.pages.deep_create_page import DEEPCreatePage


@pytest.mark.parametrize(
    "instruction_input, expect_enabled, expect_error",
    [
        ("", True, False),          # 미입력 → 활성화(필수값 아님)
        ("정상 지시사항 입력", True, False),  # 정상 입력 → 버튼 활성화
        ("a" * 2001, False, True),      # 2000자 초과 → 버튼 비활성화 + 에러
    ]
)
def test_deep_instruction_input_validation(
    driver, instruction_input, expect_enabled, expect_error
):
    """
    DEEP 지시사항 입력값 검증
    1. 지시사항은 필수 아님
       - 미입력 → 버튼 비활성화
       - 정상 입력 → 버튼 활성화
    2. 2000자 초과 입력 시
       - 버튼 비활성화
       - '2000자 이하로 입력해주세요.' 에러 메시지 표시
    """

    print("\n==============================")
    print("[TEST START] DEEP Instruction Input Validation")

    login(driver, USERNAME4, PASSWORD4)
    print("[STEP] 로그인 완료")

    deep_page = DEEPCreatePage(driver)

    deep_page.click_tool_tab()
    print("[STEP] 도구 탭 클릭")

    deep_page.click_deep_tab()
    print("[STEP] 심층 조사 탭 클릭")

    deep_page.clear_inputs()
    print("[STEP] 입력값 초기화")

    # 필수 입력값: 주제
    deep_page.enter_topic("AI 모델 성능 비교")
    deep_page.blur_topic()
    print("[STEP] 주제 입력 완료")

    deep_page.enter_instruction(instruction_input)
    deep_page.blur_instruction()
    print(f"[STEP] 지시사항 입력값 길이: {len(instruction_input)}")

    is_enabled = deep_page.is_create_button_enabled()
    print(f"[RESULT] 생성 버튼 활성화 상태: {is_enabled}")
    assert is_enabled is expect_enabled, "생성 버튼 활성화 상태가 기대값과 다름"

    if expect_error:
        error_text = deep_page.get_instruction_error_text()
        print(f"[RESULT] 지시사항 에러 메시지: {error_text}")
        assert error_text == "2000자 이하로 입력해주세요.", \
            "지시사항 길이 초과 시 에러 메시지가 표시되지 않음"

    print("[TEST END] DEEP Instruction Input Validation")
    print("==============================\n")
