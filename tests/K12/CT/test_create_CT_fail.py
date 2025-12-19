
from src.pages.k2_page import K12Note
from src.utils import login
from f1_helpychat.data.config import USERNAME4, PASSWORD4
from f1_helpychat.data.config import USERNAME5, PASSWORD5
from selenium.webdriver.common.by import By
import pytest
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from src.utils.logger import get_logger

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===
'''
[관련TC]
F1HEL-T235 : 생성 실패 (생성 중지)
F1HEL-T176 : 생성 실패 (추가입력만 입력)
F1HEL-T155 : 생성 실패 (성취기준 미입력)
'''
# 생성 중지
def test_create_CT_stop(driver):
    logger.info("===생성 중지 테스트 시작===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_CT_tab() 
    logger.info("세부 특기사항 페이지 활성화")
    
    # 각 필드 선택
    page.click_sch_lv()
    school_opts = page.get_sch_lvs()
    driver.find_element(By.XPATH, f"//li[text()='{school_opts[0]}']").click()
    logger.info("학교급 필드 선택 완료")

    page.click_grade_lv()
    grade_opts = page.get_grade_lvs()
    driver.find_element(By.XPATH, f"//li[text()='{grade_opts[0]}']").click()
    logger.info("학년별 필드 선택 완료")

    page.CT_click_sub()
    sub_opts = page.CT_get_subs()
    driver.find_element(By.XPATH, f"//li[text()='{sub_opts[0]}']").click()
    logger.info("과목별 필드 선택 완료")

    page.click_time()
    time_opts = page.get_times()
    driver.find_element(By.XPATH, f"//li[text()='{time_opts[0]}']").click()
    logger.info("시간별 필드 선택 완료")
    
    page.send_achieve()
    logger.info("성취기준 입력 완료")

    # 자동생성/다시 생성 버튼 클릭
    page.create_btn()
    logger.info("생성 버튼 클릭")

    # 생성 중지 클릭
    page.click_stop_icon()
    logger.info("생성 중지 버튼 클릭")

    stop_message = page.get_stop_message_text()
    logger.info("생성 중지 메세지 확인 완료")

    assert stop_message is not None
    assert "요청에 의해 답변 생성을 중지했습니다." in stop_message


# 수업지도안 생성 실패 (추가 입력란만 테스트)
def test_onlyAddInput(driver):
    logger.info("===추가 입력만 입력 후 생성 테스트 시작===")
    page = K12Note(driver)
    login(driver, USERNAME4, PASSWORD4)
    page.click_tool_tab()
    page.click_CT_tab()
    logger.info("세부 특기사항 페이지 활성화")

    page.send_add_input()
    logger.info("추가 입력란 작성")
    time.sleep(3)
    
    btn_create = driver.find_element(By.XPATH,"//button[normalize-space(text())='자동 생성']")

    # 자동 생성 버튼이 활성화 되면 fail
    assert not btn_create.is_enabled(), "fail: 자동 생성 버튼이 활성화 되었습니다."


# 성취기준 미입력
def test_no_achieve(driver):
    logger.info("===성취기준 미입력 후 생성 테스트 시작===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_CT_tab()
    logger.info("세부 특기사항 페이지 활성화")
    
    page.click_sch_lv()
    school_opts = page.get_sch_lvs()
    driver.find_element(By.XPATH, f"//li[text()='{school_opts[0]}']").click()
    logger.info("학교급 필드 선택 완료")

    page.click_grade_lv()
    grade_opts = page.get_grade_lvs()
    driver.find_element(By.XPATH, f"//li[text()='{grade_opts[0]}']").click()
    logger.info("학년별 필드 선택 완료")

    page.click_sub()
    sub_opts = page.get_subs()
    driver.find_element(By.XPATH, f"//li[text()='{sub_opts[0]}']").click()
    logger.info("과목별 필드 선택 완료")

    page.click_time()
    time_opts = page.get_times()
    driver.find_element(By.XPATH, f"//li[text()='{time_opts[0]}']").click()
    logger.info("시간별 필드 선택 완료")


    ele = page.ele_achieve()
    if ele.get_attribute("value"):   # 입력값이 있으면
        ele.send_keys(Keys.CONTROL, "a")  # 전체 선택
        ele.send_keys(Keys.DELETE)        # 삭제
    else:
        print("성취기준 입력된게 없습니다.")
    logger.info("성취기준 필드 값 삭제")

    page.create_btn()

    # 이 코드에서 예외가 발생하면 성공
    # stop icon NoSuchElement 예외 발생 시 성공
    with pytest.raises(NoSuchElementException):
        page.wait_generation_complete()

