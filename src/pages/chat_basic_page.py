import os
import time
import logging
from src.utils.logger import get_logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===


class ChatBasicPage:
    TEXT_AREA = (By.CSS_SELECTOR, ".MuiInputBase-input.MuiInputBase-inputMultiline")
    TEXT_AREAS = (By.XPATH, ".//textarea[@name='input']")
    COMPLETE = (By.XPATH, "//p[.//span[@data-status='complete']]")
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
        logger.info("✔️ [START] 텍스트 입력 없이 Send 버튼 상태")
        send_btn = self.wait.until(
            EC.presence_of_element_located(self.SEND_BUTTON)
        )
        logger.info("✔️ Send 버튼이 화면에 표시됨")
        
        is_enabled = send_btn.is_enabled()
        logger.info(f"✔️ Send 버튼 활성화 상태 : {is_enabled}")
        
        assert not is_enabled, "❌ send 버튼이 disabled가 아닙니다."
        
        cancle_btn = self.wait.until(
            EC.element_to_be_clickable(self.CANCEL_ICON)
        )
        logger.info("✔️ Cancel 버튼 클릭 시도")
        
        cancle_btn.click()
        logger.info("✔️ [END] Cancel 버튼 클릭 완료")
        
    ## 메시지 전송
    def send_message(self, text):
        logger.info("✔️ [START] 메시지 전송 상태")
        text_area = self.wait.until(
            EC.presence_of_element_located(self.TEXT_AREA)
        )
        logger.info("✔️ 텍스트 입력 가능 상태")
        
        text_area.click()
        logger.info("✔️ 텍스트 입력창 클릭")
        
        text_area.send_keys(text)
        logger.info("✔️ 입력 창에 텍스트 주입")
        
        self.driver.find_element(*self.SEND_BUTTON).click()
        logger.info("✔️ [END] 보내기 버튼 클릭 완료")
        
        time.sleep(3)
        
    ## 로딩 아이콘 대기
    def wait_for_loadinngIcon(self):
        logger.info("✔️ [START] 로딩 아이콘 상태")
        self.wait.until(
            EC.presence_of_all_elements_located(self.LOADING_ICON)
        )
        logger.info("✔️ [END] 로딩 아이콘 대기중")
        
    ## 새로운 대화창 생성
    def new_conversation(self):
        logger.info("✔️ [START] 새로운 대화창")
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/ai-helpy-chat"]').click()
        time.sleep(3)
        logger.info("✔️ [END] 새로운 대화창 클릭 완료")
        
    ## 질문 다시 생성
    def recreate(self):
        logger.info("✔️ [START] 질문 다시 생성")
        elements = self.wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '[data-testid="arrows-rotateIcon"]')
            )
        )
        logger.info("✔️ 질문 다시 생성 아이콘 elements 대기중")
    
        elements[-1].click()
        logger.info(f"✔️ 완료 상태 요소 발견 (총 {len(elements)}개, 마지막 요소 사용)")
        
        self.wait.until(
            EC.presence_of_element_located(self.TEXT_AREA)
        )
        logger.info("✔️ [END] 질문 입력창 확인")
        
    ## 대화창에 텍스트 미입력시 전송버튼 숨김 확인
    def send_btn_is_disabled(self):
        logger.info("✔️ [START] 대화참 미입력시 전송버튼 숨김")
        send_btn = self.wait.until(
            EC.presence_of_element_located(self.SEND_BUTTON)
        )
        logger.info("✔️ 전송 버튼 확인")
        
        is_enabled = not send_btn.is_enabled()
        logger.info(f"✔️ [END] Send 버튼 비활성화 상태: {is_enabled}")
        assert is_enabled
        
    ## 대화창에 텍스트 입력시 전송버튼 활성화 확인
    def send_btn_is_enable(self, text):
        logger.info("✔️ [START] 대화창 입력시 전송버튼 활성화")
        text_area = self.wait.until(
            EC.presence_of_element_located(self.TEXT_AREA)
        )
        text_area.click()
        logger.info("✔️ 대화 입력창 확인")
        
        text_area.send_keys(text)
        logger.info("✔️ 대화창 대화 입력")
        
        send_btn = self.wait.until(
            EC.presence_of_element_located(self.SEND_BUTTON)
        )
        logger.info("✔️ 보내기 버튼 대기중")
        
        is_enabled = send_btn.is_enabled()
        logger.info(f"✔️ [END] Send 버튼 활성화 상태 :{is_enabled}")
        assert is_enabled
        
    ## 질문한 텍스트 수정 후 제 질문
    def edit_btn_click(self, text):
        try:
            logger.info("✔️ [START] 답변 완료 후 수정 버튼 클릭 및 재전송")
            logger.info("✔️ 완료 상태 요소(span) 탐색 시작")
            elements = self.wait.until(
                EC.presence_of_all_elements_located(self.COMPLETE)
            )
            if not elements:
                logger.error("❌ 완료 상태 span 요소가 존재하지 않음") 
                raise Exception("### 완료 상태 span 요소가 없습니다 ###")
            
            last_element = elements[-1]
            logger.info(f"✔️ 완료 상태 요소 발견 (총 {len(elements)}개, 마지막 요소 사용)")
            
            # 화면에 보이도록 스크롤
            logger.info("✔️ 완료 상태 요소로 스크롤 이동")
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                last_element
            )
            
            # 스크롤 이동
            time.sleep(2)
            logger.info("✔️ 화면 스크롤 업 수행")
            self.scroll_up()
            
            # 마우스 이동 (hover)
            logger.info("✔️ 완료 상태 요소 hover 시도")
            ActionChains(self.driver).move_to_element(last_element).perform()
            time.sleep(1)
            
            logger.info("✔️ 수정(edit) 버튼 탐색")
            edit_btn = self.wait.until(
                EC.visibility_of_element_located(self.EDIT_BUTTON)
            )
            logger.info("✔️ 수정(edit) 버튼 클릭")
            edit_btn.click()
            
            # time.sleep(5)
            logger.info("✔️ textarea 탐색 시작")
            text_areas = self.wait.until(
                EC.presence_of_all_elements_located(self.TEXT_AREAS)
            )
            
            
            if not text_areas:
                logger.error("✔️ 화면에 표시된 textarea가 없음")
                raise Exception("### textarea가 없습니다 ###")
            
            target_text_areas = [ta for ta in text_areas if ta.is_displayed()]
            logger.info(f"✔️ 표시된 textarea 개수: {len(target_text_areas)}")
            
            if not target_text_areas:
                raise Exception("### text-area가 없습니다.###")
            
            top_textarea = target_text_areas[0]
            
            logger.info("✔️ textarea 기존 내용 삭제 및 새 텍스트 입력")
            self.driver.execute_script("arguments[0].click();", top_textarea)
            # top_textarea.click()
            time.sleep(0.2)
            top_textarea.send_keys(Keys.CONTROL + "a")
            top_textarea.send_keys(Keys.DELETE)
            top_textarea.send_keys(text)
            
            # '보내기' 버튼 탐색 및 클릭
            logger.info("✔️ 보내기 버튼 탐색")
            submit_btn = self.wait.until(
                EC.element_to_be_clickable(self.SEND_BUTTON_DISB)
            )
            
            logger.info("✔️ Send 버튼 클릭")
            submit_btn.click()
            
            logger.info("✔️ [END] 수정 후 재전송 완료")
        except TimeoutError as e:
            logger.warning("!!! Timeout 발생! 테스트는 계속 진행")
            logger.debug(e)
            
    ## 스크린샷 (스크린샷으로 비교)
    def screenshot(self, text):
        logger.info("✔️ [START] 스크린샷 저장 시도")
        if not os.path.exists(self.SCREENSHOT_DIR):
            os.makedirs(self.SCREENSHOT_DIR)
            logger.info(f"✔️ 스크린샷 디렉토리 생성: {self.SCREENSHOT_DIR}")
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scroll_{text}_{timestamp}.png"
        filepath = os.path.join(self.SCREENSHOT_DIR, filename)
        
        self.driver.save_screenshot(filepath)
        logger.info(f"✔️[END] 스크린샷 저장: {filepath}")
        
    ## 스크롤 상단 이동 
    def scroll_up(self):
        logger.info("✔️ [START] 스크롤 상단 이동 시도")
        scroll_container = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.css-ovflmb")
            )
        )
        
        self.driver.execute_script("arguments[0].scrollTop = 0;", scroll_container)
        logger.info("✔️ [END] 스크롤 상단 이동 완료")
        
    ## 스크롤 하단 이동
    def scroll_down(self):
        logger.info("✔️ [START] 스크롤 하단 이동 시도")
        scroll_down = self.wait.until(
            EC.presence_of_element_located(
                (self.SCROLL_DOWN_BUTTON)
            )
        )
        
        time.sleep(0.5)
        scroll_down.click()
        logger.info("✔️ [END] 스크롤 하단 이동 완료")
        
    ## 텍스트 조회 답변 클립보드 복사        
    def clipboard_capy_for_text(self):
        logger.info("✔️ [START] 답변 복사 버튼 탐색")
        elements = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//button[@aria-label='복사']")
            )
        )
        self.screenshot("before")
        
        if not elements:
            logger.error("❌ 복사 버튼이 존재하지 않음")
            raise Exception("### 복사 버튼이 없습니다 ###")
        
        logger.info(f"✔️ 복사 버튼 개수: {len(elements)}")
        
        clipboard_btn = elements[-1]
        logger.info("✔️ 마지막 복사 버튼 클릭")
        clipboard_btn.click()
        
        time.sleep(1.5)
        self.screenshot("after")
        logger.info("✔️ [END] 클립보드 복사 완료")
        
        
    ## 채팅창 배지 확인
    def chat_badge_check(self, str):
        logger.info(f"✔️ [START] 채팅 배지 선택 시작 (타압: {str})")
        plus_btn = self.wait.until(
            EC.element_to_be_clickable(self.PLUS_BUTTON)
        )
        plus_btn.click()
        logger.info("✔️ 플러스 버튼 클릭")
        time.sleep(2)
        
        if str == "A":
            logger.info("✔️ 이미지 배지 선택")
            image_btn = self.wait.until(
                EC.element_to_be_clickable(self.IMAGE_CLICK)
            )
            image_btn.click()
            time.sleep(2)
            
        elif str == "B":
            logger.info("✔️ 웹 배지 선택")
            image_btn = self.wait.until(
                EC.element_to_be_clickable(self.WEB_CLICK)
            )
            image_btn.click()
            time.sleep(2)
            
        elif str == "C":
            logger.info("✔️ 파일 업로드 배지 선택")
            image_btn = self.wait.until(
                EC.element_to_be_clickable(self.FILE_UPLOAD)
            )
            image_btn.click()
            time.sleep(10)
        
        else:
            logger.warning(f"!!! 알수없는 배지 타입: {str}")
            
        logger.info("✔️ [END] 배지 선택 완료")
            
    ## 배지 삭제    
    def badge_delete(self):
        logger.info("✔️ [START] 배시 삭제 시도")
        cancle_btn = self.wait.until(
            EC.element_to_be_clickable(self.CANCEL_ICON)
        )
        cancle_btn.click()
        logger.info("✔️ cancel 버튼 클릭")
        time.sleep(2)
        
        assert self.wait.until(
            EC.invisibility_of_element_located(self.CANCEL_ICON)
        ), "❌ cancel 버튼이 삭제되지 않았습니다."
        logger.info("✔️ [END] 배지 삭제 완료")
        
    ## 전송 취소
    def chat_stop(self):
        logger.info("✔️ [START] 전송 중단 시도")
        time.sleep(2)
        stop_btn = self.wait.until(
            EC.element_to_be_clickable(self.STOP_BUTTON)
        )
        stop_btn.click()
        logger.info("✔️ [END] 전송 중단 버튼 클릭 완료")
        
    ## 파일 업로드
    def file_upload(self, path):
        logger.info(f"✔️ [START] 파일 업로드 시도: {path}")
        
        file_input = self.driver.find_element(*self.FILE_INPUT)
        file_input.send_keys(path)
        
        logger.info("✔️ 파일 경로 입력 완료")
        time.sleep(10)
        logger.info("✔️ [END] 파일 업로드 완료 (대기 종료)")