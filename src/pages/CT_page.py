from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

class ClassTemp:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 300)

    # locators
    TOOL_TAB = (By.XPATH, "//span[text()='도구']")
    CT_TAB = (By.XPATH, "//p[text()='수업지도안']")
    school_lv = (By.XPATH, "//div[@role='combobox'][1]")
    grade_lv = (By.XPATH, "(//div[@role='combobox'])[2]")
    sub = (By.XPATH, "(//div[@role='combobox'])[3]")
    time = (By.XPATH, "(//div[@role='combobox'])[4]")
    achieve = (By.XPATH, "//input[@name='achievement_criteria']")
    DOWNLOAD_BTN = (By.XPATH, "//a[contains(., '생성 결과 다운받기')]")
    
    STOP_ICON = (By.XPATH, "//*[@data-testid='stopIcon']")
    STOP_MESSAGE = (By.XPATH, "//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]")

    SUCCESS_MESSAGE = (By.XPATH, "//p[contains(text(),'입력하신 내용 기반으로 수업 지도안을 생성했습니다.')]")
    ADD_INPUT = (By.XPATH, "//textarea[@name='teacher_comment']")
    
    btn_logout = (By.XPATH, "//p[text()='로그아웃']")

    # actions
    def click_tool_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.TOOL_TAB)).click()
    def click_CT_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.CT_TAB)).click()

    # 학교급 선택
    def click_sch_lv(self):
        self.wait.until(EC.element_to_be_clickable(self.school_lv)).click()
    def get_sch_lvs(self):
        options = self.driver.find_elements(By.XPATH, "//li[@role='option']")
        return [opt.text for opt in options]
    # 학년 선택
    def click_grade_lv(self):
        self.wait.until(EC.element_to_be_clickable(self.grade_lv)).click()
    def get_grade_lvs(self):
        options = self.driver.find_elements(By.XPATH, "//li[@role='option']")
        return [opt.text for opt in options]
    # 과목 선택
    def click_sub(self):
        self.wait.until(EC.element_to_be_clickable(self.sub)).click()
    def get_subs(self):
        options = self.driver.find_elements(By.XPATH, "//li[@role='option']")
        return [opt.text for opt in options]
    # 시간 선택
    def click_time(self):
        self.wait.until(EC.element_to_be_clickable(self.time)).click()
    def get_times(self):
        options = self.driver.find_elements(By.XPATH, "//li[@role='option']")
        return [opt.text for opt in options]
    
    def ele_achieve(self):
        return self.driver.find_element(*self.achieve)
    
    def send_achieve(self):
        return self.driver.find_element(*self.achieve).send_keys("덧셈가능")
    

    def wait_success_message(self):
        return self.wait.until(EC.visibility_of_all_elements_located(self.SUCCESS_MESSAGE))
    
    
    def wait_generation_complete(self):
        self.wait.until(
            EC.invisibility_of_element_located(self.STOP_ICON)
        )
        #return self.driver.find_element(*self.STOP_ICON)


    # def get_wait_generation_complete(self):
    #     return self.wait.until(
    #         EC.invisibility_of_element_located(self.STOP_ICON)
    #     )

    def click_stop_icon(self):
        self.wait.until(EC.element_to_be_clickable(self.STOP_ICON)).click()
    
    def get_stop_message_text(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.STOP_MESSAGE)).text
        except:
            return None
    
    def send_add_input(self):
        self.wait.until(EC.visibility_of_element_located(self.ADD_INPUT)).send_keys("테스트입니다.")

    
    def profile_click(self):
        self.driver.find_element(By.CSS_SELECTOR, '.MuiAvatar-root').click()
    
    def logout(self):
        return self.wait.until(EC.element_to_be_clickable(self.btn_logout)).click()



    def sch_lv_txt(self):
        return self.driver.find_element(*self.school_lv).text
    
    def sub_lv_txt(self):
        return self.driver.find_element(*self.sub).text
    def grade_lv_txt(self):
        return self.driver.find_element(*self.grade_lv).text
    
    def time_txt(self):
        return self.driver.find_element(*self.time).text


