from src.pages.account_page import AccountPage
from src.pages.update_page import UpdatePage
import os
import json
from src.utils.logger import get_logger
from pathlib import Path
from src.utils import login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===

base_dir = os.path.dirname(__file__)  # 현재 test_join.py 위치
json_path = Path(__file__).resolve().parents[2] / "data" / "join_data.json"

with open(json_path, "r", encoding="utf-8") as f:
    join_data = json.load(f)

# 탈퇴 테스트
## 해당 테스트는 탈퇴 할 수 있는 계정이 먼저 회원가입 되어 있어야 한다.
'''
[관련TC]
F1HEL-T77 : 탈퇴하기 기능 및 탈퇴 후 로그인 가능 여부 확인
'''
def test_withdraw(driver):
    logger.info("===탈퇴 테스트 시작===")
    account_page = AccountPage(driver)
    setting_page = UpdatePage(driver)
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    user = join_data[0]
    login(driver, user["loginId"], user["password"])
    logger.info("로그인 완료")
    setting_page.go_to_setting()
    logger.info("정보 수정 페이지 활성화(탈퇴)")

    logger.info("탈퇴하는 중입니다 ... ")
    account_page.withdraw_click(user["loginId"])
    logger.info(" 탈퇴가 완료 되었습니다. ")


# 탈퇴하기 테스트를 했던 계정으로 테스트 해야합니다.
def test_withdraw_login(driver):
    logger.info("===탈퇴 후 재로그인 테스트 시작===")
    user = join_data[0]
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    user = join_data[0]
    login(driver, user["loginId"], user["password"])
    expected_msg = user["expected_msg_aft_wd"]

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//*[contains(text(), '{expected_msg}')]")))

    assert user["expected_msg_aft_wd"] in driver.page_source
