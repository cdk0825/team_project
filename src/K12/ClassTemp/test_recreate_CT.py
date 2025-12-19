
from src.pages.k2_page import K12Note
from src.utils import login
from src.config import USERNAME5, PASSWORD5
from selenium.webdriver.common.by import By
from src.utils.logger import get_logger

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===
'''
[관련 TC]
F1HEL-T232 : 다시 생성 테스트 (다른 입력값)
'''
# 다른 입력값
def test_recreate_CT(driver):
    logger.info("===세부 특기사항 생성 테스트 시작===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_CT_tab() 
    logger.info("세부 특기사항 페이지 활성화")
    
    # 학교급, 학년, 과목, 시간 택
    page.click_sch_lv()
    school_opts = page.get_sch_lvs()
    driver.find_element(By.XPATH, f"//li[text()='{school_opts[1]}']").click()
    logger.info(f'"{school_opts[1]}"를 선택했습니다.')

    page.click_grade_lv()
    grade_opts = page.get_grade_lvs()
    driver.find_element(By.XPATH, f"//li[text()='{grade_opts[1]}']").click()
    logger.info(f'"{grade_opts[1]}"를 선택했습니다.')

    page.CT_click_sub()
    sub_opts = page.CT_get_subs()
    driver.find_element(By.XPATH, f"//li[text()='{sub_opts[1]}']").click()
    logger.info(f'"{sub_opts[1]}"를 선택했습니다.')

    page.click_time()
    time_opts = page.get_times()
    driver.find_element(By.XPATH, f"//li[text()='{time_opts[1]}']").click()
    logger.info(f'"{time_opts[1]}"를 선택했습니다.')

    page.send_achieve()
    
    page.create_btn()

    page.wait_generation_complete()

    complete_msg = page.ct_wait_success_message()

    assert len(complete_msg) == 1, "완료 메세지는 하나여야 합니다."