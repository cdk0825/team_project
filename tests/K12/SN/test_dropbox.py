from selenium.webdriver.support import expected_conditions as EC
from src.pages.k2_page import K12Note
from src.utils import login
from f1_helpychat.data.config import USERNAME5, PASSWORD5
from selenium.webdriver.common.by import By
from src.utils.logger import get_logger

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===
'''
F1HEL-T146 : 세부 특기사항 드롭박스 확인 테스트
'''

# 드롭박스 리스트 확인하기
def test_specialnote_dropbox(driver):
    logger.info("===세부 특기사항 드롭박스 옵션 확인 테스트 시작===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_SN_tab()
    logger.info("세부특기사항 페이지 활성화")

    page.click_sch_lv()
    page.get_sch_lvs()

    for text,element in page.get_sch_lvs():
        logger.info(f"학교급 선택: {text}")
        element = page.driver.find_element(
        By.XPATH,f"//li[@role='option' and contains(text(), '{text}')]")
        element.click()
        school_texts = page.get_sch_lvs
        page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
        page.click_sub()
        sub_texts = page.get_subs()
        logger.info(f"{text} 과목 리스트: {sub_texts}")
        page.close_listbox()
        page.click_sch_lv()

    assert school_texts, "학교급 옵션이 없음"
    assert sub_texts, "과목 옵션이 없음"
