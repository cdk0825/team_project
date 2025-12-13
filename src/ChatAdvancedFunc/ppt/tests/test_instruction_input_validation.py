import pytest
from src.ChatAdvancedFunc.ppt.pages.ppt_create_page import PPTCreatePage
from src.utils import login

# 2000자 초과 테스트 데이터
LONG_INSTRUCTION = (
    "This instruction text is intentionally long to verify the maximum length validation of the instruction input field. "
    "In modern web applications, instruction or description fields often allow flexible input, but they still require strict limits "
    "to prevent excessive data from being submitted, which could negatively impact performance, layout rendering, or backend processing. "
    "By entering a very long instruction string, testers can ensure that the system properly enforces character limits and displays "
    "clear and user-friendly error messages when those limits are exceeded. "
    "This test scenario is particularly important for AI-based content generation tools, where users may attempt to provide extremely "
    "detailed prompts containing background context, formatting requirements, and multiple content constraints. "
    "Such prompts may include requests for structured text, images, tables, bullet points, summaries, and comparisons, all within a single instruction. "
    "If the application fails to handle overly long input correctly, it could result in truncated data, unexpected behavior, or even system crashes. "
    "Therefore, validating the upper boundary of instruction input length is a critical aspect of quality assurance. "
    "This long instruction continues to add more descriptive content to ensure that the total character count comfortably exceeds two thousand characters. "
    "Additional sentences are included to simulate realistic user behavior, where users might copy and paste large amounts of text from documents, "
    "research notes, or external sources. "
    "These scenarios are common in educational, enterprise, and professional productivity tools, where rich and detailed instructions are frequently used. "
    "By repeatedly extending this instruction text with explanatory sentences, examples, and contextual information, we can confidently test "
    "whether the application correctly detects input length violations and responds with the appropriate validation message. "
    "The goal of this test data is not readability, but reliability, consistency, and robustness of the input validation logic. "
    "As the text grows longer, it continues to serve as a realistic approximation of extreme user input, ensuring that edge cases are properly handled. "
    "This approach helps uncover hidden issues related to frontend validation, backend constraints, database field sizes, and overall system stability. "
    "Ultimately, thorough testing with long instruction strings contributes to a higher quality user experience and a more resilient application. "
    "To further extend the length of this instruction, additional filler sentences are appended, reinforcing the importance of boundary testing. "
    "Quality assurance engineers rely on such deliberately excessive inputs to validate system behavior under abnormal but plausible conditions. "
    "This final section exists solely to push the total character count well beyond the two thousand character threshold, "
    "ensuring that the validation rule is triggered without ambiguity or flakiness during automated test execution."
)


@pytest.mark.parametrize("instruction, expect_error", [
    # ("", False),                  # 공백 (필수 아님)
    # ("간단한 지시사항", False),    # 정상 입력
    (LONG_INSTRUCTION, True),     # 2000자 초과
])
def test_instruction_input_validation(driver, instruction, expect_error):
    """
    지시사항 입력 필드 유효성 검증
    - 공백 허용
    - 2000자 초과 시 오류 메시지 노출
    """

    print("\n==============================")
    print("[TEST START] Instruction Input Validation")

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
    ppt_page.enter_instruction(instruction)
    print("[STEP] 지시사항 입력 완료")

    # then
    error_text = ppt_page.get_instruction_error_text()
    print(f"[RESULT] error_text: {error_text}")

    if expect_error:
        assert error_text == "2000자 이하로 입력해주세요.", (
            f"[ASSERT FAIL] Expected error but got: {error_text}"
        )
        print("[ASSERT PASS] 오류 메시지 정상 노출")
    else:
        assert error_text is None, (
            f"[ASSERT FAIL] Expected no error but got: {error_text}"
        )
        print("[ASSERT PASS] 오류 메시지 미노출 정상")

    print("[TEST END] Instruction Input Validation")
    print("==============================\n")
