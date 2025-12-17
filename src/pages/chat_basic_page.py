import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime

class ChatBasicPage:
    TEXT_AREA = (By.CSS_SELECTOR, ".MuiInputBase-input.MuiInputBase-inputMultiline")
    
    SEND_BUTTON = (By.XPATH, "//button[@aria-label='보내기']")
    SEND_BUTTON_DISB = (By.CSS_SELECTOR, ".MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary")
    SEND_BUTTON_HIDE = (By.CSS_SELECTOR, ".MuiButtonBase-root.Mui-disabled.MuiIconButton-root.Mui-disabled")
    INPUT_OPTIONAL = (By.CSS_SELECTOR, ".MuiButtonBase-root.MuiChip-root")
    LOADING_ICON = (By.CSS_SELECTOR, '[data-testid="arrows-rotateIcon"]')
    NEW_CONVERS = (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat"]')
    EDIT_BUTTON = (By.XPATH, "//button[@aria-label='수정']")
    SCROLL_DOWN_BUTTON = (By.XPATH, "//button[@aria-label='맨 아래로 스크롤']")
    PLUS_BUTTON = (By.CSS_SELECTOR, '[data-testid="plusIcon"]')
    IMAGE_CLICK = (By.XPATH, "//span[text()='이미지 생성']")
    WEB_CLICK = (By.XPATH, "//span[text()='웹 검색']")
    CANCEL_ICON = (By.CSS_SELECTOR, '[data-testid="CancelIcon"]')
    STOP_BUTTON = (By.XPATH, "//button[@aria-label='취소']")
    FILE_UPLOAD = (By.XPATH, "//span[text()='파일 업로드']")
    FILE_INPUT = (By.CSS_SELECTOR, "input[type='file']")
    
    SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
    # LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
    
    def __init__(self, driver, timeout=200):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        
    ## 텍스트 없이 전송버튼 클릭
    def no_textInput_send_btn_click(self):
        send_btn = self.wait.until(
            EC.presence_of_element_located(self.SEND_BUTTON)
        )
        
        assert not send_btn.is_enabled(), "❌ send 버튼이 disabled가 아닙니다."
        
        cancle_btn = self.wait.until(
            EC.element_to_be_clickable(self.CANCEL_ICON)
        )
        cancle_btn.click()
        
    ## 메시지 전송
    def send_message(self, text):
        text_area = self.wait.until(
            EC.presence_of_element_located(self.TEXT_AREA)
        )
        text_area.click()
        text_area.send_keys(text)
        self.driver.find_element(*self.SEND_BUTTON).click()
        
        time.sleep(3)
        
    ## 로딩 아이콘 대기
    def wait_for_loadinngIcon(self):
        self.wait.until(
            EC.presence_of_all_elements_located(self.LOADING_ICON)
        )
        
    ## 새로운 대화창 생성
    def new_conversation(self):
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/ai-helpy-chat"]').click()
        time.sleep(3)
        
    ## 질문 다시 생성
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
        
    ## 대화창에 텍스트 미입력시 전송버튼 숨김 확인
    def send_btn_is_disabled(self):
        print("## 입력창에 아무것도 입력하지 않았을경우 보내기버튼 비활성화 ##")
        
        send_btn = self.wait.until(
            EC.presence_of_element_located(self.SEND_BUTTON)
        )

        assert not send_btn.is_enabled()
        
    ## 대화창에 텍스트 입력시 전송버튼 활성화 확인
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
        
    ## 질문한 텍스트 수정 후 제 질문
    def edit_btn_click(self, text):
        elements = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//p[.//span[@data-status='complete']]")
            )
        )
        if not elements:
            raise Exception("### 완료 상태 span 요소가 없습니다 ###")
        last_element = elements[-1]

        # 화면에 보이도록 스크롤
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_element)
        
        # 스크롤 이동
        time.sleep(2)
        self.scroll_up()
        
        # 마우스 이동 (hover)
        ActionChains(self.driver).move_to_element(last_element).perform()
        time.sleep(1)
        
        edit_btn = self.wait.until(
            EC.visibility_of_element_located(self.EDIT_BUTTON)
        )
        edit_btn.click()
        
        # time.sleep(5)
        text_areas = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, ".//textarea[@name='input']")
            )
        )
        
        if not text_areas:
            raise Exception("### textarea가 없습니다 ###")
        
        target_text_areas = [ta for ta in text_areas if ta.is_displayed()]
        
        if not target_text_areas:
            raise Exception("### text-area가 없습니다.###")
        
        top_textarea = target_text_areas[0]
        
        self.driver.execute_script("arguments[0].click();", top_textarea)
        # top_textarea.click()
        time.sleep(0.2)
        top_textarea.send_keys(Keys.CONTROL + "a")
        top_textarea.send_keys(Keys.DELETE)
        top_textarea.send_keys(text)
        
        # '보내기' 버튼 탐색 및 클릭
        submit_btn = self.wait.until(
            EC.element_to_be_clickable(self.SEND_BUTTON_DISB)
        )
        
        submit_btn.click()
        
    ## 스크린샷 (스크린샷으로 비교)
    def screenshot(self, text):
        if not os.path.exists(self.SCREENSHOT_DIR):
            os.makedirs(self.SCREENSHOT_DIR)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scroll_{text}_{timestamp}.png"
        filepath = os.path.join(self.SCREENSHOT_DIR, filename)
        self.driver.save_screenshot(filepath)
        print(f"스크린샷 저장: {filepath}")
        
    ## 스크롤 상단 이동 
    def scroll_up(self):
        scroll_container = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.css-ovflmb")
            )
        )
        
        self.driver.execute_script("arguments[0].scrollTop = 0;", scroll_container)
        
    ## 스크롤 하단 이동
    def scroll_down(self):
        scroll_down = self.wait.until(
            EC.presence_of_element_located(
                (self.SCROLL_DOWN_BUTTON)
            )
        )
        
        time.sleep(0.5)
        scroll_down.click()
        
    ## 텍스트 조회 답변 클립보드 복사        
    def clipboard_capy_for_text(self):
        elements = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//button[@aria-label='복사']")
            )
        )
        self.screenshot("before")
        
        clipboard_btn = elements[-1]
        clipboard_btn.click()
        
        time.sleep(1.5)
        self.screenshot("after")
        
        
    ## 채팅창 배지 확인
    def chat_badge_check(self, str):
        plus_btn = self.wait.until(
            EC.element_to_be_clickable(self.PLUS_BUTTON)
        )
        plus_btn.click()
        time.sleep(2)
        
        if str == "A":
            image_btn = self.wait.until(
                EC.element_to_be_clickable(self.IMAGE_CLICK)
            )
            image_btn.click()
            time.sleep(2)
            
        elif str == "B":
            image_btn = self.wait.until(
                EC.element_to_be_clickable(self.WEB_CLICK)
            )
            image_btn.click()
            time.sleep(2)
            
        elif str == "C":
            image_btn = self.wait.until(
                EC.element_to_be_clickable(self.FILE_UPLOAD)
            )
            image_btn.click()
            time.sleep(20)
            
    ## 배지 삭제    
    def badge_delete(self):
        cancle_btn = self.wait.until(
            EC.element_to_be_clickable(self.CANCEL_ICON)
        )
        cancle_btn.click()
        time.sleep(2)
        
        assert self.wait.until(
            EC.invisibility_of_element_located(self.CANCEL_ICON)
        ), "❌ cancel 버튼이 삭제되지 않았습니다."
        
    ## 전송 취소
    def chat_stop(self):
        time.sleep(2)
        stop_btn = self.wait.until(
            EC.element_to_be_clickable(self.STOP_BUTTON)
        )
        stop_btn.click()
        
    ## 파일 업로드
    def file_upload(self, path):
        file_input = self.driver.find_element(*self.FILE_INPUT)
        
        file_input.send_keys(path)
        
        time.sleep(10)