import pytest
from src.ChatAdvancedFunc.ppt.pages.ppt_create_page import PPTCreatePage
from src.utils import login

# 500자 이상 테스트 데이터
LONG_TOPIC = (
    "The quick brown fox jumps over the lazy dog, a sentence often used in typing practice due to its inclusion of every letter in the English alphabet. "
    "Beyond its linguistic utility, this phrase has become emblematic of completeness in text testing and font rendering. "
    "In software development, long strings such as this one are frequently used to evaluate input field limitations, text overflow handling, and character encoding issues. "
    "By testing with a string exceeding typical lengths, developers can ensure that their applications gracefully handle extreme cases without crashing or corrupting data. "
    "Moreover, such tests can uncover subtle bugs related to memory allocation, UI layout, and database storage, providing a more robust and user-friendly experience. "
    "This methodology, when applied consistently, significantly improves the reliability and resilience of software systems across various platforms and devices."
)

@pytest.mark.parametrize("topic, expect_error", [
    ("", True),             # 빈값
    ("A", False),           # 최소값 1자
    ("Valid Topic", False), # 정상 입력
    (LONG_TOPIC, True),     # 500자 초과
])
def test_topic_input_validation(driver, topic, expect_error):
    """
    주제 입력 필드 유효성 검증
    1. 빈값, 정상값, 500자 초과 값 테스트
    2. 오류 메시지 발생 여부 확인
    """
    
    print("\n==============================")
    print("[TEST START] Topic Input Validation")
    
    # given
    login(driver, "qa3team01@elicer.com", "20qareset25elice!")
    print("[STEP] 관리자 로그인 완료")

    ppt_page = PPTCreatePage(driver)

    ppt_page.click_tool_tab()
    print("[STEP] 도구 탭 클릭")

    ppt_page.click_ppt_tab()
    print("[STEP] PPT 생성 탭 클릭")

    ppt_page.clear_inputs()
    print("[STEP] 입력값 초기화")

    # when
    ppt_page.enter_topic(topic)
    print("[STEP] 주제 입력 완료")

    # then
    error_text = ppt_page.get_topic_error_text()
    print(f"[RESULT] error_text: {error_text}")

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

    print("[TEST END] Topic Input Validation")
    print("==============================\n")