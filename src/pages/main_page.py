from selenium.webdriver.common.by import By
from src.pages.side_menu_page import SideMenu

class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.side_menu = SideMenu(driver)
        # 모달 배경
        self.MODAL_BACKDROP = (By.CSS_SELECTOR, ".MuiBackdrop-root")
        # 검색 모달 창
        self.SEARCH_MODAL_SECTION = (By.CSS_SELECTOR, ".MuiDialog-paper[role='dialog']")
    
    def click_background(self):
        self.driver.find_element(*self.MODAL_BACKDROP).click()
        print("✅ 액션: 모달 배경 클릭 (모달 창 닫기)")

    def check_search_history_modal(self):
        return self.driver.find_element(*self.SEARCH_MODAL_SECTION).is_displayed()
