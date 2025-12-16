from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



class UpdatePage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_setting(self):
        self.driver.find_element(By.CSS_SELECTOR, '.MuiAvatar-root').click()
        self.driver.find_element(By.XPATH, "//span[normalize-space(text())='계정 관리']").click()
        #세팅은 새창으로 전환되어서 포커스 새 창에 맞춰줌
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])
    
    def update_name(self):
        update_icons=self.driver.find_elements(By.XPATH, "//button[@type='button' and contains(@class,'MuiIconButton-root')]")
        update_icons[0].click()

        input_name = self.driver.find_element(By.NAME, "fullname")
        input_name.send_keys(Keys.CONTROL+"a", Keys.DELETE)
        input_name.send_keys("테스트")
        ok_btn= self.driver.find_element(By.XPATH, "//button[contains(text(),'완료')]")
        ok_btn.click()

        update_name = self.driver.find_element(By.XPATH, "//h6[contains(@class,'MuiTypography-subtitle2')]").text
        print(update_name)
        return update_name
    
  
