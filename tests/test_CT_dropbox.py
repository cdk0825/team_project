
from src.pages.k2_page import K12Note
from src.utils import login
from src.config import USERNAME5, PASSWORD5
from selenium.webdriver.common.by import By
import pytest
from src.utils.logger import get_logger

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===
'''
[관련TC]
F1HEL-T154 : 드롭박스 정상 출력 확인
'''
# 드롭박스 텍스트 확인
@pytest.mark.parametrize("school", ["초등", "중등", "고등"])
def test_CT_dropbox(driver, school):
    logger.info("===세부 특기사항 드롭박스 옵션 확인 테스트 시작===")
    page = K12Note(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_CT_tab()
    logger.info("세부 특기사항 페이지 활성화")

    page.click_sch_lv()
    school_opts = page.get_sch_lvs()
    driver.find_element(By.XPATH, f"//li[text()='{school}']").click()
    print("학교급 옵션:", school_opts)
    logger.info("학교급 목록이 출력되었습니다.")

    page.click_grade_lv()
    grade_opts = page.get_grade_lvs()
    driver.find_element(By.XPATH, f"//li[text()='{grade_opts[0]}']").click()
    print(f"{school_opts[0]} 선택 → 학년:", grade_opts)
    logger.info("학년별 목록이 출력되었습니다.")

    page.CT_click_sub()
    sub_opts = page.CT_get_subs()
    driver.find_element(By.XPATH, f"//li[text()='{sub_opts[0]}']").click()
    print(f"{grade_opts[0]} 선택 → 과목:", sub_opts)
    logger.info("과목별 목록이 출력되었습니다.")

    page.click_time()
    time_opts = page.get_times()
    print(f"{sub_opts[0]} 선택 → 수업시간:", time_opts)
    logger.info("수업시간 목록이 출력되었습니다.")

    assert school_opts, "학교급 옵션이 없음"
    assert grade_opts, "학년 옵션이 없음"
    assert sub_opts, "과목 옵션이 없음"
    assert time_opts, "수업시간 옵션이 없음"


