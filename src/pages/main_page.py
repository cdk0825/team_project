from selenium.webdriver.common.by import By
from src.pages.side_menu_page import SideMenu
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from src.pages.main_page_constants import (HISTORY_DELETE_BUTTON_PARAGRAPH, TITLE_RENAME_BUTTON_PARAGRAPH, RENAME_MODAL_TITLE, RENAME_CANCEL_BTN_PARAGRAPH, RENAME_SAVE_BTN_PARAGRAPH, DELETE_MODAL_TITLE, DELETE_CONFIRM_BTN_PARAGRAPH, FIELDSET_OUTLINE_COLOR)
from selenium.webdriver.common.keys import Keys
from src.utils import capture_screenshot
import re
from src.pages.chat_basic_page import chatBasicPage
import logging
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.side_menu = SideMenu(driver)
        self.chat_page = chatBasicPage(driver)

        # 요소 선택
        self.MODAL_BACKDROP = (By.CSS_SELECTOR, ".MuiBackdrop-root")
        self.SEARCH_MODAL_SECTION = (By.CSS_SELECTOR, ".MuiDialog-paper[role='dialog']")
        self.HISTORY_LIST_SECTION = (By.XPATH, "//ul[@data-testid='virtuoso-item-list']")
        self.HISTORY_LIST = (By.CSS_SELECTOR, "a.MuiListItemButton-root")
        self.FIRST_HISTORY = (By.CSS_SELECTOR, "a.MuiListItemButton-root[data-item-index='0']")
        self.HISTORY_PARAGRAPH = (By.CSS_SELECTOR, "p.MuiTypography-root")
        self.HISTORY_MENU_BTN = (By.CSS_SELECTOR, ".menu-button")
        self.HISTORY_SCROLL_SECTION = (By.XPATH, "//div[@data-testid='virtuoso-scroller']")

        # 토스트 메시지
        self.TOAST_MESSAGE = (By.CSS_SELECTOR, ".notistack-MuiContent[role='alert']")

        # 히스토리 메뉴
        self.HISTORY_MENU_MODAL = (By.CSS_SELECTOR, ".MuiMenu-list[role='menu']")
        self.HISTORY_RENAME_BTN = (By.XPATH, f"//span[contains(text(), '{TITLE_RENAME_BUTTON_PARAGRAPH}')]/parent::div/parent::li")
        self.HISTORY_DELETE_BTN = (By.XPATH, f"//p[contains(text(), '{HISTORY_DELETE_BUTTON_PARAGRAPH}')]/parent::div/parent::li")
        
        # 이름 변경 모달
        self.RENAME_MODAL = (By.XPATH, f"//h2[contains(text(), '{RENAME_MODAL_TITLE}')]/parent::div[@role='dialog']")
        self.RENAME_MODAL_INPUT_FIELD = (By.XPATH, "//input[@name='name']")
        self.HISTORY_TITLE_INPUT_FIELD = (By.CSS_SELECTOR, "fieldset.MuiOutlinedInput-notchedOutline")

        # 모달 버튼
        self.CANCEL_BTN = (By.XPATH, f"//button[contains(text(), '{RENAME_CANCEL_BTN_PARAGRAPH}')]")
        self.RENAME_SAVE_BTN = (By.XPATH, f"//button[contains(text(), '{RENAME_SAVE_BTN_PARAGRAPH}')]")      
        self.HISTORY_DELETE_CONFIRM_BTN = (By.XPATH, f"//button[contains(text(), '{DELETE_CONFIRM_BTN_PARAGRAPH}')]")  
        
        # 히스토리 삭제 모달
        self.HISTORY_DELETE_MODAL = (By.XPATH, f"//h2[contains(text(), '{DELETE_MODAL_TITLE}')]/parent::div[@role='dialog']")

        # 히스토리 검색 모달
        self.DIALOG_CONTAINER = (By.CSS_SELECTOR, ".MuiDialog-container")
        self.HISTORY_SEARCH_INPUT_FIELD = (By.CSS_SELECTOR, "input[type='text'][placeholder='Search']")
        self.HISTORY_SEARCH_EXIT_BTN = (By.XPATH, "//*[@data-icon='xmark']/parent::button")
        self.HISTORY_SEARCH_LIST = (By.CSS_SELECTOR, "ul.MuiList-root")
        self.HISTORY_ITEM = (By.CSS_SELECTOR, "li.MuiListItem-root")

    def click_background(self):
        """ 모달 배경 클릭해 창 닫기 """
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.MODAL_BACKDROP)).click()
            logger.info("✅ 액션: 모달 배경 클릭 (모달 창 닫기)")
        except TimeoutException:
            logger.warning("❌ 경고: 모달 배경 요소를 찾지 못했습니다. 모달이 열려 있지 않을 수 있습니다.")

    def check_search_history_modal(self):
        """ 검색 히스토리 모달이 표시되는지 확인 """
        try:
            return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SEARCH_MODAL_SECTION)).is_displayed()
        except TimeoutException:
            logger.debug("❌ 검색 히스토리 모달이 10초 내에 표시되지 않았습니다.")
            return False
    
    def scroll_to_top(self, scrollable_container_xpath="//div[@data-testid='virtuoso-scroller']"):
        """ 맨 위로 스크롤 """
        scroll_script = f"document.evaluate(\"{scrollable_container_xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollTop = 0;"
        self.driver.execute_script(scroll_script)
        logger.debug("액션: 히스토리 목록을 맨 위로 스크롤")

    def get_first_history(self):
        """ 첫 번째 히스토리 가져오기 """
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.FIRST_HISTORY))

    def get_history_list_section(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.HISTORY_LIST_SECTION))

    def get_history_list(self):
        history_list_section = self.get_history_list_section()
        return history_list_section.find_elements(*self.HISTORY_LIST)
    
    def get_history_menu_modal(self):
        return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.HISTORY_MENU_MODAL))
    
    def get_rename_input_field_value(self):
        new_title_input = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.RENAME_MODAL_INPUT_FIELD))
        modified_value = new_title_input.get_attribute('value')
        logger.debug(f"검증: 재오픈된 입력 필드 값: {modified_value}")
    
    def click_rename_save_btn(self, target):
        target.find_element(*self.RENAME_SAVE_BTN).click()
        logger.debug("액션: '저장' 버튼 클릭")

    def click_hidden_menu_btn(self, target):
        # hover event
        ActionChains(self.driver).move_to_element(target).perform()
        logger.debug("액션: 히스토리 항목에 마우스 오버")

        hidden_menu_button = target.find_element(*self.HISTORY_MENU_BTN)
        hidden_menu_button.click()
        logger.debug("액션: 히스토리 메뉴 버튼 클릭")

    def click_rename_btn(self, target):
        target.find_element(*self.HISTORY_RENAME_BTN).click()
        logger.debug("액션: 이름 변경 버튼 클릭")

    def click_delete_btn(self, target):
        target.find_element(*self.HISTORY_DELETE_BTN).click()
        logger.debug("액션: 삭제 버튼 클릭")

    def click_history_delete_confirm_btn(self, target):
        target.find_element(*self.HISTORY_DELETE_CONFIRM_BTN).click()
        logger.debug("액션: 삭제 확인 버튼 클릭")

    def click_cancel_btn(self, target):
        target.find_element(*self.CANCEL_BTN).click()
        logger.info("✅ 액션: 삭제 모달에서 '취소' 버튼 클릭")

    def clear_input_field(self, target):
        target.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
        logger.debug("액션: 입력 필드 초기화")

    def capture_toast_message(self, title):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.TOAST_MESSAGE))
        capture_screenshot(self.driver, title=title)   

    def validation_fieldset_color(self):
        history_title_fieldset = self.driver.find_element(*self.HISTORY_TITLE_INPUT_FIELD)
        fieldset_color = history_title_fieldset.value_of_css_property("border-color")
        capture_screenshot(self.driver, title="modify_history_empty_validation")
        logger.debug(f"검증: fieldset border-color: {fieldset_color}")

        if fieldset_color != FIELDSET_OUTLINE_COLOR:
            logger.error(f"❌ fieldset의 outline 색상이 예상 색상({FIELDSET_OUTLINE_COLOR})과 다릅니다: {fieldset_color}")
        logger.info(f"✅ fieldset outline 색상: {fieldset_color}")

    def validation_save_btn_is_enabled(self):
        is_enabled = self.driver.find_element(*self.RENAME_SAVE_BTN).is_enabled()

        if is_enabled:
            logger.error("❌ 저장 버튼이 비활성화 되지 않았습니다.")
        logger.info(f"✅ 저장 버튼 활성화 상태: {is_enabled} (비활성화됨)")

    def input_rename_field(self, keyword):
        new_title_input = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.RENAME_MODAL_INPUT_FIELD))
        new_title_input.click()

        self.clear_input_field(new_title_input)
        
        new_title_input.send_keys(keyword)
        logger.debug(f"액션: 입력 값 '{keyword}' 입력")

    def find_history_menu(self, i=0):
        """ hover 시 나타나는 히스토리 메뉴 찾기 """
        histories = self.get_history_list()

        if not histories:
            raise ValueError("❌ 히스토리 항목이 존재하지 않습니다.")
        if len(histories) <= i:
            raise ValueError(
                f"❌ 요청된 인덱스 ({i})에 해당하는 히스토리 항목이 없습니다. "
                f"현재 목록의 총 항목 수는 {len(histories)}개 입니다."
            )
        target_history = histories[i]
        logger.debug(f"대상 히스토리 ({i}) 텍스트: {target_history.text}")
        
        self.click_hidden_menu_btn(target_history)

        return self.get_history_menu_modal()

    def wait_for_history_title_update(self, expected_title, index=0):
        target_locator = (By.CSS_SELECTOR, f"a.MuiListItemButton-root[data-item-index='{index}'] p.MuiTypography-root")
        
        logger.debug(f"검증: 인덱스 {index}의 타이틀이 '{expected_title}'로 업데이트될 때까지 대기")
        
        try:
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element(target_locator, expected_title)
            )
            logger.info("✅ 검증: 히스토리 목록에서 타이틀 업데이트 확인 완료")
        except TimeoutException:
            current_text = self.driver.find_element(*target_locator).text
            logger.error(f"❌ 오류: 10초 내에 타이틀이 업데이트되지 않았습니다. 현재 값: '{current_text}'")
            raise

    def modify_history_title(self, keyword, i=0):
        """ i번째 히스토리의 타이틀을 keyword로 변경 """
        history_menu_modal = self.find_history_menu(i)

        self.click_rename_btn(history_menu_modal)
        self.input_rename_field(keyword)
        
        self.click_rename_save_btn(history_menu_modal)

        self.wait_for_history_title_update(keyword, i)

        self.capture_toast_message(title="modify_history")
        logger.info(f"✅ 액션: 인덱스 {i}의 히스토리 이름을 '{keyword}'으로 변경 완료")

    def get_all_history_texts(self):
        try:
            history_elements = self.get_history_list()

            texts = []
            for element in history_elements:
                text_element = element.find_element(*self.HISTORY_PARAGRAPH)
                texts.append(text_element.text)
            return texts
        except TimeoutException:
            logger.warning("경고: 히스토리 목록 섹션을 찾지 못했습니다. 빈 리스트 반환.")
            return []
        except NoSuchElementException:
            logger.warning("경고: 히스토리 항목을 찾지 못했습니다. 빈 리스트 반환.")
            return []

    def get_chat_id_from_url(self, base_url: str = "https://qaproject.elice.io/ai-helpy-chat"):
        current_url = self.driver.current_url
        logger.debug(f"현재 URL: {current_url}")

        if not current_url.startswith(base_url):
            logger.error(f"❌ URL 접두사 불일치: 기대값 '{base_url}', 실제값 '{current_url[:len(base_url)]}'")
            return None
        
        uuid_pattern = r"/chats/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"

        path = current_url.replace(base_url, "")
        match = re.match(uuid_pattern, path)

        if match:
            chat_id = match.group(1)
            logger.debug(f"✅ Chat ID 추출 성공: {chat_id}")
            return chat_id
        else:
            logger.error(f"❌ URL 패턴 불일치: URL '{current_url}'에서 유효한 Chat ID를 찾을 수 없습니다.")
            return None
        
    def setup_function_with_precondition(self, keyword):
        """ keyword 타이틀의 새 히스토리를 생성 """
        logger.info(f"액션: 새 히스토리 생성을 위한 전제 조건 실행 (키워드: '{keyword}')")
        self.side_menu.click_new_chat_btn()
        self.chat_page.send_message(keyword)
        self.chat_page.wait_for_response()
        logger.debug("전제 조건 완료: 메시지 전송 및 응답 대기 완료")

    def search_history_with_keyword(self, keyword):
        """ keyword로 히스토리 목록 검색 """
        logger.debug(f"액션: 히스토리 검색 모달 열기 및 키워드 '{keyword}' 검색 시작")
        self.side_menu.click_search_history_btn()
        
        try:
            dialog = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.DIALOG_CONTAINER))
            keyword_input = dialog.find_element(*self.HISTORY_SEARCH_INPUT_FIELD)
            keyword_input.click()

            # 입력창 초기화 및 키워드 입력
            keyword_input.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
            keyword_input.send_keys(keyword)
            logger.debug(f"액션: 검색어 '{keyword}' 입력 완료")
            
            count = 0
            
            # 검색 결과 목록을 대기
            search_result = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.HISTORY_SEARCH_LIST))
            history_items = search_result.find_elements(*self.HISTORY_ITEM)
            count = len(history_items)
            logger.info(f"검색 결과 확인: '{keyword}'에 대해 {count}개의 항목 발견")
            
        except TimeoutException:
            logger.warning("검색 결과 목록(HISTORY_SEARCH_LIST)이 5초 내에 나타나지 않았습니다. 검색 결과 없음으로 간주.")
            count = 0
        except NoSuchElementException:
            logger.debug("검색 결과 항목을 찾을 수 없습니다. (0개로 처리)")
            count = 0
        finally:
            try:
                exit_btn = self.driver.find_element(*self.HISTORY_SEARCH_EXIT_BTN)
                exit_btn.click()
                logger.debug("액션: 검색 모달 닫기 버튼 클릭")
            except Exception as e:
                logger.warning(f"검색 모달 닫기 실패: {e}")

            return count