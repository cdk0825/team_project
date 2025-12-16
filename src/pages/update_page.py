from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

class UpdatePage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_setting(self):
        self.driver.find_element(By.CSS_SELECTOR, '.MuiAvatar-root').click()
        self.driver.find_element(By.XPATH, "//span[normalize-space(text())='계정 관리']").click()
        #세팅은 새창으로 전환되어서 포커스 새 창에 맞춰줌
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])

    def ok_btn(self):
        return self.driver.find_element(By.XPATH, "//button[contains(text(),'완료')]")
    
    def update_name(self, new_name):
        wait = WebDriverWait(self.driver, 10)
        update_icon_locator = (By.XPATH, "//button[@type='button' and contains(@class,'MuiIconButton-root')]")

        # 요소가 나타날 때까지 기다림
        update_icons = wait.until(EC.presence_of_all_elements_located(update_icon_locator))
        update_icons[0].click()

        input_name = self.driver.find_element(By.NAME, "fullname")
        input_name.send_keys(Keys.CONTROL+"a", Keys.DELETE)
        input_name.send_keys(new_name)

        return new_name
    
    def send_code(self):
         return self.driver.find_element(By.XPATH, "//button[contains(text(),'인증메일 발송')]")

    def update_email(self, new_email):
        wait = WebDriverWait(self.driver, 10)
        update_icon_locator = (By.XPATH, "//button[@type='button' and contains(@class,'MuiIconButton-root')]")

        # 요소가 나타날 때까지 기다림
        update_icons = wait.until(EC.presence_of_all_elements_located(update_icon_locator))
        update_icons[1].click()

        input_email = self.driver.find_element(By.NAME, "to")

        input_email.send_keys(Keys.CONTROL+"a", Keys.DELETE)
        input_email.send_keys(new_email)
        time.sleep(3)

        return new_email
    

    
  
