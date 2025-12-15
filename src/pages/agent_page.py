from selenium.webdriver.common.by import By
from src.pages.side_menu_page import SideMenu
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from src.pages.agent_page_constants import AGENT_SEARCH_BUTTON_PARAGRAPH, NO_RESULT_FOUND_PARAGRAPH

class AgentPage:
    def __init__(self, driver):
        self.driver = driver
        self.side_menu = SideMenu(driver)

        self.AGENT_LIST = (By.CSS_SELECTOR, ".MuiGrid-container")

        self.AGENT_SEARCH_INPUT = (By.XPATH,  f"//input[contains(@placeholder, '{AGENT_SEARCH_BUTTON_PARAGRAPH}')]")

        self.AGENT_LIST_TITLES = (By.CSS_SELECTOR, ".MuiTypography-root")

        self.NO_RESULT_MESSAGE = (By.XPATH, f"//h6[contains(text(), '{NO_RESULT_FOUND_PARAGRAPH}')]")

    def check_agent_list(self):
        agent_list = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.AGENT_LIST))
        return agent_list.is_displayed()
    
    def input_search_keyword(self, keyword):
        search_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.AGENT_SEARCH_INPUT))
        search_field.click()

        # 입력창 초기화
        search_field.send_keys(Keys.CONTROL, 'a')
        search_field.send_keys(Keys.DELETE)
        # 키워드 입력
        search_field.send_keys(keyword)
    
    def count_keyword_list(self, keyword):
        def check_result_state(driver):
            list_section = driver.find_element(*self.AGENT_LIST)
            if list_section.is_displayed():
                return list_section
            no_result = driver.find_element(*self.NO_RESULT_MESSAGE)
            if no_result.is_displayed():
                return no_result
            return False
        try:
            result = WebDriverWait(self.driver, 10).until(check_result_state)
            if result == NO_RESULT_FOUND_PARAGRAPH:
                return []
            agent_list_elements = result.find_elements(*self.AGENT_LIST_TITLES)
            agent_list_texts = [e.text for e in agent_list_elements]

            contains_keyword_list = []
            for text in agent_list_texts:
                if keyword in text:
                    contains_keyword_list.append(text)

            return contains_keyword_list
        except TimeoutException:
            print(f"DEBUG: 키워드 '{keyword}'에 대한 검색 결과 목록 섹션({self.AGENT_LIST})이 10초 안에 나타나지 않았습니다. (검색 결과 없음으로 간주)")
            return []