import pytest
from src.ChatAdvancedFunc.ppt.pages.ppt_create_page import PPTCreatePage
from src.utils import login
from src.config import USERNAME1, PASSWORD1


@pytest.mark.parametrize(
    "section_count, slide_count, should_create",
    [
        pytest.param(
            "4", "2", False,
            marks=pytest.mark.xfail(
                reason="섹션 수 > 슬라이드 수 비즈니스 룰 검증 미구현"
            )
        ),
        ("3", "3", True),
        ("2", "4", True),
    ]
)
def test_section_slide_rules(driver, section_count, slide_count, should_create):
    """
    섹션 / 슬라이드 수 비즈니스 룰 검증
    - 섹션 수 > 슬라이드 수 : 생성 불가 (버튼 비활성 또는 오류 메시지 필요)
    - 섹션 수 = 슬라이드 수 : 정상 생성
    - 섹션 수 < 슬라이드 수 : 정상 생성
    """
    print("\n [TEST START] Section / Slide Business Rules Validation")

    login(driver, USERNAME1, PASSWORD1)
    print("[STEP] 관리자 로그인 완료")

    ppt_page = PPTCreatePage(driver)

    ppt_page.click_tool_tab()
    print("[STEP] 도구 탭 클릭")
    ppt_page.click_ppt_tab()
    print("[STEP] PPT 생성 탭 클릭")

    ppt_page.clear_inputs()
    print("[STEP] 입력값 초기화")
    
    ppt_page.enter_topic("이순신")
    print("[STEP] 필수 입력값 주제 입력: 이순신")

    ppt_page.enter_section_input(section_count)
    ppt_page.enter_slide_input(slide_count)
    print(f"[STEP] 섹션 수 입력: {section_count}, 슬라이드 수 입력: {slide_count}")

    if should_create:
        print("[EXPECT] 생성 버튼이 활성화되어야 함")
        print("[ASSERT] 생성 버튼 활성화 확인")
        assert ppt_page.is_create_button_enabled() is True
        print("[ASSERT PASS] 생성 버튼 활성화 상태")
    else:
        print("[EXPECT] 생성 버튼이 비활성화되어야 함")
        assert ppt_page.is_create_button_enabled() is False, \
            "섹션 수가 슬라이드 수보다 큰데 생성 버튼이 활성화됨"
        print("[ASSERT PASS] 잘못된 조건에서 생성 버튼 비활성 확인")

    print("[TEST END] Section / Slide Business Rules Validation")
    print("==============================\n")
