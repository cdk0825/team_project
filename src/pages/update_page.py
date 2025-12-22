from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UpdatePage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_setting(self):
        wait = WebDriverWait(self.driver, 10)

        profile = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiAvatar-root")))
        profile.click()

        account_manage = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space(text())='계정 관리']")))
        account_manage.click()

        #세팅은 새창으로 전환되어서 포커스 새 창에 맞춰줌
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])

    def ok_btn(self):
        return self.driver.find_element(By.XPATH, "//button[contains(text(),'완료')]")
    
    # 이름 변경 함수
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
    
    def btn_send_code(self):
         return self.driver.find_element(By.XPATH, "//button[contains(text(),'인증메일 발송')]")
    
    def btn_send_code_phone(self):
         return self.driver.find_element(By.XPATH, "//button[contains(text(),'인증 요청')]")
    
    

    def update_email(self, new_email):
        wait = WebDriverWait(self.driver, 10)
        update_icon_locator = (By.XPATH, "//button[@type='button' and contains(@class,'MuiIconButton-root')]")

        # 요소가 나타날 때까지 기다림
        update_icons = wait.until(EC.presence_of_all_elements_located(update_icon_locator))
        update_icons[1].click()

        input_email = self.driver.find_element(By.XPATH, "//input[@placeholder='이메일']")

        input_email.send_keys(Keys.CONTROL+"a", Keys.DELETE)
        input_email.send_keys(new_email)
        
        return new_email
    
    def error_mag(self):
        # 이메일 에러 메세지 가져오기
        msg_locator = (By.XPATH, "//p[contains(@class,'MuiFormHelperText-root') and contains(@class,'Mui-error')]")
        msg_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(msg_locator))
        return msg_element.text

    def wait_and_send_input_code(self):
        code_locator = (By.NAME, "code")
        # 요소가 보일 때까지 기다림
        input_code = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(code_locator)
        )
        # 값 입력
        input_code.send_keys("000000")

    def update_phone(self, new_num):
        wait = WebDriverWait(self.driver, 10)
        update_icon_locator = (By.XPATH, "//button[@type='button' and contains(@class,'MuiIconButton-root')]")
        # 요소가 나타날 때까지 기다림
        update_icons = wait.until(EC.presence_of_all_elements_located(update_icon_locator))
        update_icons[2].click()
        input_num = self.driver.find_element(By.XPATH, "//input[@placeholder='휴대폰 번호']")
        #input_num.send_keys(Keys.CONTROL+"a", Keys.DELETE)
        input_num.send_keys(new_num)
        return input_num
    
    def phone_input(self):
        return self.driver.find_element(By.XPATH, "//input[@placeholder='휴대폰 번호']")

    
    def error_phone(self):
        msg_locator = (By.XPATH, "//p[contains(@class,'MuiFormHelperText-root') and contains(@class,'Mui-error')]")
        msg_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(msg_locator))
        return msg_element.text

    def update_password(self, pw, new_pw):
        wait = WebDriverWait(self.driver, 10)
        update_icon_locator = (By.XPATH, "//button[@type='button' and contains(@class,'MuiIconButton-root')]")
        # 요소가 나타날 때까지 기다림
        update_icons = wait.until(EC.presence_of_all_elements_located(update_icon_locator))
        update_icons[3].click()
        input_now_pw = self.driver.find_element(By.XPATH, "//input[@placeholder='비밀번호']")
        input_new_pw = self.driver.find_element(By.XPATH, "//input[@placeholder='새 비밀번호']")
        #input_num.send_keys(Keys.CONTROL+"a", Keys.DELETE)
        input_now_pw.send_keys(pw)
        input_new_pw.send_keys(new_pw)
        return input_new_pw
  
    def error_new_password(self):
        # 새 비밀번호 입력 시 에러 메세지
        error_new_msg_locator = (By.XPATH, "//p[contains(@class,'MuiTypography-root') and contains(@class,'MuiTypography-body1')]")
        error_new_msg_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(error_new_msg_locator))
        return error_new_msg_element.text
    
    def error_now_password(self):
        # 현재 비밀번호 에러 메세지
        error_now_msg_locator = (By.XPATH, "//p[contains(@class,'MuiFormHelperText-root') and contains(@class,'Mui-error')]")
        error_now_msg_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(error_now_msg_locator))
        return error_now_msg_element.text
    
    # 비밀번호 변경 성공 후 env에서 값 바꾸기
    # def update_env(self, new_pw):
    #     with open(".env", "r") as f:
    #         lines = f.readlines()
    #     with open(".env", "w") as f:
    #         for line in lines:
    #             if line.startswith("PASSWORD5="):
    #                 f.write(f"PASSWORD5={new_pw}\n")
    #             else:
    #                 f.write(line)
