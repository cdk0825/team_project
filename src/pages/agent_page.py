from selenium.webdriver.common.by import By
from src.pages.side_menu_page import SideMenu
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from src.pages.agent_page_constants import AGENT_SEARCH_BUTTON_PARAGRAPH, NO_RESULT_FOUND_PARAGRAPH
from f1_helpychat.data.chat_history_data import NEW_AGENT_NAME, NEW_AGENT_RULE, NEW_AGENT_START_CONV
import logging
from src.utils import capture_screenshot

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

        # 로딩 확인용 skeleton
        self.SKELETON = (By.CSS_SELECTOR, "span.MuiSkeleton-root")
        self.AGENT_BUTTON = (By.XPATH, f"//div[contains(@class, 'virtuoso-grid-item')]//a[contains(@class, 'MuiCard-root')]")
        self.AGENT_TITLE = (By.XPATH, f"//div[contains(@class, 'MuiBox-root')]//h6[contains(@class, 'MuiTypography-h6')]")

        # 에이전트 탐색 창의 만들기 버튼
        self.CREATE_AGENT_BTN = (By.XPATH, "//a[contains(text(), '만들기')]")
        self.AGENT_NAME_INPUT = (By.CSS_SELECTOR, "input[name='name']")
        self.AGENT_RULE_INPUT = (By.CSS_SELECTOR, "textarea[name='systemPrompt']")
        self.START_CONVERSATION_INPUT = (By.CSS_SELECTOR, "input[name='conversationStarters.0.value']")
        # 에이전트 생성 창의 만들기 버튼
        self.CREATE_MY_AGENT_BTN = (By.XPATH, "//button[contains(text(), '만들기')]")
        self.LOADING_BTN = (By.XPATH, "//button[contains(@class, 'MuiLoadingButton-root')]/span[contains(@class, 'MuiLoadingButton-loadingIndicator')]")
        self.SAVE_BTN = (By.XPATH, "//div[@role='dialog']//button[contains(text(), '저장')]")

        # 스크롤 section
        self.AGENT_LIST_SECTION = (By.XPATH, "//main//div[@data-testid='virtuoso-scroller']")
        self.DELETE_TARGET_AGENT = (By.XPATH, f"//p[contains(text(), '{NEW_AGENT_NAME}')]/ancestor::a[contains(@class, 'MuiPaper-root')]")
        self.MENU_ICON = (By.XPATH, ".//*[@data-icon='ellipsis-vertical']")
        self.DELETE_MENU_BTN = (By.XPATH, "//p[contains(text(), '삭제')]/ancestor::li[@role='menuitem']")
        self.DELETE_CONFIRM_BTN = (By.XPATH, "//div[@role='dialog']//button[contains(text(), '삭제')]")

        self.GO_BACK_BTN = (By.XPATH, "//button[contains(@aria-label, '뒤로가기')]")

        # toast message
        self.NOTISTACK = (By.CSS_SELECTOR, "div#notistack-snackbar")

    def get_agent_list(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.AGENT_LIST))

    def get_agent_search_input(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.AGENT_SEARCH_INPUT))
    
    def get_no_result_msg(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.NO_RESULT_MESSAGE))

    def get_agent_title(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.AGENT_TITLE)).text

    def get_delete_target_agent(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.DELETE_TARGET_AGENT))


    def click_agent_btn(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.AGENT_BUTTON)).click()

    def click_create_agent_btn(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CREATE_AGENT_BTN)).click()

    def click_my_agent_btn(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CREATE_MY_AGENT_BTN)).click()

    def click_save_btn(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.SAVE_BTN)).click()

    def click_go_back_btn(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.GO_BACK_BTN)).click()

    def click_menu_icon(self, target):
        target.find_element(*self.MENU_ICON).click()

    def click_delete_menu_btn(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.DELETE_MENU_BTN)).click()

    def click_delete_confirm_btn(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.DELETE_CONFIRM_BTN)).click()

    def clear_input_field(self, target):
        target.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
        logger.debug("액션: 입력 필드 초기화")

    def scroll_to_bottom(self):
        self.driver.find_element(*self.AGENT_LIST_SECTION).send_keys(Keys.PAGE_DOWN)

    def capture_notistack(self, title):
        try:
            message = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.NOTISTACK)).text
            capture_screenshot(self.driver, title=title) 
            return message
        except TimeoutException:
            logger.error("❌ 토스트 메시지를 찾지 못했습니다.")  
            return ""

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

    def input_agent_name(self, keyword):
        name_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.AGENT_NAME_INPUT))
        name_input.click()
        self.clear_input_field(name_input)
        name_input.send_keys(keyword)
        logger.debug(f"액션: 키워드 '{keyword}' 입력 완료")

    def input_rule(self, keyword):
        rule_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.AGENT_RULE_INPUT))
        rule_input.click()
        self.clear_input_field(rule_input)
        rule_input.send_keys(keyword)
        logger.debug(f"액션: 키워드 '{keyword}' 입력 완료")

    def input_start_converstation(self, keyword):
        start_conv_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.START_CONVERSATION_INPUT))
        start_conv_input.click()
        self.clear_input_field(start_conv_input)
        start_conv_input.send_keys(keyword)
        logger.debug(f"액션: 키워드 '{keyword}' 입력 완료")

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

    def wait_for_loading_spinner_disappear(self):
        WebDriverWait(self.driver,10).until(EC.invisibility_of_element_located(self.LOADING_BTN))

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
        
    def create_agent(self):
        """ 에이전트 생성 """
        self.click_create_agent_btn()

        self.input_agent_name(NEW_AGENT_NAME)
        self.input_rule(NEW_AGENT_RULE)

        self.input_start_converstation(NEW_AGENT_START_CONV)
        self.click_my_agent_btn()
        self.click_save_btn()

        self.wait_for_loading_spinner_disappear()