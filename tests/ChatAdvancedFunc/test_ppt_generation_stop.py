import pytest
from src.utils.logger import get_logger 
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from f1_helpychat.src.pages.ppt_create_page import PPTCreatePage

logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T143")
def test_ppt_generation_stop(driver):
    """
    PPT 생성 중지 기능 테스트
    - 주제 / 지시사항 입력
    - 생성 → 다시 생성
    - STOP 아이콘 클릭
    - 중지 안내 멘트 노출 확인
    """

    try:
        logger.info("\n==============================")
        logger.info("[TEST START] PPT Generation Stop")

        login(driver, USERNAME1, PASSWORD1)
        logger.info("[STEP] 관리자 로그인 완료")

        ppt_page = PPTCreatePage(driver)

        ppt_page.click_tool_tab()
        ppt_page.click_ppt_tab()
        logger.info("[STEP] PPT 생성 화면 진입")

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

        if not stop_message:
            logger.error("[ASSERT FAIL] 중지 안내 멘트가 노출되지 않음")

        assert stop_message is not None, "중지 안내 멘트가 표시되지 않음"
        assert "요청에 의해 답변 생성을 중지했습니다." in stop_message, \
            "중지 안내 멘트 내용 불일치"
        
    except Exception as e:
        logger.exception("[TEST ERROR] 예외 발생")
        raise
    
    finally:
        logger.info("[TEST END] PPT Generation Stop")
        logger.info("==============================\n")
