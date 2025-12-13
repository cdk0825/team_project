from selenium.webdriver.common.by import By

class SideMenu:
    def __init__(self, driver):
        self.driver = driver
        # 새 대화 버튼
        self.NEW_CHAT_BTN = (By.XPATH, "//a[@href='/ai-helpy-chat']")
        # 검색 버튼
        self.SEARCH_HISTORY_BTN = (By.XPATH, "//span[contains(text(), '검색')]/ancestor::div[2]")
        # 도구 버튼
        self.TOOLS_BTN = (By.XPATH, "//a[@href='/ai-helpy-chat/tools']")
        # 에이전트 탐색 버튼
        self.AGENT_SEARCH_BTN = (By.XPATH, "//a[@href='/ai-helpy-chat/agents']")

    def click_new_chat_btn(self):
        self.driver.find_element(*self.NEW_CHAT_BTN).click()
        print("✅ 액션: 새 대화 버튼 클릭")

    def click_search_history_btn(self):
        self.driver.find_element(*self.SEARCH_HISTORY_BTN).click()
        print("✅ 액션: 히스토리 검색 버튼 클릭")

    def click_tools_btn(self):
        self.driver.find_element(*self.TOOLS_BTN).click()
        print("✅ 액션: 도구 버튼 클릭")

    def click_agent_search_btn(self):
        self.driver.find_element(*self.AGENT_SEARCH_BTN).click()
        print("✅ 액션: 에이전트 탐색 버튼 클릭")   