from selenium.webdriver.support import expected_conditions as EC
from src.pages.k2_page import K12Note
from src.utils import login
from src.config import USERNAME5, PASSWORD5
from src.utils.logger import get_logger

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===

# 세부 특기사항 생성 성공
'''
[관련TC]
F1HEL-T145 : 세부 특기사항 생성 테스트
'''
def test_SN_succes(driver):
    logger.info("===세부 특기사항 생성 성공 테스트 시작===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_SN_tab() 
    logger.info("세부특기사항 페이지 활성화")

    page.click_sch_lv()
    page.select_cho()
    page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
    page.click_sub()
    page.select_kuk()
    logger.info("각 필드 값 입력 완료")

    page.SN_upload_exel_succes()
    logger.info("엑셀 파일 첨부")

    page.create_btn()
    logger.info("생성 버튼 클릭")
        
    assert page.result_download().is_enabled()
