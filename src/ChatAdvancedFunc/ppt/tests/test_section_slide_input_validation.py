import pytest
from src.ChatAdvancedFunc.ppt.pages.ppt_create_page import PPTCreatePage
from src.utils import login
from src.config import USERNAME1, PASSWORD1

@pytest.mark.parametrize("testdata, expected", [
    ("강아지", ""),   # 한글 문자 입력 -> 비어야 함
    ("abc", ""),      # 영어 문자 입력 -> 비어야 함
    ("5", "5"),       # 숫자 입력 -> 그대로 들어가야 함
])
def test_section_slide_input_validation(driver, testdata, expected):
    """
    섹션 / 슬라이드 입력폼 숫자 유효성 검증
    - 문자 입력 시 차단
    - 숫자 입력 시 정상 입력 확인
    """
    print("\n [TEST START] Section / Slide Input Validation")
    
    login(driver, USERNAME1, PASSWORD1)
    print("[STEP] 관리자 로그인 완료")
    
    ppt_page = PPTCreatePage(driver)

    ppt_page.click_tool_tab()
    print("[STEP] 도구 탭 클릭")
    ppt_page.click_ppt_tab()
    print("[STEP] PPT 생성 탭 클릭")

    ppt_page.clear_inputs()
    print("[STEP] 입력값 초기화")

    ppt_page.enter_section_input(testdata)
    ppt_page.enter_slide_input(testdata)
    print("[STEP] 입력값 입력 완료")

    section_value = ppt_page.get_section_value()
    slide_value = ppt_page.get_slide_value()
    print(f"[RESULT] section_value: '{section_value}', slide_value: '{slide_value}'")

    assert section_value == expected, f"섹션 입력폼에 잘못된 값이 들어감: {section_value}"
    assert slide_value == expected, f"슬라이드 입력폼에 잘못된 값이 들어감: {slide_value}"

    print("[ASSERT PASS] 섹션 / 슬라이드 입력값 검증 성공")
    print("[TEST END] Section / Slide Input Validation")
    print("==============================\n")