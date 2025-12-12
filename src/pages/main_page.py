from selenium.webdriver.common.by import By

class MainPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # 새 대화 버튼
    NEW_CHAT_BTN = (By.XPATH, "//a[@href='/ai-helpy-chat']")
    # 검색 버튼
    SEARCH_HISTORY_BTN = (By.XPATH, "//span[contains(text(), '검색')]/ancestor::div[2]")
    # 도구 버튼
    TOOLS_BTN = (By.XPATH, "//a[@href='/ai-helpy-chat/tools']")
    # 에이전트 탐색 버튼
    AGENT_SEARCH_BTN = (By.XPATH, "//a[@href='/ai-helpy-chat/agents']")

    # 모달 배경
    MODAL_BACKDROP = (By.CSS_SELECTOR, ".MuiBackdrop-root")

    def click_new_chat_btn(self):
        self.driver.find_element(*self.NEW_CHAT_BTN).click()

    def click_search_history_btn(self):
        self.driver.find_element(*self.SEARCH_HISTORY_BTN).click()

    def click_tools_btn(self):
        self.driver.find_element(*self.TOOLS_BTN).click()

    def click_agent_search_btn(self):
        self.driver.find_element(*self.AGENT_SEARCH_BTN).click()

    def click_background(self):
        self.driver.find_element(*self.MODAL_BACKDROP).click()