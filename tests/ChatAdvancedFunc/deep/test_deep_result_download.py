import os
import pytest
from src.utils import login
from src.utils.logger import get_logger 
from data.config import USERNAME1, PASSWORD1
from src.pages.deep_create_page import DEEPCreatePage
from src.utils.file_utils import wait_for_download
from selenium.webdriver.support import expected_conditions as EC

logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T130") 
@pytest.mark.parametrize(
    "download_type, expected_ext",
    [
        ("markdown", ".md"),
        ("hwp", ".hwp"),
    ]
)
def test_deep_result_download_file_extension(driver, download_dir, download_type, expected_ext):
    """
    심층조사 결과 다운로드 파일 확장자 검증
    - 마크다운 다운로드 → .md
    - HWP 파일 다운로드 → .hwp
    """

    logger.info("\n==============================")
    logger.info(f"[TEST START] DEEP Result Download ({expected_ext})")
    
    try:
        login(driver, USERNAME1, PASSWORD1)
        logger.info("[STEP] 관리자 로그인 완료")

        deep_page = DEEPCreatePage(driver)

        deep_page.click_tool_tab()
        deep_page.click_deep_tab()
        logger.info("[STEP] 심층 조사 탭 진입")

        deep_page.clear_inputs()
        deep_page.enter_topic("AI 모델의 성능 비교")
        deep_page.enter_instruction("최신 GPT, Gemini 모델 차이를 정리하라.")
        logger.info("[STEP] 입력 완료")

        deep_page.click_create()
        deep_page.click_regenerate()
        logger.info("[STEP] 생성")

        deep_page.wait_generation_complete()
        assert deep_page.wait_success_message().is_displayed()
        logger.info("[ASSERT PASS] 생성 완료 확인")

        # 다운로드 시작
        deep_page.click_download_button()
        logger.info("[STEP] 다운받기 버튼 클릭")

        if download_type == "markdown":
            deep_page.wait.until(
                EC.element_to_be_clickable(deep_page.MARKDOWN_ITEM)
            ).click()
            logger.info("[STEP] 마크다운 다운로드 클릭")

        elif download_type == "hwp":
            deep_page.wait.until(
                EC.element_to_be_clickable(deep_page.HWPFILE_ITEM)
            ).click()
            logger.info("[STEP] HWP 파일 다운로드 클릭")

        # 다운로드 완료 대기
        # .md 또는 .hwp처럼 expected_ext가 붙은 파일이 생기면
        # → 다운로드 완료로 판단하고 파일명 리턴
        downloaded_file = wait_for_download(download_dir, expected_ext)
        logger.info(f"[INFO] 다운로드 파일: {downloaded_file}")
        
        # 파일명을 이름/확장자로 분리 
        _, ext = os.path.splitext(downloaded_file)
        logger.info(f"[ASSERT] 파일 확장자: {ext}")
        
        if ext != expected_ext:
            logger.error(
                f"[ASSERT FAIL] 파일 확장자 불일치 "
                f"(expect={expected_ext}, actual={ext})"
            )
        assert ext == expected_ext

        logger.info(f"[ASSERT PASS] 다운로드 파일 확장자 검증 성공 ({expected_ext})")
    
    except Exception:
      logger.exception("[TEST ERROR] 테스트 중 예외 발생")
      raise

    finally:
        logger.info(f"[TEST END] DEEP Result Download ({expected_ext})")
        logger.info("==============================\n")
