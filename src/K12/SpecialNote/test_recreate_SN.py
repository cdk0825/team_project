from selenium.webdriver.support import expected_conditions as EC
from src.pages.k2_page import K12Note
from src.utils import login
from src.config import USERNAME5, PASSWORD5
from src.utils.logger import get_logger

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===

'''
[관련 TC]
F1HEL-T228 : 다시 생성 테스트 (다른 입력값)
'''

# 세부특기 생성 성공
def test_SN_succes(driver):
    logger.info("===세부 특기사항 다시 생성 테스트 시작===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_SN_tab()
    logger.info("세부 특기사항 페이지 활성화")

    page.click_sch_lv()
    page.select_joong()
    page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
    page.click_sub()
    page.select_soo()
    logger.info("필드 값 입력")

    page.SN_upload_exel_succes()
    logger.info("엑셀 첨부")

    page.create_btn()
    logger.info("생성 버튼 클릭")
    # btn_recreate = driver.find_element(By.XPATH,"//button[normalize-space(text())='다시 생성']")
    # btn_recreate.click()
    # modal = WebDriverWait(driver, 10).until(
    #         EC.visibility_of_element_located((By.CSS_SELECTOR, ".MuiDialog-root")))
    # button_in_modal = WebDriverWait(modal, 10).until(
    # EC.element_to_be_clickable((By.XPATH, ".//button[normalize-space(text())='다시 생성']")))
    # button_in_modal.click()

    page.wait_generation_complete()

    complete_msg = page.sn_wait_success_message()


    # complete_msg = driver.find_elements(By.XPATH,
    # "//p[contains(text(), '입력하신 내용 기반으로 세부 특기사항을 생성했습니다.')]"
    # )
    assert len(complete_msg) == 1, "완료 메세지는 하나여야 합니다."
    assert len(page.result_download()) ==1, "결과값은 하나여야 합니다."
