import pytest
from src.utils import login
from src.utils.logger import get_logger 
from f1_helpychat.data.config import USERNAME1, PASSWORD1
from f1_helpychat.src.pages.deep_create_page import DEEPCreatePage

logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T126") 
def test_success_create(driver):
    """
    DEEP 정상 생성 테스트
    - 주제, 지시사항 입력
    - 생성 → 다시 생성
    - 생성 결과 확인 (생성메시지, 다운받기)
    """
    
    logger.info("\n==============================")
    logger.info("[TEST START] DEEP Success Create")
    
    try:
        login(driver, USERNAME1, PASSWORD1)
        logger.info("[STEP] 관리자 로그인 완료")
        
        deep_page = DEEPCreatePage(driver)

        deep_page.click_tool_tab()
        deep_page.click_deep_tab()
        logger.info("[STEP] 심층 조사 화면 진입")

        deep_page.clear_inputs()
        logger.info("[STEP] 입력값 초기화")

        deep_page.enter_topic("AI 모델의 성능 비교")
        deep_page.enter_instruction(
            "최신 GPT, Gemini 모델의 차이를 표로 정리하라. "
            "참고한 근거를 단계별로 제시하라."
        )
        logger.info("[STEP] 주세/지시사항 입력 완료")

        is_enabled = deep_page.is_create_button_enabled()
        logger.info(f"[ASSERT] 생성 버튼 활성화 여부: {is_enabled}")
        
        if not is_enabled:
            logger.error("[ASSERT FAIL] 생성 버튼이 비활성 상태")
        assert is_enabled is True, "생성 버튼이 활성화되지 않음"

        deep_page.click_create()
        deep_page.click_regenerate()
        logger.info("[STEP] 생성 -> 다시 생성 클릭")

        logger.info("[WAIT] 심층 조사 생성 완료 대기 (STOP 아이콘 사라질 때까지)")
        deep_page.wait_generation_complete()

        logger.info("[ASSERT] 생성 완료 메시지 확인")
        assert deep_page.wait_success_message().is_displayed()
        logger.info("[ASSERT PASS] 생성 완료 메시지 노출")        

        is_download_displayed = deep_page.is_download_button_displayed()
        logger.info(f"[ASSERT] 다운받기 버튼 표시 여부: {is_download_displayed}")
        
        if not is_download_displayed:
            logger.error("[ASSERT FAIL] 다운로드 버튼 미노출")
        assert is_download_displayed is True, "다운받기 버튼이 표시되지 않음"
        
        deep_page.click_download_button()
        logger.info("[STEP] 다운받기 버튼 클릭")

        assert deep_page.is_markdown_item_displayed() is True
        logger.info("[ASSERT PASS] 마크다운 다운로드 항목 노출")

        assert deep_page.is_hwp_item_displayed() is True
        logger.info("[ASSERT PASS] HWP 파일 다운로드 항목 노출")

    except Exception:
      logger.exception("[TEST ERROR] 테스트 중 예외 발생")
      raise

    finally:
        logger.info("[TEST END] DEEP Success Create")
        logger.info("==============================\n")