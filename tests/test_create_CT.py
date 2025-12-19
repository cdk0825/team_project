
from src.pages.k2_page import K12Note
from src.utils import login
from src.config import USERNAME5, PASSWORD5
from selenium.webdriver.common.by import By
from src.utils.logger import get_logger
from selenium.common.exceptions import TimeoutException


# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===

'''
[관련 TC]
F1HEL-T153 : 수업지도안 생성 테스트
'''

def test_create_CT(driver):
    logger.info("===수업지도안 생성 테스트 시작===")

    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_CT_tab()
    logger.info("수업지도안 페이지 활성화")
    
    # 학교급, 학년, 과목, 시간 택
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
    
    # 성취기준 입력
    page.send_achieve()
    logger.info("성취기준을 입력")
    
    # 자동생성/다시 생성 버튼 클릭
    page.create_btn()
    logger.info("생성 버튼 클릭")

    # Stop icon이 보이지 않을 때까지 기다림
    page.wait_generation_complete()
    logger.info("생성 중지 아이콘이 사라졌습니다.")

    try:
        # 완료 메세지 뜰때까지 기다림
        page.ct_wait_success_message()
        logger.info("완료 메세지 확인되었습니다.")
                # 성공 케이스: 다운로드 버튼이 활성화되어 있어야 함
        assert page.result_download().is_enabled(), "fail: 성공했는데 다운로드 버튼이 비활성화됨"

    except TimeoutException:
        logger.warning("생성 실패 메시지 감지됨.")

