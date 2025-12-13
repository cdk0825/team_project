from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class PPTCreatePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 100)

    # locators
    TOOL_TAB = (By.XPATH, "//span[text()='도구']")
    PPT_TAB = (By.XPATH, "//p[text()='PPT 생성']")
    TOPIC_INPUT = (By.XPATH, "//label[contains(.,'주제')]/following::input[1]")
    INSTRUCTION_AREA = (By.XPATH, "//label[contains(.,'지시사항')]/following::textarea[1]")
    CREATE_BTN = (By.XPATH, "//button[@form='tool-factory-create_pptx']")
    
    DEEP_TOGGLE_INPUT = (By.XPATH, "//input[@name='simple_mode']")
    DEEP_TOGGLE_WRAPPER = (By.XPATH, "//input[@name='simple_mode']/parent::span")
    TOGGLE_WRAPPER = (By.XPATH, "//input[@name='simple_mode']/following-sibling::span")
    
    REGENERATE_BTN = (By.XPATH, "//button[contains(@class, 'css-1thd9aa') and text()='다시 생성']")
    DOWNLOAD_BTN = (By.XPATH, "//a[contains(., '생성 결과 다운받기')]")
    
    STOP_ICON = (By.XPATH, "//*[@data-testid='stopIcon']")
    STOP_MESSAGE = (By.XPATH, "//div[contains(@class,'MuiAlert-message')]" "//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]")
    
    SECTION_INPUT = (By.XPATH, "//input[@name='slides_count']")
    SLIDE_INPUT = (By.XPATH, "//input[@name='section_count']")
    
    TOPIC_ERROR_TEXT = (By.XPATH, "//p[text()='1자 이상 500자 이하로 입력해주세요.']")
    INSTRUCTION_ERROR_TEXT = (By.XPATH, "//p[text()='2000자 이하로 입력해주세요.']")
    

    # actions
    def click_tool_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.TOOL_TAB)).click()

    def click_ppt_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.PPT_TAB)).click()

    def clear_inputs(self):
        self.wait.until(EC.presence_of_element_located(self.TOPIC_INPUT)).clear()
        self.wait.until(EC.presence_of_element_located(self.INSTRUCTION_AREA)).clear()

    def enter_topic(self, topic):
        self.wait.until(EC.presence_of_element_located(self.TOPIC_INPUT)).send_keys(topic)

    def enter_instruction(self, instruction):
        self.wait.until(EC.presence_of_element_located(self.INSTRUCTION_AREA)).send_keys(instruction)

    def is_create_button_enabled(self):
        return self.driver.find_element(*self.CREATE_BTN).is_enabled()

    def turn_on_deep_toggle_if_off(self):
        toggle_input = self.driver.find_element(*self.DEEP_TOGGLE_INPUT)
        toggle_wrapper = self.driver.find_element(*self.DEEP_TOGGLE_WRAPPER)

        if toggle_input.get_attribute("value") == "false":
            toggle_wrapper.click()
            WebDriverWait(self.driver, 5).until(
                lambda d: toggle_input.get_attribute("value") == "true"
            )

        return toggle_input.get_attribute("value")  

    def click_create(self):
        self.wait.until(EC.element_to_be_clickable(self.CREATE_BTN)).click()

    def click_regenerate(self):
        self.wait.until(EC.element_to_be_clickable(self.REGENERATE_BTN)).click()

    def wait_download_button(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.DOWNLOAD_BTN)
    )
    
    def wait_generation_complete(self):
        self.wait.until(
            EC.invisibility_of_element_located(self.STOP_ICON)
        )
    
    def click_stop_icon(self):
        self.wait.until(EC.element_to_be_clickable(self.STOP_ICON)).click()

    def get_stop_message_text(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.STOP_MESSAGE)
            ).text
        except:
            return None
    
    def clear_section_input(self):
        self.wait.until(EC.presence_of_element_located(self.SECTION_INPUT)).clear()

    def clear_slide_input(self):
        self.wait.until(EC.presence_of_element_located(self.SLIDE_INPUT)).clear()

    def enter_section_input(self, value):
        self.wait.until(EC.presence_of_element_located(self.SECTION_INPUT)).send_keys(value)

    def enter_slide_input(self, value):
        self.wait.until(EC.presence_of_element_located(self.SLIDE_INPUT)).send_keys(value)

    def get_section_value(self):
        return self.driver.find_element(*self.SECTION_INPUT).get_attribute("value")

    def get_slide_value(self):
        return self.driver.find_element(*self.SLIDE_INPUT).get_attribute("value")
    
    def get_topic_error_text(self):
        try:
            return self.driver.find_element(*self.TOPIC_ERROR_TEXT).text
        except:
            return None
    
    def get_instruction_error_text(self):
        try:
            return self.driver.find_element(*self.INSTRUCTION_ERROR_TEXT).text
        except:
            return None

        
