
from src.pages.k2_page import K12Note
from src.utils import login
from data.config import USERNAME4, PASSWORD4
from data.config import USERNAME5, PASSWORD5
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from src.utils.logger import get_logger

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===

'''
[관련TC]
F1HEL-T156 : 생성 실패 테스트 (파일 미업로드)
F1HEL-T175 : 생성 실패 테스트 (미지원 파일 첨부)
F1HEL-T223 : 생성 실패 테스트 (추가 입력만 입력)
F1HEL-T234 : 생성 실패 테스트 (생성 중지)
'''

# 행동특성 종합의견 생성 실패(파일 미첨부)
def test_BG_nofile(driver):
    logger.info("===행동특성 및 종합의견 생성 실패 파일 미첨부 테스트===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_BG_tab()
    logger.info("행동특성 및 종합의견 탭 활성화")

    logger.info("파일을 첨부 하지 않았습니다.")
    page.create_btn()

    assert not page.result_download().is_enabled(), "fail: 첨부파일이 없는데 결과가 생성되었습니다."


    # 행동특성 종합의견 생성 실패(미지원 파일 첨부)
def test_BG_wrongfile(driver):
    logger.info("===행동특성 및 종합의견 생성 실패 미지원 파일 첨부 테스트===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_BG_tab()
    logger.info("행동특성 및 종합의견 탭 활성화")

    page.upload_pdf_succes()
    logger.info("pdf 파일 첨부")

    try:
        files = driver.find_elements(By.XPATH, "//input[@type='file']")
        assert len(files) == 0 , "fail: 파일이 첨부되어 있습니다."
    except NoSuchElementException:
        assert True

# 생성중지
def test_BG_stop(driver):
    logger.info("===행동특성 및 종합의견 생성 중지 테스트===")

    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_BG_tab()
    logger.info("행동특성 및 종합의견 탭 활성화")

    page.BG_upload_exel_succes()
    logger.info("엑셀 파일 첨부")

    page.create_btn()

    page.click_stop_icon()
    stop_message = page.get_stop_message_text()

    assert stop_message is not None
    assert "요청에 의해 답변 생성을 중지했습니다." in stop_message

# BG 생성 실패 (추가 입력란만 테스트)
def test_onlyAddInput(driver):
    logger.info("===행동특성 및 종합의견 추가 입력란만 입력 테스트===")
    page = K12Note(driver)
    login(driver, USERNAME4, PASSWORD4)
    page.click_tool_tab()
    page.click_BG_tab()
    logger.info("행동특성 및 종합의견 탭 활성화")

    logger.info("파일을 첨부 하지 않았습니다.")

    page.send_add_input()
    logger.info("추가 입력란만 입력했습니다.")

    btn_create = driver.find_element(By.XPATH,"//button[normalize-space(text())='자동 생성']")

    assert not btn_create.is_enabled()