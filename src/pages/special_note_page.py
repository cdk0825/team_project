from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

class SpecialNote:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 300)
    # locators
    TOOL_TAB = (By.XPATH, "//span[text()='도구']")
    SN_TAB = (By.XPATH, "//p[text()='세부 특기사항']")
    school_lv = (By.XPATH, "//div[@role='combobox'][1]")
    sub = (By.XPATH, "(//div[@role='combobox'])[2]")
    LISTBOX = (By.XPATH, "//ul[@role='listbox']")
    cho = (By.XPATH, "//li[@role='option' and normalize-space(text())='초등']")
    kuk = (By.XPATH, "//li[@role='option' and normalize-space(text())='국어']")
    btn_create = (By.XPATH,"//button[normalize-space(text())='자동 생성']" )
    btn_recreate = (By.XPATH,"//button[normalize-space(text())='다시 생성']" )
    btn_download=(By.XPATH, "//a[normalize-space(text())='생성 결과 다운받기']")
    joong = (By.XPATH, "//li[@role='option' and normalize-space(text())='중등']")
    soo = (By.XPATH, "//li[@role='option' and normalize-space(text())='수학']")
    btn_logout = (By.XPATH, "//p[text()='로그아웃']")
    btn_rv_history = (By.XPATH, "//a[text()='Remove history']")

    STOP_ICON = (By.XPATH, "//*[@data-testid='stopIcon']" )
    SUCCESS_MESSAGE = (By.XPATH, "//p[contains(text(),'입력하신 내용 기반으로 세부 특기사항을 생성했습니다.')]")
    STOP_MESSAGE = (By.XPATH, "//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]")
    ADD_INPUT = (By.XPATH, "//textarea[@name='teacher_comment']")

    # actions
    def click_tool_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.TOOL_TAB)).click()
    def click_SN_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.SN_TAB)).click()
    
    def click_sch_lv(self):
        self.wait.until(EC.element_to_be_clickable(self.school_lv)).click()

    def sch_lv(self):
        return self.driver.find_element(*self.school_lv).text
    
    def sub_lv(self):
        return self.driver.find_element(*self.sub).text
    
    def get_sch_lvs(self):
        options = self.driver.find_elements(By.XPATH, "//li[@role='option']")
        return [opt.text for opt in options]

    def click_sub(self):
        self.wait.until(EC.element_to_be_clickable(self.sub))
        sub_elem = self.driver.find_element(*self.sub)  # locator 튜플 풀어서 전달
        sub_elem.click()

    def get_subs(self):
        self.wait.until(EC.element_to_be_clickable(self.sub))
        options = self.driver.find_elements(By.XPATH, "//li[@role='option']")
        return [opt.text for opt in options]
    
    def close_listbox(self):
        self.driver.find_element(By.TAG_NAME, "body").click()
    
    def select_cho(self):
        self.wait.until(EC.element_to_be_clickable(self.cho)).click()

    def select_kuk(self):
        self.wait.until(EC.element_to_be_clickable(self.kuk)).click()

    def upload_exel_succes(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.abspath(os.path.join(base_dir, "..", "resources", "student_evaluation_template.xlsx"))
        print("업로드 파일 경로:", file_path)
        print("존재 여부:", os.path.exists(file_path))  # True여야 정상

        upload_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
        upload_input.send_keys(file_path)

    def upload_pdf_succes(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.abspath(os.path.join(base_dir, "..", "resources", "project_OT.pdf"))
        print("업로드 파일 경로:", file_path)
        print("존재 여부:", os.path.exists(file_path))  # True여야 정상

        upload_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
        upload_input.send_keys(file_path)

    def upload_largefile_succes(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.abspath(os.path.join(base_dir, "..", "resources", "large_test.xlsx"))
        print("업로드 파일 경로:", file_path)
        print("존재 여부:", os.path.exists(file_path))  # True여야 정상

        upload_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
        upload_input.send_keys(file_path)

    def click_create(self):
        self.wait.until(EC.element_to_be_clickable(self.btn_create)).click()
    
    def click_recreate(self):
        self.wait.until(EC.element_to_be_clickable(self.btn_recreate)).click()

    def result_download(self):
        return self.wait.until(EC.element_to_be_clickable(self.btn_download))
    
    def select_joong(self):
        self.wait.until(EC.element_to_be_clickable(self.joong)).click()

    def select_soo(self):
        self.wait.until(EC.element_to_be_clickable(self.soo)).click()

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.btn_logout)).click()

    def profile_click(self):
        self.driver.find_element(By.CSS_SELECTOR, '.MuiAvatar-root').click()
    
    def rv_history(self):
        return self.wait.until(EC.element_to_be_clickable(self.btn_rv_history))
    
    # Stop icon
    def wait_generation_complete(self):
        return self.wait.until(EC.invisibility_of_element_located(self.STOP_ICON))
    # 생성 완료 메세지
    def wait_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
    

    def click_stop_icon(self):
        self.wait.until(EC.element_to_be_clickable(self.STOP_ICON)).click()
    
    def get_stop_message_text(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.STOP_MESSAGE)).text
        except:
            return None
    
    def send_add_input(self):
        self.wait.until(EC.visibility_of_element_located(self.ADD_INPUT)).send_keys("테스트입니다.")