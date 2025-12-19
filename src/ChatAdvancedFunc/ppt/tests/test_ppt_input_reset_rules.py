import pytest
from src.utils.logger import get_logger 
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from src.ChatAdvancedFunc.ppt.pages.ppt_create_page import PPTCreatePage

# 로깅 설정
logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T160")
@pytest.mark.xfail(reason="PPT 생성 화면 진입 시 입력값 자동 초기화 미구현")
def test_input_reset_rules(driver):
    """
    입력값 초기화 검증
    - PPT 생성 화면 재진입 시
      이전에 입력한 값(주제/지시사항/섹션/슬라이드)이 자동으로 초기화되어야 함
    - 현재는 초기화되지 않아 xfail로 관리
    """

    logger.info("\n==============================")
    logger.info("[TEST START] PPT Input Reset Rules Validation")

    login(driver, USERNAME1, PASSWORD1)
    logger.info("[STEP] 관리자 로그인 완료")

    ppt_page = PPTCreatePage(driver)

    ppt_page.click_tool_tab()
    logger.info("[STEP] 도구 탭 클릭")

    ppt_page.click_ppt_tab()
    logger.info("[STEP] PPT 생성 탭 클릭")
    
    logger.info("[STEP] 입력값 초기화")
    ppt_page.clear_inputs()

    logger.info("[STEP] 입력값 입력")
    ppt_page.enter_topic("입력값 초기화 테스트")
    ppt_page.enter_instruction("입력값 초기화 지시사항 테스트")
    ppt_page.enter_section_input(2)
    ppt_page.enter_slide_input(4)
    
    ppt_page.click_create()
    logger.info("[STEP] 생성 버튼 클릭")

    ppt_page.click_regenerate()
    logger.info("[STEP] 다시 생성 버튼 클릭")
   
    logger.info("[WAIT] PPT 생성 완료 대기 (STOP 아이콘 사라질 때까지)")
    ppt_page.wait_generation_complete()

    download_btn = ppt_page.wait_download_button()
    assert download_btn.is_displayed()
    logger.info("[ASSERT PASS] 다운로드 버튼 정상 노출")

    # 다시 PPT 생성 화면 진입
    logger.info("[STEP] 새 대화 진입")
    ppt_page.click_newchat_tab()
    
    logger.info("[STEP] PPT 생성 탭 재진입")
    ppt_page.click_tool_tab()
    ppt_page.click_ppt_tab()

    # 입력값 초기화 여부 확인
    topic_value = ppt_page.get_topic_value()
    instruction_value = ppt_page.get_instruction_value()
    section_value = ppt_page.get_section_value()
    slide_value = ppt_page.get_slide_value()

    logger.info(f"[RESULT] topic_value: '{topic_value}'")
    logger.info(f"[RESULT] instruction_value: '{instruction_value}'")
    logger.info(f"[RESULT] section_value: '{section_value}'")
    logger.info(f"[RESULT] slide_value: '{slide_value}'")

    logger.info("[EXPECT] 모든 입력값이 초기화되어 있어야 함")
    assert topic_value == "", "주제 입력값이 초기화되지 않음"
    assert instruction_value == "", "지시사항 입력값이 초기화되지 않음"
    assert section_value == "", "섹션 입력값이 초기화되지 않음"
    assert slide_value == "", "슬라이드 입력값이 초기화되지 않음"

    logger.info("[ASSERT PASS] 입력값 자동 초기화 확인")

    logger.info("[TEST END] PPT Input Reset Rules Validation")
    logger.info("==============================\n")
