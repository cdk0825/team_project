import pytest
from src.ChatAdvancedFunc.ppt.pages.ppt_create_page import PPTCreatePage
from src.utils import login
from src.config import USERNAME1, PASSWORD1

@pytest.mark.parametrize("topic, expect_error, expect_enabled", [
    ("", True, False),              # 미입력
    ("A", False, True),             # 최소값
    ("Valid Topic", False, True),   # 정상
    ("a" * 501, True, False),      # 500자 초과
])
def test_topic_input_validation(driver, topic, expect_error, expect_enabled):
    """
    주제 입력 필드 유효성 검증
    - 미입력, 최소값 1자, 정상값, 500자 초과 값 테스트
    - 오류 메시지 발생 여부 확인
    """
    
    print("\n==============================")
    print("[TEST START] Topic Input Validation")

    login(driver, USERNAME1, PASSWORD1)
    print("[STEP] 관리자 로그인 완료")

    ppt_page = PPTCreatePage(driver)

    ppt_page.click_tool_tab()
    print("[STEP] 도구 탭 클릭")

    ppt_page.click_ppt_tab()
    print("[STEP] PPT 생성 탭 클릭")

    ppt_page.clear_inputs()
    print("[STEP] 입력값 초기화")

    ppt_page.enter_topic(topic)
    print(f"[STEP] 주제 입력값 길이: {len(topic)}")

    error_text = ppt_page.get_topic_error_text()
    print(f"[RESULT] error_text: {error_text}")
    
    is_enabled = ppt_page.is_create_button_enabled()
    print(f"[RESULT] 생성 버튼 활성화 상태: {is_enabled}")

    if expect_error:
        assert error_text == "1자 이상 500자 이하로 입력해주세요.", (
            f"[ASSERT FAIL] Expected error but got: {error_text}"
        )
        print("[ASSERT PASS] 오류 메시지 정상 노출")
    else:
        assert error_text is None, (
            f"[ASSERT FAIL] Expected no error but got: {error_text}"
        )
        print("[ASSERT PASS] 오류 메시지 미노출 정상")
    assert is_enabled is expect_enabled, (
        f"[ASSERT FAIL] 생성 버튼 상태 불일치: {is_enabled}"
    )

    print("[TEST END] Topic Input Validation")
    print("==============================\n")