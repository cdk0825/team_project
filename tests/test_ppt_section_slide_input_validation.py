import pytest
from src.utils.logger import get_logger 
from f1_helpychat.src.pages.ppt_create_page import PPTCreatePage
from src.utils import login
from f1_helpychat.data.config import USERNAME1, PASSWORD1

# 로깅 설정
logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T40")
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
    
    logger.info("==============================\n")
    logger.info("\n [TEST START] Section / Slide Input Validation")
    
    try:
        login(driver, USERNAME1, PASSWORD1)
        logger.info("[STEP] 관리자 로그인 완료")
        
        ppt_page = PPTCreatePage(driver)

        ppt_page.click_tool_tab()
        ppt_page.click_ppt_tab()
        logger.info("[STEP] PPT 생성 화면 진입")

        ppt_page.clear_inputs()
        logger.info("[STEP] 입력값 초기화")

        ppt_page.enter_section_input(testdata)
        ppt_page.enter_slide_input(testdata)
        logger.info("[STEP] 입력값 입력 완료")

        section_value = ppt_page.get_section_value()
        slide_value = ppt_page.get_slide_value()
        logger.info(f"[RESULT] section_value: '{section_value}', slide_value: '{slide_value}'")

        # 섹션 입력 검증
        if section_value != expected:
            logger.error(
                f"[ERROR] 섹션 입력값 불일치 - input='{testdata}', "
                f"expected='{expected}', actual='{section_value}'"
            )
        assert section_value == expected, \
            f"섹션 입력폼에 잘못된 값이 들어감: {section_value}"

        # 슬라이드 입력 검증
        if slide_value != expected:
            logger.error(
                f"[ERROR] 슬라이드 입력값 불일치 - input='{testdata}', "
                f"expected='{expected}', actual='{slide_value}'"
            )
        assert slide_value == expected, \
            f"슬라이드 입력폼에 잘못된 값이 들어감: {slide_value}"
            
    except Exception as e:
      logger.exception("[TEST ERROR] 예외 발생")
      raise

    finally:    
        logger.info("[ASSERT PASS] 섹션 / 슬라이드 입력값 검증 성공")
        logger.info("[TEST END] Section / Slide Input Validation")
        logger.info("==============================\n")