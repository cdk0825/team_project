from selenium.webdriver.support import expected_conditions as EC
import logging
from src.pages.CT_page import ClassTemp
from src.utils import login
from src.config import USERNAME4, PASSWORD4
from src.config import USERNAME5, PASSWORD5
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pytest
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


#로깅설정하기
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# 생성 중지
def test_create_CT_stop(driver):
    page = ClassTemp(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_CT_tab() 
    
    page.click_sch_lv()
    school_opts = page.get_sch_lvs()
    #print("학교급 옵션:", school_opts)

    driver.find_element(By.XPATH, f"//li[text()='{school_opts[0]}']").click()

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

    page.click_stop_icon()
    time.sleep(3)
    stop_message = page.get_stop_message_text()
    assert stop_message is not None
    assert "요청에 의해 답변 생성을 중지했습니다." in stop_message


# 수업지도안 생성 실패 (추가 입력란만 테스트)
def test_onlyAddInput(driver):
    page = ClassTemp(driver)
    login(driver, USERNAME4, PASSWORD4)
    page.click_tool_tab()
    page.click_CT_tab() 
    page.send_add_input()
    time.sleep(3)
    
    btn_create = driver.find_element(By.XPATH,"//button[normalize-space(text())='자동 생성']")

    assert not btn_create.is_enabled()



# 성취기준 미입력
def test_no_achieve(driver):
    page = ClassTemp(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_CT_tab() 
    
    page.click_sch_lv()
    school_opts = page.get_sch_lvs()
    #print("학교급 옵션:", school_opts)

    driver.find_element(By.XPATH, f"//li[text()='{school_opts[0]}']").click()

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

    ele = page.ele_achieve()
    if ele.get_attribute("value"):   # 입력값이 있으면
        ele.send_keys(Keys.CONTROL, "a")  # 전체 선택
        ele.send_keys(Keys.DELETE)        # 삭제
    else:
        print("성취기준 입력된게 없습니다.")

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

    # 이 코드에서 예외가 발생하면 성공
    with pytest.raises(NoSuchElementException):
        page.wait_generation_complete()

