from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class JoinPage:
    def __init__(self, driver):
        self.driver = driver

    def set_login_id(self, login_id):
        self.driver.find_element(By.NAME, "loginId").send_keys(login_id)
    def get_login_id(self):
        return self.driver.find_element(By.NAME, "loginId")
    
    def set_password(self, password):
        self.driver.find_element(By.NAME, "password").send_keys(password)
    def get_password(self):
        return self.driver.find_element(By.NAME, "password")
    
    def set_name(self, name):
        self.driver.find_element(By.NAME, "fullname").send_keys(name)
    def get_name(self):
        return self.driver.find_element(By.NAME, "fullname")
    
    def get_create_btn(self):
        return self.driver.find_element(By.LINK_TEXT, "Create account")
    
    def get_create_btn_2(self):
        return self.driver.find_element(By.XPATH, "//button[contains(text(),'Create account')]")
    
    def click_create_account_with_email(self):
        WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Create account with email']"))).click()

    def get_all_agr_chkboxes(self):
        return self.driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][data-indeterminate="false"]')

    # def get_agr_chkbox(self):
    #     return self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"].PrivateSwitchBase-input')

    def click_chkbox(self, index):
        chkboxs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"].PrivateSwitchBase-input')
        if not chkboxs[index].is_selected():
            chkboxs[index].click()

    def profile_click(self):
        self.driver.find_element(By.CSS_SELECTOR, '.MuiAvatar-root').click()
    
    def get_welcome_name(self):
        return self.driver.find_element(By.CSS_SELECTOR, "p.css-if9dpr").text
    
    def get_welcome_email(self):
        return self.driver.find_element(By.CSS_SELECTOR, "p.css-14lgytj").text

    def login_btn_click(self):
        self.driver.find_element(By.XPATH, "//button[normalize-space(text())='Login']").click()
