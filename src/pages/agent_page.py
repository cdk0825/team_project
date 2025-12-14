from selenium.webdriver.common.by import By
from src.pages.side_menu_page import SideMenu

class AgentPage:
    def __init__(self, driver):
        self.driver = driver
        self.side_menu = SideMenu(driver)

        self.AGENT_LIST = (By.XPATH, "//div[@data-testid='virtuoso-item-list']")

    def check_agent_list(self):
        return self.driver.find_element(*self.AGENT_LIST).is_displayed()