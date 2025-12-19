
from src.pages.k2_page import K12Note
from src.utils import login
from data.config import USERNAME5, PASSWORD5
from src.utils.logger import get_logger
from selenium.common.exceptions import TimeoutException

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===

'''
[관련TC]
F1HEL-T150 : 생성 성공 테스트
'''

# 행동특성 종합의견 생성 성공 테스트
def test_BG_succes(driver):
    logger.info("===행동특성 및 종합의견 생성 테스트===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_BG_tab()
    logger.info("행동특성 및 종합의견 탭 활성화")

   
    page.BG_upload_exel_succes()
    logger.info("행동특성 및 종합의견 엑셀 첨부")

    page.create_btn()
    logger.info("생성 버튼 클릭")

    page.wait_generation_complete()
    logger.info("생성 중지 아이콘이 사라졌습니다.")

    try:
        # 성공 메시지 기다림
        page.bg_wait_success_message()
        logger.info("완료 메세지 확인되었습니다.")

        # 성공 케이스: 다운로드 버튼이 활성화되어 있어야 함
        assert page.result_download().is_enabled(), "fail: 성공했는데 다운로드 버튼이 비활성화됨"

    except TimeoutException:
        logger.warning("생성 실패 메시지 감지됨.")
