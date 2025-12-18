import pytest
from src.utils.logger import get_logger 
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from src.ChatAdvancedFunc.ppt.pages.ppt_create_page import PPTCreatePage

logger = get_logger(__file__)

def test_ppt_generation_stop(driver):
    """
    PPT 생성 중지 기능 테스트
    - 주제 / 지시사항 입력
    - 생성 → 다시 생성
    - STOP 아이콘 클릭
    - 중지 안내 멘트 노출 확인
    """

    logger.info("\n==============================")
    logger.info("[TEST START] PPT Generation Stop")

    login(driver, USERNAME1, PASSWORD1)
    logger.info("[STEP] 관리자 로그인 완료")

    ppt_page = PPTCreatePage(driver)

    ppt_page.click_tool_tab()
    assert "/tools" in driver.current_url
    logger.info("[STEP] 도구 탭 진입")

    ppt_page.click_ppt_tab()
    logger.info("[STEP] PPT 생성 탭 진입")

    ppt_page.clear_inputs()
    logger.info("[STEP] 입력값 초기화")

    ppt_page.enter_topic("이순신")
    logger.info("[STEP] 주제 입력: 이순신")

    ppt_page.enter_instruction(
        "이순신에 대해서 텍스트, 이미지, 표를 활용하여 생성"
    )
    logger.info("[STEP] 지시사항 입력")

    ppt_page.click_create()
    logger.info("[STEP] 생성 버튼 클릭")

    ppt_page.click_regenerate()
    logger.info("[STEP] 다시 생성 버튼 클릭")

    ppt_page.click_stop_icon()
    logger.info("[STEP] 생성 중지(STOP) 클릭")

    stop_message = ppt_page.get_stop_message_text()
    logger.info(f"[RESULT] 중지 멘트: {stop_message}")

    assert stop_message is not None
    assert "요청에 의해 답변 생성을 중지했습니다." in stop_message

    logger.info("[ASSERT PASS] 중지 안내 멘트 정상 노출")
    logger.info("[TEST END] PPT Generation Stop")
    logger.info("==============================\n")
