import pytest
from src.utils.logger import get_logger 
from src.ChatAdvancedFunc.ppt.pages.ppt_create_page import PPTCreatePage
from src.utils import login
from src.config import USERNAME1, PASSWORD1

# 로깅 설정
logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T84", "F1HEL_T85", "F1HEL_T86")
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
    logger.info("\n [TEST START] Section / Slide Business Rules Validation")

    login(driver, USERNAME1, PASSWORD1)
    logger.info("[STEP] 관리자 로그인 완료")

    ppt_page = PPTCreatePage(driver)

    ppt_page.click_tool_tab()
    logger.info("[STEP] 도구 탭 클릭")
    ppt_page.click_ppt_tab()
    logger.info("[STEP] PPT 생성 탭 클릭")

    ppt_page.clear_inputs()
    logger.info("[STEP] 입력값 초기화")
    
    ppt_page.enter_topic("이순신")
    logger.info("[STEP] 필수 입력값 주제 입력: 이순신")

    ppt_page.enter_section_input(section_count)
    ppt_page.enter_slide_input(slide_count)
    logger.info(f"[STEP] 섹션 수 입력: {section_count}, 슬라이드 수 입력: {slide_count}")

    if should_create:
        logger.info("[EXPECT] 생성 버튼이 활성화되어야 함")
        logger.info("[ASSERT] 생성 버튼 활성화 확인")
        assert ppt_page.is_create_button_enabled() is True
        logger.info("[ASSERT PASS] 생성 버튼 활성화 상태")
    else:
        logger.info("[EXPECT] 생성 버튼이 비활성화되어야 함")
        assert ppt_page.is_create_button_enabled() is False, \
            "섹션 수가 슬라이드 수보다 큰데 생성 버튼이 활성화됨"
        logger.info("[ASSERT PASS] 잘못된 조건에서 생성 버튼 비활성 확인")

    logger.info("[TEST END] Section / Slide Business Rules Validation")
    logger.info("==============================\n")
