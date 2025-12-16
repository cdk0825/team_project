from selenium.webdriver.common.by import By
from src.pages.side_menu_page import SideMenu
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from src.pages.main_page_constants import (HISTORY_DELETE_BUTTON_PARAGRAPH, TITLE_RENAME_BUTTON_PARAGRAPH, RENAME_MODAL_TITLE, RENAME_CANCEL_BTN_PARAGRAPH, RENAME_SAVE_BTN_PARAGRAPH, DELETE_MODAL_TITLE, DELETE_CONFIRM_BTN_PARAGRAPH, SCROLL_PAUSE_TIME, INDEX_ATTRIBUTE)
from selenium.webdriver.common.keys import Keys
from src.utils import capture_screenshot
import re
from src.pages.chat_basic_page import chatBasicPage

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
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.MODAL_BACKDROP)).click()
        print("✅ 액션: 모달 배경 클릭 (모달 창 닫기)")

    def check_search_history_modal(self):
        """ 검색 히스토리 모달이 표시되는지 확인 """
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SEARCH_MODAL_SECTION)).is_displayed()
    
    def scroll_to_top(self, scrollable_container_xpath="//div[@data-testid='virtuoso-scroller']"):
        """ 맨 위로 스크롤 """
        scroll_script = f"document.evaluate(\"{scrollable_container_xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollTop = 0;"
        self.driver.execute_script(scroll_script)

    def get_first_history(self):
        """ 첫 번째 히스토리 가져오기 """
        first_history = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.FIRST_HISTORY))
        return first_history
            
    def find_history_menu(self, i=0):
        """ hover 시 나타나는 히스토리 메뉴 찾기 """
        history_list_section = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.HISTORY_LIST_SECTION))
        histories = history_list_section.find_elements(*self.HISTORY_LIST)

        if not histories:
            raise ValueError("히스토리 항목이 존재하지 않습니다.")
        if len(histories) <= i:
            raise ValueError(
                f"요청된 인덱스 ({i})에 해당하는 히스토리 항목이 없습니다. "
                f"현재 목록의 총 항목 수는 {len(histories)}개 입니다."
            )
        target_history = histories[i]
        print(target_history.text)
        
        # hover event
        ActionChains(self.driver).move_to_element(target_history).perform()

        hidden_menu_button = target_history.find_element(*self.HISTORY_MENU_BTN)
        hidden_menu_button.click()

        history_menu_modal = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.HISTORY_MENU_MODAL))
        return history_menu_modal
    
    def open_rename_modal_and_input(self, keyword, i=0):
        """ i번째의 히스토리 타이틀 변경 모달을 열고, 입력창에 keyword 입력 """
        history_menu_modal = self.find_history_menu(i)

        # 이름 변경 버튼 클릭
        history_rename_btn = history_menu_modal.find_element(*self.HISTORY_RENAME_BTN)
        history_rename_btn.click()

        new_title_input = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.RENAME_MODAL_INPUT_FIELD))
        new_title_input.click()

        # 입력창 초기화
        new_title_input.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
        new_title_input.send_keys(keyword)
        
        return history_menu_modal

    def modify_history_title(self, keyword, i=0):
        """ i번째 히스토리의 타이틀을 keyword로 변경 """
        history_menu_modal = self.open_rename_modal_and_input(keyword, i)

        save_btn = history_menu_modal.find_element(*self.RENAME_SAVE_BTN)
        save_btn.click()

        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.TOAST_MESSAGE))
        capture_screenshot(self.driver, title="modify_history")    
        print(f"✅ 액션: 인덱스 {i}의 히스토리 이름을 '{keyword}'으로 변경 완료")

    def delete_history_menu_select(self, i=0):
        history_menu_modal = self.find_history_menu(i)
        history_delete_btn = history_menu_modal.find_element(*self.HISTORY_DELETE_BTN)
        history_delete_btn.click()

        return history_menu_modal

    def delete_history(self, i=0):
        """ i번째 히스토리를 삭제 """
        history_menu_modal = self.delete_history_menu_select(i)

        delete_btn = history_menu_modal.find_element(*self.HISTORY_DELETE_CONFIRM_BTN)
        delete_btn.click()

        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.TOAST_MESSAGE))
        capture_screenshot(self.driver, title="delete_history")    
        print(f"✅ 액션: 인덱스 {i}의 히스토리 항목 삭제 완료")

    def delete_history_cancel(self, i=0):
        history_menu_modal = self.delete_history_menu_select(i)

        cancel_btn = history_menu_modal.find_element(*self.CANCEL_BTN)
        cancel_btn.click()

    def check_rename_validation_empty(self):
        """ 타이틀에 빈 값 입력 시 유효성 검사 상태 확인 """
        self.open_rename_modal_and_input("", 0)

        history_title_fieldset = self.driver.find_element(*self.HISTORY_TITLE_INPUT_FIELD)
        fieldset_color = history_title_fieldset.value_of_css_property("border-color")
        capture_screenshot(self.driver, title="modify_history")

        save_btn = self.driver.find_element(*self.RENAME_SAVE_BTN)
        return fieldset_color, save_btn.is_enabled()
  
    def check_rename_validation_max_length(self, keyword):
        """ 최대 길이 테스트 후 실제 저장된 타이틀 값 반환 """
        self.modify_history_title(keyword, 0)
        history_menu_modal_reopen = self.find_history_menu(i=0)

        # 이름 변경 버튼 클릭
        history_rename_btn = history_menu_modal_reopen.find_element(*self.HISTORY_RENAME_BTN)
        history_rename_btn.click()

        new_title_input = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.RENAME_MODAL_INPUT_FIELD))
        return new_title_input.get_attribute('value')
    def get_all_history_texts(self):
        history_list_section = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.HISTORY_LIST_SECTION)
        )
        history_elements =history_list_section.find_elements(*self.HISTORY_LIST)

        texts = []
        for element in history_elements:
            text_element = element.find_element(*self.HISTORY_PARAGRAPH)
            texts.append(text_element.text)
        return texts
    
    def check_modify_and_order(self, keyword, i=1):
        """ 이름 수정 후 히스토리 목록이 재정렬되는지 확인 """

        self.modify_history_title(keyword, i)
        after_texts = self.get_all_history_texts()
        is_reordered = after_texts[i] == keyword
        return is_reordered

    def get_chat_id_from_url(self, base_url: str = "https://qaproject.elice.io/ai-helpy-chat"):
        current_url = self.driver.current_url

        if not current_url.startswith(base_url):
            print(f"❌ URL 접두사 불일치: 기대값 '{base_url}', 실제값 '{current_url[:len(base_url)]}'")
            return None
        
        uuid_pattern = r"/chats/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"

        path = current_url.replace(base_url, "")
        match = re.match(uuid_pattern, path)

        if match:
            chat_id = match.group(1)
            return chat_id
        else:
            print(f"❌ URL 패턴 불일치: URL '{current_url}'에서 유효한 Chat ID를 찾을 수 없습니다.")
            return None
        
    def setup_function_with_precondition(self, keyword):
        """ keyword 타이틀의 새 히스토리를 생성 """
        self.side_menu.click_new_chat_btn()
        self.chat_page.send_message(keyword)
        self.chat_page.wait_for_response()

    def search_history_with_keyword(self, keyword):
        """ keyword로 히스토리 목록 검색 """
        self.side_menu.click_search_history_btn()
        
        dialog = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.DIALOG_CONTAINER))
        keyword_input = dialog.find_element(*self.HISTORY_SEARCH_INPUT_FIELD)
        keyword_input.click()

        # 입력창 초기화
        keyword_input.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
        keyword_input.send_keys(keyword)
        
        count = 0
        try:
            #search_result = dialog.find_element(*self.HISTORY_SEARCH_LIST)
            search_result = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.HISTORY_SEARCH_LIST))
            history_items = search_result.find_elements(*self.HISTORY_ITEM)
            count = len(history_items)
        except:
            count = 0
        finally:
            exit_btn = dialog.find_element(*self.HISTORY_SEARCH_EXIT_BTN)
            exit_btn.click()

        return count