# 새로 고침 혹은 재로그인 시 기존에 입력했던 필드들이 초기화 되는지 확인
from selenium.webdriver.support import expected_conditions as EC
from src.pages.k2_page import K12Note
from src.utils import login
from data.config import USERNAME4, PASSWORD4
from data.config import USERNAME5, PASSWORD5
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from src.utils.logger import get_logger

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===


'''
[관련 TC]
F1HEL-T157 : 생성 실패 테스트 (파일 미첨부)
F1HEL-T172 : 생성 실패 테스트 (파일 용량초과)
F1HEL-T174 : 생성 실패 테스트 (미지원 파일 첨부)
F1HEL-T177 : 생성 실패 테스트 (추가입력만 입력)
F1HEL-T233 : 생성 중지 테스트
'''

# 세부특기 생성 실패 (파일 미첨부)
def test_create_SN_fail_nofile(driver):
    logger.info("===세부 특기사항 생성 실패 테스트 시작(파일 미첨부)===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_SN_tab()
    logger.info("세부특기사항 페이지 활성화")

    page.click_sch_lv()
    page.select_cho()
    page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
    page.click_sub()
    page.select_kuk()

    logger.info("파일 미첨부")

    page.create_btn()

    assert not page.sn_wait_success_message().is_displayed(), "fail: 첨부파일이 없는데 결과가 생성되었습니다."

    
# 세부특기 생성 실패 (미지원 파일 첨부)
def test_create_SN_fail_wrongfile(driver):
    logger.info("===세부 특기사항 생성 실패 테스트 시작 (미지원 파일 첨부)===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_SN_tab()
    logger.info("세부특기사항 페이지 활성화")

    page.click_sch_lv()
    page.select_cho()
    page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
    page.click_sub()
    page.select_kuk()

    page.upload_pdf_succes()
    logger.info("pdf 파일을 첨부")

    try:
        files = driver.find_elements(By.XPATH, "//input[@type='file']")
        assert len(files) == 0 , "fail: 파일이 첨부되어 있습니다."
    except NoSuchElementException:
        assert True


# 세부특기 생성 실패 (생성 중지)
def test_create_SN_fail_Stop(driver):
    logger.info("===세부 특기사항 생성 중지 테스트 시작===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_SN_tab()
    logger.info("세부특기사항 페이지 활성화")

    page.click_sch_lv()
    page.select_cho()
    page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
    page.click_sub()
    page.select_kuk()

    page.SN_upload_exel_succes()
    logger.info("엑셀 파일 첨부")
    
    page.create_btn()

    page.click_stop_icon()
    logger.info("정지 아이콘 클릭")
    stop_message = page.get_stop_message_text()

    assert stop_message is not None
    assert "요청에 의해 답변 생성을 중지했습니다." in stop_message

# 세부특기 생성 실패 (추가 입력란만 테스트)
def test_create_SN_fail_onlyAddInput(driver):
    logger.info("===세부 특기사항 생성 실패 테스트 (추가 입력만 입력)===")
    page = K12Note(driver)
    login(driver, USERNAME4, PASSWORD4)
    page.click_tool_tab()
    page.click_SN_tab()
    page.send_add_input()
    
    btn_create = driver.find_element(By.XPATH,"//button[normalize-space(text())='자동 생성']")

    assert not btn_create.is_enabled()



# 대용량 파일이 안 만들어져서 보류
# 영상 파일을 xls 변환 실패
# 세부특기 생성 실패 (대용량 파일 파일 첨부)
# def test_create_SN_fail_overfile(driver):
#     page = K12Note(driver)
#     login(driver, USERNAME5, PASSWORD5)
#     page.click_tool_tab()
#     page.click_SN_tab()
#     page.click_sch_lv()
#     page.select_cho()
#     page.wait.until(EC.invisibility_of_element_located(page.LISTBOX))
#     page.click_sub()
#     page.select_kuk()
#     page.upload_largefile_succes()

    # try:
    #     files = driver.find_elements(By.XPATH, "//input[@type='file']")
        
    # except NoSuchElementException:
    #     assert True
