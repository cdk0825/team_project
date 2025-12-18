from selenium.webdriver.support import expected_conditions as EC
import logging
from src.pages.CT_page import ClassTemp
from src.utils import login
from src.config import USERNAME5, PASSWORD5
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pytest


#로깅설정하기
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

@pytest.mark.parametrize("school", ["초등", "중등", "고등"])
def test_CT_dropbox(driver, school):
    page = ClassTemp(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.click_tool_tab()
    page.click_CT_tab()

    page.click_sch_lv()
    school_opts = page.get_sch_lvs()
    print("학교급 옵션:", school_opts)


    driver.find_element(By.XPATH, f"//li[text()='{school}']").click()


    page.click_grade_lv()
    grade_opts = page.get_grade_lvs()
    print(f"{school} 선택 → 학년:", grade_opts)

    driver.find_element(By.XPATH, f"//li[text()='{grade_opts[0]}']").click()

    page.click_sub()
    sub_opts = page.get_subs()
    print(f"{grade_opts[0]} 선택 → 과목:", sub_opts)

    driver.find_element(By.XPATH, f"//li[text()='{sub_opts[0]}']").click()

    page.click_time()
    time_opts = page.get_times()
    print(f"{sub_opts[0]} 선택 → 수업시간:", time_opts)

    assert school_opts, "학교급 옵션이 없음"
    assert grade_opts, "학년 옵션이 없음"
    assert sub_opts, "과목 옵션이 없음"
    assert time_opts, "수업시간 옵션이 없음"


