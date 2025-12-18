from selenium.webdriver.support import expected_conditions as EC
import logging
from src.pages.CT_page import ClassTemp
from src.utils import login
from src.config import USERNAME5, PASSWORD5
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pytest
import time

#로깅설정하기
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# 다른 입력값
def test_recreate_CT(driver):
    page = ClassTemp(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_CT_tab() 
    
    page.click_sch_lv()
    school_opts = page.get_sch_lvs()
    #print("학교급 옵션:", school_opts)

    driver.find_element(By.XPATH, f"//li[text()='{school_opts[1]}']").click()

    page.click_grade_lv()
    grade_opts = page.get_grade_lvs()
    #print(f"{school_opts[0]} 선택 → 학년:", grade_opts)

    driver.find_element(By.XPATH, f"//li[text()='{grade_opts[0]}']").click()

    page.click_sub()
    sub_opts = page.get_subs()
    #print(f"{grade_opts[0]} 선택 → 과목:", sub_opts)

    driver.find_element(By.XPATH, f"//li[text()='{sub_opts[0]}']").click()

    page.click_time()
    time_opts = page.get_times()
    #print(f"{sub_opts[0]} 선택 → 수업시간:", time_opts)

    driver.find_element(By.XPATH, f"//li[text()='{time_opts[0]}']").click()
    
    page.send_achieve()
    

    if "자동 생성" in driver.page_source:
        btn_create = driver.find_element(By.XPATH,"//button[normalize-space(text())='자동 생성']")
        btn_create.click()
    elif "다시 생성" in driver.page_source:
        btn_recreate = driver.find_element(By.XPATH,"//button[normalize-space(text())='다시 생성']")
        btn_recreate.click()
        modal = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiDialog-root")))
        button_in_modal = WebDriverWait(modal, 10).until(
        EC.element_to_be_clickable((By.XPATH, ".//button[normalize-space(text())='다시 생성']")))
        button_in_modal.click()

    page.wait_generation_complete()

    complete_msg = page.wait_success_message()

    assert len(complete_msg) == 1, "완료 메세지는 하나여야 합니다."