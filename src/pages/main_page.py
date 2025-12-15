from selenium.webdriver.common.by import By
from src.pages.side_menu_page import SideMenu
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from src.pages.main_page_constants import HISTORY_DELETE_BUTTON_PARAGRAPN, TITLE_RENAME_BUTTON_PARAGRAPH, RENAME_MODAL_TITLE, RENAME_CANCEL_BTN_PARAGRAPH, RENAME_SAVE_BTN_PARAGRAPH, NEW_TITLE_NAME, DELETE_MODAL_TITLE, DELETE_CONFIRM_BTN_PARAGRAPH, SCROLL_PAUSE_TIME, INDEX_ATTRIBUTE
from selenium.webdriver.common.keys import Keys
from src.utils import capture_screenshot
import time


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.side_menu = SideMenu(driver)
        # 모달 배경
        self.MODAL_BACKDROP = (By.CSS_SELECTOR, ".MuiBackdrop-root")
        # 검색 모달 창
        self.SEARCH_MODAL_SECTION = (By.CSS_SELECTOR, ".MuiDialog-paper[role='dialog']")
        # 히스토리 목록 섹션
        self.HISTORY_LIST_SECTION = (By.XPATH, "//ul[@data-testid='virtuoso-item-list']")
        # 히스토리 목록
        self.HISTORY_LIST = (By.CSS_SELECTOR, "a.MuiListItemButton-root")
        # 첫 번째 히스토리
        self.FIRST_HISTORY = (By.CSS_SELECTOR, "a.MuiListItemButton-root[data-item-index='0']")
        # 히스토리 문구
        self.HISTORY_PARAGRAPH = (By.CSS_SELECTOR, "p.MuiTypography-root")
        # 히스토리 메뉴 버튼
        self.HISTORY_MENU_BTN = (By.CSS_SELECTOR, ".menu-button")
        # 히스토리 메뉴 모달
        self.HISTORY_MENU_MODAL = (By.CSS_SELECTOR, ".MuiMenu-list[role='menu']")
        # 히스토리 타이틀 변경 버튼
        self.HISTORY_RENAME_BTN = (By.XPATH, f"//span[contains(text(), '{TITLE_RENAME_BUTTON_PARAGRAPH}')]/parent::div/parent::li")
        # 히스토리 삭제 버튼
        self.HISTORY_DELETE_BTN = (By.XPATH, f"//p[contains(text(), '{HISTORY_DELETE_BUTTON_PARAGRAPN}')]/parent::div/parent::li")
        # 이름 변경 모달 창
        self.RENAME_MODAL = (By.XPATH, f"//h2[contains(text(), '{RENAME_MODAL_TITLE}')]/parent::div[@role='dialog']")
        # 이름 변경 모달 창 - 입력 필드
        self.RENAME_MODAL_INPUT_FIELD = (By.XPATH, "//input[@name='name']")
        # 취소 버튼 (이름 변경, 히스토리 삭제 동일)
        self.CANCEL_BTN = (By.XPATH, f"//button[contains(text(), '{RENAME_CANCEL_BTN_PARAGRAPH}')]")
        # 이름 변경 저장 버튼
        self.RENAME_SAVE_BTN = (By.XPATH, f"//button[contains(text(), '{RENAME_SAVE_BTN_PARAGRAPH}')]")
        # 토스트 메시지
        self.TOAST_MESSAGE = (By.CSS_SELECTOR, ".notistack-MuiContent[role='alert']")
        # 히스토리 삭제 모달 창
        self.HISTORY_DELETE_MODAL = (By.XPATH, f"//h2[contains(text(), '{DELETE_MODAL_TITLE}')]/parent::div[@role='dialog']")
        # 히스토리 삭제 확인 버튼
        self.HISTORY_DELETE_CONFIRM_BTN = (By.XPATH, f"//button[contains(text(), '{DELETE_CONFIRM_BTN_PARAGRAPH}')]")
        # 히스토리 스크롤 섹션
        self.HISTORY_SCROLL_SECTION = (By.XPATH, "//div[@data-testid='virtuoso-scroller']")
        # 이름 변경 모달 창 - 입력 필드 - OUTLINE
        self.HISTORY_TITLE_INPUT_FIELD = (By.CSS_SELECTOR, "fieldset.MuiOutlinedInput-notchedOutline")

    def click_background(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.MODAL_BACKDROP)).click()
        print("✅ 액션: 모달 배경 클릭 (모달 창 닫기)")

    def check_search_history_modal(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SEARCH_MODAL_SECTION)).is_displayed()
    
    def scroll_to_top(self, scrollable_container_xpath="//div[@data-testid='virtuoso-scroller']"):
        scroll_script = f"document.evaluate(\"{scrollable_container_xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollTop = 0;"
        self.driver.execute_script(scroll_script)

    def count_all_history_items(self, scrollable_container_xpath="//div[@data-testid='virtuoso-scroller']"):
        def get_last_valid_index(elements, attribute_name):
            for ele in reversed(elements):
                index_value = ele.get_attribute(attribute_name)
                if index_value is not None:
                    return int(index_value)
            return 0

        scroll_script = f"document.evaluate(\"{scrollable_container_xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollTop = document.evaluate(\"{scrollable_container_xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight;"
        self.driver.execute_script(scroll_script)

        time.sleep(SCROLL_PAUSE_TIME)

        history_elements = self.driver.find_elements(*self.HISTORY_LIST)
        last_index = get_last_valid_index(history_elements, INDEX_ATTRIBUTE)

        return last_index + 1

    def get_first_history(self):
        first_history = self.driver.find_element(*self.FIRST_HISTORY)
        return first_history
            
    def find_history_menu(self):
        history_list_section = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.HISTORY_LIST_SECTION))
        first_history = history_list_section.find_element(*self.HISTORY_LIST)

        # hover event
        actions = ActionChains(self.driver)
        actions.move_to_element(first_history).perform()

        hidden_menu_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.HISTORY_MENU_BTN))
        hidden_menu_button.click()

        history_menu_modal = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.HISTORY_MENU_MODAL))
        return history_menu_modal
    
    def find_first_history_and_input_keyword(self, keyword):
        history_menu_modal = self.find_history_menu()

        # 이름 변경 버튼 클릭
        history_rename_btn = history_menu_modal.find_element(*self.HISTORY_RENAME_BTN)
        history_rename_btn.click()

        new_title_input = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.RENAME_MODAL_INPUT_FIELD))
        new_title_input.click()

        # 입력창 초기화
        new_title_input.send_keys(Keys.CONTROL, 'a')
        new_title_input.send_keys(Keys.DELETE)

        # 새 타이틀명 입력
        new_title_input.send_keys(keyword)
        return history_menu_modal

    def modify_first_history(self):
        history_menu_modal = self.find_first_history_and_input_keyword(NEW_TITLE_NAME)

        save_btn = history_menu_modal.find_element(*self.RENAME_SAVE_BTN)
        save_btn.click()

        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.TOAST_MESSAGE))
        time.sleep(0.5)
        capture_screenshot(self.driver, title="modify_history")    

    def delete_first_history(self):
        history_menu_modal = self.find_history_menu()
        history_delete_btn = history_menu_modal.find_element(*self.HISTORY_DELETE_BTN)
        history_delete_btn.click()

        delete_btn = history_menu_modal.find_element(*self.HISTORY_DELETE_CONFIRM_BTN)
        delete_btn.click()

        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.TOAST_MESSAGE))
        time.sleep(0.5)
        capture_screenshot(self.driver, title="delete_history")    

    def modify_history_title_empty(self):
        self.find_first_history_and_input_keyword("")
        history_title_fieldset = self.driver.find_element(*self.HISTORY_TITLE_INPUT_FIELD)
        fieldset_color = history_title_fieldset.value_of_css_property("border-color")
        capture_screenshot(self.driver, title="modify_history")

        save_btn = self.driver.find_element(*self.RENAME_SAVE_BTN)
        return fieldset_color, save_btn.is_enabled()
  
    def modify_history_title_max_length(self, keyword):
        self.find_first_history_and_input_keyword(keyword)

        save_btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.RENAME_SAVE_BTN))
        save_btn.click()

        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.TOAST_MESSAGE))
        time.sleep(0.5)
        capture_screenshot(self.driver, title="modify_history")    

        time.sleep(5)
        history_menu_modal_reopen = self.find_history_menu()

        # 이름 변경 버튼 클릭
        history_rename_btn = history_menu_modal_reopen.find_element(*self.HISTORY_RENAME_BTN)
        history_rename_btn.click()

        new_title_input = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.RENAME_MODAL_INPUT_FIELD))
        return new_title_input.get_attribute('value')

