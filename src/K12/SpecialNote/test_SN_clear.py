# 새로 고침 혹은 재로그인 시 기존에 입력했던 필드들이 초기화 되는지 확인
from selenium.webdriver.support import expected_conditions as EC
import logging
from src.pages.special_note_page import SpecialNote
from src.utils import login
from src.config import USERNAME5, PASSWORD5
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

#로깅설정하기
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# 세부특기 생성 성공
def test_SN_clear(driver):
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
    page.wait_success_message()
    page.profile_click()
    page.logout()
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(PASSWORD5)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    page.click_tool_tab()
    page.click_SN_tab()

    assert page.sch_lv() == "학교급을 선택해주세요.", "fail: 학교급이 이미 선택되어 있습니다."
    assert page.sub_lv() == "과목을 선택해주세요." , "fail: 과목이 이미 선택되어 있습니다." 
    assert not btn_recreate.is_displayed(), "fail: 다시 생성 버튼이 활성화 되어 있습니다."
    assert page.wait_success_message(), "fail: 이미 생성된 결과가 있습니다."