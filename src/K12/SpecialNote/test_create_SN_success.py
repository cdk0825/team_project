from selenium.webdriver.support import expected_conditions as EC
import logging
from src.pages.special_note_page import SpecialNote
from src.utils import login
from src.config import USERNAME5, PASSWORD5
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
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
    page = SpecialNote(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_SN_tab()
    page.click_sch_lv()
    page.select_cho()
    page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
    page.click_sub()
    page.select_kuk()
    page.upload_exel_succes()

    page.create_btn()

        
    assert page.result_download().is_enabled()
