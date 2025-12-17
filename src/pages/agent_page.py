from selenium.webdriver.common.by import By
from src.pages.side_menu_page import SideMenu
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from src.pages.agent_page_constants import AGENT_SEARCH_BUTTON_PARAGRAPH, NO_RESULT_FOUND_PARAGRAPH
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class AgentPage:
    def __init__(self, driver):
        self.driver = driver
        self.side_menu = SideMenu(driver)

        # 요소 선택
        self.AGENT_SEARCH_INPUT = (By.XPATH, f"//input[contains(@placeholder, '{AGENT_SEARCH_BUTTON_PARAGRAPH}')]")
        self.AGENT_LIST = (By.CSS_SELECTOR, ".MuiGrid-container")
        self.AGENT_LIST_TITLES = (By.CSS_SELECTOR, ".MuiTypography-root")
        self.NO_RESULT_MESSAGE = (By.XPATH, f"//h6[contains(text(), '{NO_RESULT_FOUND_PARAGRAPH}')]")

        self.SKELETON = (By.CSS_SELECTOR, "span.MuiSkeleton-root")
        self.AGENT_BUTTON = (By.XPATH, f"//div[contains(@class, 'virtuoso-grid-item')]//a[contains(@class, 'MuiCard-root')]")
        self.AGENT_TITLE = (By.XPATH, f"//div[contains(@class, 'MuiBox-root')]//h6[contains(@class, 'MuiTypography-h6')]")

    def get_agent_list(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.AGENT_LIST))

    def get_agent_search_input(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.AGENT_SEARCH_INPUT))
    
    def get_no_result_msg(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.NO_RESULT_MESSAGE))

    def get_agent_title(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.AGENT_TITLE)).text

    def wait_for_skeleton_disappear(self, timeout=10):
        """
        스켈레톤(로딩 표시) 요소가 DOM에서 사라지거나 보이지 않게 될 때까지 명시적으로 대기
        """
        logger.debug(f"검증: 스켈레톤 로딩 요소 ({self.SKELETON}) 사라짐 대기 시작 (최대 {timeout}초)")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.SKELETON),
                message=f"❌ 로딩이 {timeout}초를 초과했습니다. 스켈레톤 요소가 여전히 표시됨."
            )
            logger.info("✅ 검증 완료: 스켈레톤 로딩 요소 사라짐 확인 (데이터 로드 완료)")
            return True
        except TimeoutException:
            logger.error(f"❌ 오류: 스켈레톤이 지정된 시간 내에 사라지지 않았습니다.")
            raise

    def click_agent_button(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.AGENT_BUTTON)).click()

    def clear_input_field(self, target):
        target.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
        logger.debug("액션: 입력 필드 초기화")

    def input_search_keyword(self, keyword):
        """ 검색 필드에 키워드를 입력해 에이전트 목록 검색 """
        logger.info(f"액션: 검색 필드에 키워드 '{keyword}' 입력")

        search_field = self.get_agent_search_input()
        search_field.click()

        self.clear_input_field(search_field)
        
        search_field.send_keys(keyword)
        logger.debug(f"액션: 키워드 '{keyword}' 입력 완료")


    def check_no_result_message_is_displayed(self):
        logger.debug("검증: '검색 결과 없음' 메시지 표시 여부 확인 시작")
        try:
            self.get_no_result_msg()
            logger.info("✅ 검증: '검색 결과 없음' 메시지가 표시되었습니다.")
            return True
        except TimeoutException:
            logger.info("❌ 검증: '검색 결과 없음' 메시지가 10초 내에 표시되지 않았습니다.")
            return False
        except Exception as e:
            logger.error(f"❌ 오류: 결과 없음 메시지 확인 중 예외 발생: {e}")
            return False
    
    def wait_for_search_result_state(self):
        def check_result_state(driver):
            try:
                list_section = self.get_agent_list()
                if list_section.is_displayed():
                    return True
            except (NoSuchElementException, StaleElementReferenceException):
                pass
                
            try:
                no_result = driver.find_element(*self.NO_RESULT_MESSAGE)
                if no_result.is_displayed():
                    return True
            except (NoSuchElementException, StaleElementReferenceException):
                pass
                
            return False
        
        logger.debug("검증: 검색 결과 목록 상태가 확정될 때까지 대기 (최대 10초)")
        try:
            WebDriverWait(self.driver, 10).until(check_result_state, message="❌ 검색 결과 목록 또는 결과 없음 메시지가 10초 내에 나타나지 않았습니다.")
        except TimeoutException:
            logger.warning("❌ 경고: 검색 결과 상태를 10초 내에 확인할 수 없습니다. 빈 리스트로 처리합니다.")
            raise
    
    def is_no_result_msg_displayed(self):
        try:
            no_result_element = self.get_no_result_msg()
            return no_result_element.is_displayed()
        except NoSuchElementException:
            return False
        except StaleElementReferenceException:
            return False
        
    def get_all_search_result_texts(self):
        try:
            list_section = self.get_agent_list()
            agent_list_elements = list_section.find_elements(*self.AGENT_LIST_TITLES)

            texts = [e.text for e in agent_list_elements]
            return texts
        except NoSuchElementException:
            logger.warning("❌ 경고: 에이전트 목록 섹션을 찾을 수 없습니다.")
            return []
        except StaleElementReferenceException:
            logger.warning("❌ 경고: 목록 요소 참조가 만료되었습니다.")
            return []

    def count_keyword_list(self, keyword):
        """ 검색 결과 목록을 확인하고, 결과에서 주어진 키워드를 포함하는 항목 리스트 반환 """
        try:
            self.wait_for_search_result_state()

            if self.is_no_result_msg_displayed():
                logger.info("✅ 검증: '검색 결과 없음' 상태 확인됨. 빈 리스트 반환.")
                return []
            
            all_texts = self.get_all_search_result_texts()

            contains_keyword_list = [text for text in all_texts if keyword in text]

            logger.info(f"✅ 검증: '{keyword}'를 포함하는 항목 {len(contains_keyword_list)}개 발견")
            logger.debug(f"발견된 항목 목록: {contains_keyword_list}")
            return contains_keyword_list
        except TimeoutException:
            return []