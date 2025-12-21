from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class DEEPCreatePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 300)
    
    # locators
    DEEP_TAB = (By.XPATH, "//p[text()='심층 조사']")
    TOOL_TAB = (By.XPATH, "//span[text()='도구']")
    NEWCHAT_TAB = (By.XPATH, "//span[text()='새 대화']")
    
    TOPIC_INPUT = (By.XPATH, "//label[contains(.,'주제')]/following::input[1]")
    INSTRUCTION_AREA = (By.XPATH, "//label[contains(.,'지시사항')]/following::textarea[1]")
    CREATE_BTN = (By.XPATH, "//button[@form='tool-factory-do_deep_research']")
    
    REGENERATE_BTN = (By.XPATH, "//button[contains(@class, 'css-1thd9aa') and text()='다시 생성']")
    
    STOP_ICON = (By.XPATH, "//*[@data-testid='stopIcon']")
    STOP_MESSAGE = (By.XPATH, "//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]")
    
    TOPIC_ERROR_TEXT = (By.XPATH, "//p[text()='1자 이상 500자 이하로 입력해주세요.']")
    INSTRUCTION_ERROR_TEXT = (By.XPATH, "//p[text()='2000자 이하로 입력해주세요.']")
    
    SUCCESS_MESSAGE = (By.XPATH, "//p[contains(text(),'입력하신 내용 기반으로 심층조사 결과를 생성했습니다')]")
    
    DOWNLOAD_BTN = (By.XPATH, "//button[@type='button' and contains(., '다운받기')]")
    MARKDOWN_ITEM = (By.XPATH, "//span[contains(., '마크다운 다운로드')]")
    HWPFILE_ITEM = (By.XPATH, "//span[contains(., 'HWP파일 다운로드')]")  
    
    
    # actions
    def click_tool_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.TOOL_TAB)).click()

    def click_deep_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.DEEP_TAB)).click()
    
    def click_newchat_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.NEWCHAT_TAB)).click()
        
    def clear_topic(self):
        topic = self.wait.until(EC.element_to_be_clickable(self.TOPIC_INPUT))
        topic.click()
        topic.send_keys(Keys.CONTROL, "a")
        topic.send_keys(Keys.BACKSPACE)

    def clear_instruction(self):
        instruction = self.wait.until(EC.element_to_be_clickable(self.INSTRUCTION_AREA))
        instruction.click()
        instruction.send_keys(Keys.CONTROL, "a")
        instruction.send_keys(Keys.BACKSPACE)

    def clear_inputs(self):
        self.clear_topic()
        self.clear_instruction()

    def enter_topic(self, topic):
        self.wait.until(EC.presence_of_element_located(self.TOPIC_INPUT)).send_keys(topic)

    def enter_instruction(self, instruction):
        self.wait.until(EC.presence_of_element_located(self.INSTRUCTION_AREA)).send_keys(instruction)

    def click_create(self):
        self.wait.until(EC.element_to_be_clickable(self.CREATE_BTN)).click()

    def click_regenerate(self):
        self.wait.until(EC.element_to_be_clickable(self.REGENERATE_BTN)).click()

    def wait_generation_complete(self):
        self.wait.until(EC.invisibility_of_element_located(self.STOP_ICON))

    def wait_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))

    def is_download_button_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.DOWNLOAD_BTN)
        ).is_displayed()
    
    def click_download_button(self):
        self.wait.until(
            EC.element_to_be_clickable(self.DOWNLOAD_BTN)
        ).click()

    def is_markdown_item_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.MARKDOWN_ITEM)
        ).is_displayed()

    def is_hwp_item_displayed(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.HWPFILE_ITEM)
        ).is_displayed()
    
    def blur_topic(self):
        # 주제 필드 validation 트리거용
        self.driver.find_element(*self.INSTRUCTION_AREA).click()
    
    def blur_instruction(self):
        self.driver.find_element(By.TAG_NAME, "body").click()
    
    def is_create_button_enabled(self):
        return self.driver.find_element(*self.CREATE_BTN).is_enabled()

    def get_topic_error_text(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.TOPIC_ERROR_TEXT)
            ).text
        except TimeoutException:
            return None
    
    def get_instruction_error_text(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.INSTRUCTION_ERROR_TEXT)
            ).text
        except TimeoutException:
            return None
    
    def click_stop_icon(self):
        self.wait.until(EC.element_to_be_clickable(self.STOP_ICON)).click()

    def get_stop_message_text(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.STOP_MESSAGE)
            ).text
        except TimeoutException:
            raise
    
    def get_topic_value(self):
        return self.driver.find_element(*self.TOPIC_INPUT).get_attribute("value")

    def get_instruction_value(self):
        return self.driver.find_element(*self.INSTRUCTION_AREA).get_attribute("value")