# pytest fixture 및 공통 설정 정의
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from src.utils.file_utils import clean_download_dir
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from src.pages.main_page import MainPage
from src.utils import login
from data.config import USERNAME, PASSWORD
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# 테스트용 다운로드 디렉토리
@pytest.fixture
def download_dir():
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    path = os.path.join(PROJECT_ROOT, "downloads")
    os.makedirs(path, exist_ok=True)
    return path

@pytest.fixture
def driver(download_dir):
    """크롬 브라우저를 열고 테스트 후 닫는 pytest fixture"""    
    options = webdriver.ChromeOptions()
    
    # 테스트 시작 전 다운로드 폴더 정리
    clean_download_dir(download_dir)
    
    # 크롬 다운로드 관련 설정
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)  # Chrome 브라우저 열기
    driver.implicitly_wait(5)  # 암묵적 대기: 요소 로딩 최대 5초까지 대기
    yield driver
    driver.delete_all_cookies()
    driver.quit()  # 테스트 완료 후 브라우저 닫기

@pytest.fixture
def logged_in_main_page_setup(driver):
    logger.info("\n[SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USERNAME, PASSWORD)
    logger.info("[SETUP] ✅ 액션: 관리자 로그인 완료")

    main = MainPage(driver)

    return main

@pytest.fixture
def logged_in_driver(driver):
    logger.info("\n[SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USERNAME, PASSWORD)
    logger.info("[SETUP] ✅ 액션: 관리자 로그인 완료")

    MainPage(driver)

    return driver
