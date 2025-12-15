from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class chatBasicPage:
    TEXT_AREA = (By.CSS_SELECTOR, ".MuiInputBase-input.MuiInputBase-inputMultiline")
    SEND_BUTTON = (By.XPATH, "//button[@aria-label='보내기']")
    LOADING_ICON = (By.CSS_SELECTOR, '[data-testid="arrows-rotateIcon"]')
    NEW_CONVERS = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat"]')
    EDIT_BUTTON = (By.XPATH, "//button[@aria-label='수정']")
    
    def __init__(self, driver, timeout=200):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        
    def send_message(self, text):
        text_area = self.wait.until(
            EC.presence_of_element_located(self.TEXT_AREA)
        )
        text_area.click()
        text_area.send_keys(text)
        self.driver.find_element(*self.SEND_BUTTON).click()
        
        time.sleep(3)
        
    def wait_for_response(self):
        self.wait.until(
            EC.presence_of_all_elements_located(self.LOADING_ICON)
        )
        
    def new_conversation(self):
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/ai-helpy-chat"]').click()
        time.sleep(3)
        
    def recreate(self):
        elements = self.wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '[data-testid="arrows-rotateIcon"]')
            )
        )
    
        elements[-1].click()
        self.wait.until(
            EC.presence_of_element_located(self.TEXT_AREA)
        )
        
        
    def send_btn_is_disabled(self):
        print("## 입력창에 아무것도 입력하지 않았을경우 보내기버튼 비활성화 ##")
        
        send_btn = self.wait.until(
            EC.presence_of_element_located(self.SEND_BUTTON)
        )

        assert not send_btn.is_enabled()
        
    def send_btn_is_enable(self, text):
        text_area = self.wait.until(
            EC.presence_of_element_located(self.TEXT_AREA)
        )
        
        text_area.click()
        text_area.send_keys(text)
        
        print("## 입력창에 텍스트 입력시 보내기버튼 활성화 ##")
        
        send_btn = self.wait.until(
            EC.presence_of_element_located(self.SEND_BUTTON)
        )
        
        send_btn = self.driver.find_element(
            By.XPATH, "//button[@aria-label='보내기']"
        )
        
        assert send_btn.is_enabled()
        
    def edit_btn_click(self):
        elements = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//p[.//span[@data-status='complete']]")
            )
        )
        if not elements:
            raise Exception("완료 상태 span 요소가 없습니다")
        last_element = elements[-1]

        # 화면에 보이도록 스크롤
        self.driver.execute_script("arguments[0].scrollIntoView(true);", last_element)
        
        # 마우스 이동 (hover)
        ActionChains(self.driver).move_to_element(last_element).perform()

        # 편집 버튼 클릭
        edit_btn = self.wait.until(
            EC.element_to_be_clickable(self.EDIT_BUTTON)
        )
        edit_btn.click()
        
        
        
        time.sleep(5)