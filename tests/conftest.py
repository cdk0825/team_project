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
import shutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# 세션 시작 시 딱 한 번 실행되어 폴더를 초기화합니다.
@pytest.fixture(scope="session", autouse=True)
def clean_screenshots():
    screenshot_dir = "screenshots"
    if os.path.exists(screenshot_dir):
        print(f"\n🧹 기존 스크린샷 삭제 중: {screenshot_dir}")
        shutil.rmtree(screenshot_dir)
    os.makedirs(screenshot_dir, exist_ok=True)
    
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
    
    # 1. 공통으로 사용할 기본 prefs 사전 생성
    # 다운로드 설정 등을 기본으로 넣어둡니다.
    browser_prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }

    # 2. 젠킨스/CI 환경 전용 설정
    if os.environ.get('JENKINS_URL') or os.environ.get('CI'):
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--lang=ko_KR')
        
        
        # [중요] 기존 browser_prefs에 한국어 설정을 추가(update)합니다.
        browser_prefs.update({
            "intl.accept_languages": "ko,ko-KR",
            "profile.default_content_languages": "ko-KR"
        })
        
        print("🚀 [DEBUG] 젠킨스 전용 최신 설정(언어/환경)이 통합 적용되었습니다!")
        
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        options.add_argument(f'user-agent={user_agent}')

    # 3. 통합된 prefs를 딱 한 번만 적용
    options.add_experimental_option("prefs", browser_prefs)

    # 4. 기타 옵션 및 드라이버 실행
    # 브라우저 사이즈 설정 설정이 안되어 있을 경우 화면에서 엘리먼트 못찾음
    options.add_argument('--window-size=1920x1080')
    clean_download_dir(download_dir)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)
    
    driver.set_window_size(1920, 1080)
    
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

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 테스트 결과를 가져옵니다.
    outcome = yield
    rep = outcome.get_result()
    
    # 테스트가 실패('call')했을 경우에만 실행됩니다.
    if rep.when == 'call' and rep.failed:
        try:
            # driver 피스처를 사용하는 테스트인지 확인
            if 'driver' in item.fixturenames:
                web_driver = item.funcargs['driver']
                
                # 프로젝트 루트에 screenshots 폴더 생성
                screenshot_dir = "screenshots"
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                
                # 파일명을 테스트 함수 이름으로 설정 (예: test_login_fail.png)
                file_path = os.path.join(screenshot_dir, f"{item.name}.png")
                web_driver.save_screenshot(file_path)
                print(f"\n📸 스크린샷 저장 완료: {file_path}")
        except Exception as e:
            print(f"❌ 스크린샷 저장 실패: {e}")
