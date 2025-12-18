from selenium.webdriver.support import expected_conditions as EC
import logging
from src.pages.special_note_page import SpecialNote
from src.utils import login
from src.config import USERNAME5, PASSWORD5
import pytest
import os
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import ActionChains


#로깅설정하기
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# 드롭박스 리스트 확인하기
def test_specialnote_dropbox(driver):
    page = SpecialNote(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_SN_tab()
    page.click_sch_lv()
    page.get_sch_lvs()

    for text,element in page.get_sch_lvs():
        print(f"학교급 선택: {text}")
        element = page.driver.find_element(
        By.XPATH,f"//li[@role='option' and contains(text(), '{text}')]")
        element.click()
        page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
        page.click_sub()
        sub_texts = page.get_subs()
        print(f"{text} 과목 리스트: {sub_texts}")
        page.close_listbox()
        page.click_sch_lv()