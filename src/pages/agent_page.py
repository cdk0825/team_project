from selenium.webdriver.common.by import By
from src.pages.side_menu_page import SideMenu
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.pages.agent_page_constants import AGENT_SEARCH_BUTTON_PARAGRAPH, NO_RESULT_FOUND_PARAGRAPH

class AgentPage:
    def __init__(self, driver):
        self.driver = driver
        self.side_menu = SideMenu(driver)

       # 요소 선택
        self.AGENT_SEARCH_INPUT = (By.XPATH,  f"//input[contains(@placeholder, '{AGENT_SEARCH_BUTTON_PARAGRAPH}')]")
        self.AGENT_LIST = (By.CSS_SELECTOR, ".MuiGrid-container")
        self.AGENT_LIST_TITLES = (By.CSS_SELECTOR, ".MuiTypography-root")
        self.NO_RESULT_MESSAGE = (By.XPATH, f"//h6[contains(text(), '{NO_RESULT_FOUND_PARAGRAPH}')]")

    def check_agent_list(self):
        """ 에이전트 목록 섹션 화면 출력 여부 확인 """
        agent_list = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.AGENT_LIST))
        return agent_list.is_displayed()
    
    def input_search_keyword(self, keyword):
        """ 검색 필드에 키워드를 입력해 에이전트 목록 검색 """
        search_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.AGENT_SEARCH_INPUT))
        search_field.click()

        # 입력창 초기화
        search_field.send_keys(Keys.CONTROL, 'a')
        search_field.send_keys(Keys.DELETE)
        # 키워드 입력
        search_field.send_keys(keyword)

    def check_no_result_message_is_displayed(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.NO_RESULT_MESSAGE))
            return True
        except TimeoutException:
            return False
    
    def count_keyword_list(self, keyword):
        """ 검색 결과 목록을 확인하고, 결과에서 주어진 키워드를 포함하는 항목 리스트 반환 """
        def check_result_state(driver):
            list_section = driver.find_element(*self.AGENT_LIST)
            if list_section.is_displayed():
                return True
            no_result = driver.find_element(*self.NO_RESULT_MESSAGE)
            if no_result.is_displayed():
                return True
            return False
        try:
            WebDriverWait(self.driver, 10).until(check_result_state)
            no_result_element = self.driver.find_element(*self.NO_RESULT_MESSAGE)
            if no_result_element.is_displayed():
                return []
        except NoSuchElementException:
            pass

        try:
            list_section = self.driver.find_element(*self.AGENT_LIST)
            agent_list_elements = list_section.find_elements(*self.AGENT_LIST_TITLES)
            contains_keyword_list = [e.text for e in agent_list_elements if keyword in e.text]
            return contains_keyword_list
        
        except NoSuchElementException:
            return []