# 새로 고침 혹은 재로그인 시 기존에 입력했던 필드들이 초기화 되는지 확인
from selenium.webdriver.support import expected_conditions as EC
import logging
from src.pages.special_note_page import SpecialNote
from src.utils import login
from src.config import USERNAME4, PASSWORD4
from src.config import USERNAME5, PASSWORD5
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

#로깅설정하기
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# 세부특기 생성 실패 (파일 미첨부)
def test_create_SN_fail_nofile(driver):
    page = SpecialNote(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_SN_tab()
    page.click_sch_lv()
    page.select_cho()
    page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
    page.click_sub()
    page.select_kuk()

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

    assert not page.wait_success_message().is_displayed(), "fail: 첨부파일이 없는데 결과가 생성되었습니다."

    
# 세부특기 생성 실패 (미지원 파일 첨부)
def test_create_SN_fail_wrongfile(driver):
    page = SpecialNote(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_SN_tab()
    page.click_sch_lv()
    page.select_cho()
    page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
    page.click_sub()
    page.select_kuk()

    page.upload_pdf_succes()

    try:
        files = driver.find_elements(By.XPATH, "//input[@type='file']")
        assert len(files) == 0 , "fail: 파일이 첨부되어 있습니다."
    except NoSuchElementException:
        assert True


# 세부특기 생성 실패 (생성 중지)
def test_create_SN_fail_Stop(driver):
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

    page.click_stop_icon()
    stop_message = page.get_stop_message_text()
    assert stop_message is not None
    assert "요청에 의해 답변 생성을 중지했습니다." in stop_message

# 세부특기 생성 실패 (추가 입력란만 테스트)
def test_create_SN_fail_onlyAddInput(driver):
    page = SpecialNote(driver)
    login(driver, USERNAME4, PASSWORD4)
    page.click_tool_tab()
    page.click_SN_tab()
    page.send_add_input()
    
    btn_create = driver.find_element(By.XPATH,"//button[normalize-space(text())='자동 생성']")

    assert not btn_create.is_enabled()



# 대용량 파일이 안 만들어져서 보류
# 세부특기 생성 실패 (대용량 파일 파일 첨부)
def test_create_SN_fail_overfile(driver):
    page = SpecialNote(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_SN_tab()
    page.click_sch_lv()
    page.select_cho()
    page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
    page.click_sub()
    page.select_kuk()

    page.upload_largefile_succes()
    time.sleep(3)

    # try:
    #     files = driver.find_elements(By.XPATH, "//input[@type='file']")
        
    # except NoSuchElementException:
    #     assert True
