# 새로 고침 혹은 재로그인 시 기존에 입력했던 필드들이 초기화 되는지 확인
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
[관련 TC]
F1HEL-T224 : 결과 생성 후 로그아웃 -> 재로그인 시 입력된 내용 및 결과가 초기화 되어있는지 확인
'''

# 세부특기 초기화 확인
def test_SN_clear(driver):
    logger.info("===세부 특기사항 초기화 테스트 시작===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_SN_tab()
    logger.info("세부 특기사항 페이지 활성화")

    page.click_sch_lv()
    page.select_cho()
    page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
    page.click_sub()
    page.select_kuk()
    page.SN_upload_exel_succes()

    page.create_btn()

    page.wait_generation_complete()
    page.sn_wait_success_message()
    page.profile_click()

    page.logout()
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(PASSWORD5)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    page.click_tool_tab()
    page.click_SN_tab()

    assert page.sch_lv() == "학교급을 선택해주세요.", "fail: 학교급이 이미 선택되어 있습니다."
    assert page.sub_lv() == "과목을 선택해주세요." , "fail: 과목이 이미 선택되어 있습니다." 
    assert not page.btn_recreate().is_enabled(), "fail: 다시 생성 버튼이 활성화 되어 있습니다."
    assert page.sn_wait_success_message(), "fail: 이미 생성된 결과가 있습니다."