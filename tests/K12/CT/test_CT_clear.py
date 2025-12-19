from src.pages.k2_page import K12Note
from src.utils import login
from data.config import USERNAME5, PASSWORD5
from selenium.webdriver.common.by import By
from src.utils.logger import get_logger

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===

def test_CT_clear(driver):
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_CT_tab() 
    logger.info("세부 특기사항 페이지 활성화")
    
    page.click_sch_lv()
    school_opts = page.get_sch_lvs()
    driver.find_element(By.XPATH, f"//li[text()='{school_opts[0]}']").click()
    logger.info(f'"{school_opts[0]}"를 선택했습니다.')

    page.click_grade_lv()
    grade_opts = page.get_grade_lvs()
    driver.find_element(By.XPATH, f"//li[text()='{grade_opts[0]}']").click()
    logger.info(f'"{grade_opts[0]}"를 선택했습니다.')

    page.CT_click_sub()
    sub_opts = page.CT_get_subs()
    driver.find_element(By.XPATH, f"//li[text()='{sub_opts[0]}']").click()
    logger.info(f'"{sub_opts[0]}"를 선택했습니다.')

    page.click_time()
    time_opts = page.get_times()
    driver.find_element(By.XPATH, f"//li[text()='{time_opts[0]}']").click()
    logger.info(f'"{time_opts[0]}"를 선택했습니다.')

    page.send_achieve()
    
    page.create_btn()

    page.wait_generation_complete()
    page.ct_wait_success_message()

    # 로그아웃 과정
    page.profile_click()
    page.logout()
    logger.info("로그아웃 중입니다 ... ")

    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(PASSWORD5)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    logger.info("재로그인 중입니다 ... ")

    page.click_tool_tab()
    page.click_CT_tab()
    logger.info("초기화 되었는지 확인 중...")

    assert page.sch_lv_txt() == "학교급을 선택해주세요.", "fail: 학교급이 이미 선택되어 있습니다."
    assert page.grade_lv_txt() == "학년을을 선택해주세요.", "fail: 학년이 이미 선택되어 있습니다."
    assert page.sub_lv_txt() == "과목을 선택해주세요." , "fail: 과목이 이미 선택되어 있습니다." 
    assert page.time_txt() == "시간을 입력해주세요." , "fail: 시간이 이미 입력되어 있습니다." 
    assert not page.btn_recreate.is_displayed(), "fail: 다시 생성 버튼이 활성화 되어 있습니다."
    assert page.ct_wait_success_message(), "fail: 이미 생성된 결과가 있습니다."