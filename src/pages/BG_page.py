from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

class BehaviorGeneral:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 300)
    
    # locators
    TOOL_TAB = (By.XPATH, "//span[text()='도구']")
    BG_TAB = (By.XPATH, "//p[text()='행동특성 및 종합의견']")
    btn_download=(By.XPATH, "//a[normalize-space(text())='생성 결과 다운받기']")
    STOP_ICON = (By.XPATH, "//*[@data-testid='stopIcon']")
    STOP_MESSAGE = (By.XPATH, "//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]")

    SUCCESS_MESSAGE = (By.XPATH, "//p[contains(text(),'입력하신 내용 기반으로 행동특성 및 종합의견을 생성했습니다.')]")
    ADD_INPUT = (By.XPATH, "//textarea[@name='teacher_comment']")

    # actions
    def click_tool_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.TOOL_TAB)).click()
    def click_BG_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.BG_TAB)).click()

    def upload_exel_succes(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.abspath(os.path.join(base_dir, "..", "resources", "student_record_generation_template.xlsx"))
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

    def result_download(self):
        return self.wait.until(EC.element_to_be_clickable(self.btn_download))
    

    
    def wait_success_message(self):
        return self.wait.until(EC.visibility_of_all_elements_located(self.SUCCESS_MESSAGE))
    
    
    def wait_generation_complete(self):
        self.wait.until(
            EC.invisibility_of_element_located(self.STOP_ICON)
        )
        #return self.driver.find_element(*self.STOP_ICON)

    def click_stop_icon(self):
        self.wait.until(EC.element_to_be_clickable(self.STOP_ICON)).click()
    def get_stop_message_text(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.STOP_MESSAGE)).text
        except:
            return None
        
    def send_add_input(self):
        self.wait.until(EC.visibility_of_element_located(self.ADD_INPUT)).send_keys("테스트입니다.")