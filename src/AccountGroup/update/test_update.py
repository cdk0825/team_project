from selenium.webdriver.support import expected_conditions as EC
import logging
from src.pages.update_page import UpdatePage
from src.utils import login
from src.config import USERNAME5, PASSWORD5


#로깅설정하기
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def test_update_name(driver):
    page = UpdatePage(driver)
    login(driver, USERNAME5, PASSWORD5)
    page.go_to_setting()

    after_name = page.update_name()
    assert after_name =='테스트'