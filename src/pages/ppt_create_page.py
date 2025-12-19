from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

class PPTCreatePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 300)

    # locators
    TOOL_TAB = (By.XPATH, "//span[text()='도구']")
    PPT_TAB = (By.XPATH, "//p[text()='PPT 생성']")
    NEWCHAT_TAB = (By.XPATH, "//span[text()='새 대화']")
    
    TOPIC_INPUT = (By.XPATH, "//label[contains(.,'주제')]/following::input[1]")
    INSTRUCTION_AREA = (By.XPATH, "//label[contains(.,'지시사항')]/following::textarea[1]")
    CREATE_BTN = (By.XPATH, "//button[@form='tool-factory-create_pptx']")
    
    DEEP_TOGGLE_INPUT = (By.XPATH, "//input[@name='simple_mode']")
    
    REGENERATE_BTN = (By.XPATH, "//button[contains(@class, 'css-1thd9aa') and text()='다시 생성']")
    DOWNLOAD_BTN = (By.XPATH, "//a[contains(., '생성 결과 다운받기')]")
    
    STOP_ICON = (By.XPATH, "//*[@data-testid='stopIcon']")
    STOP_MESSAGE = (By.XPATH, "//div[contains(@class,'MuiAlert-message')]" "//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]")
    
    SECTION_INPUT = (By.XPATH, "//input[@name='section_count']")
    SLIDE_INPUT = (By.XPATH, "//input[@name='slides_count']")
    
    TOPIC_ERROR_TEXT = (By.XPATH, "//p[text()='1자 이상 500자 이하로 입력해주세요.']")
    INSTRUCTION_ERROR_TEXT = (By.XPATH, "//p[text()='2000자 이하로 입력해주세요.']")
    

    # actions
    def click_tool_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.TOOL_TAB)).click()

    def click_ppt_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.PPT_TAB)).click()
    
    def click_newchat_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.NEWCHAT_TAB)).click()

    def clear_inputs(self):
        self.clear_topic_input()
        self.clear_instruction_input()
        self.clear_section_input()
        self.clear_slide_input()
        self.clear_deep_toggle()
    
    def clear_topic_input(self):
        topic_input = self.wait.until(
            EC.element_to_be_clickable(self.TOPIC_INPUT)
        )
        topic_input.click()
        topic_input.send_keys(Keys.CONTROL, "a")
        topic_input.send_keys(Keys.BACKSPACE)
    
    def clear_instruction_input(self):
        instruction = self.wait.until(
            EC.element_to_be_clickable(self.INSTRUCTION_AREA)
        )
        instruction.click()
        instruction.send_keys(Keys.CONTROL, "a")
        instruction.send_keys(Keys.BACKSPACE)
        
    def clear_section_input(self):
        section_input = self.wait.until(
            EC.element_to_be_clickable(self.SECTION_INPUT)
        )
        section_input.click()
        section_input.send_keys(Keys.CONTROL, "a")
        section_input.send_keys(Keys.BACKSPACE)

    def clear_slide_input(self):
        slide_input = self.wait.until(
            EC.element_to_be_clickable(self.SLIDE_INPUT)
        )
        slide_input.click()
        slide_input.send_keys(Keys.CONTROL, "a")
        slide_input.send_keys(Keys.BACKSPACE)
    
    def clear_deep_toggle(self):
        toggle_input = self.wait.until(
            EC.presence_of_element_located(self.DEEP_TOGGLE_INPUT)
        )
        if toggle_input.is_selected():
            toggle_input.click()

            self.wait.until(lambda d: not toggle_input.is_selected())

    def enter_topic(self, topic):
        self.wait.until(EC.presence_of_element_located(self.TOPIC_INPUT)).send_keys(topic)

    def enter_instruction(self, instruction):
        self.wait.until(EC.presence_of_element_located(self.INSTRUCTION_AREA)).send_keys(instruction)

    def is_create_button_enabled(self):
        return self.driver.find_element(*self.CREATE_BTN).is_enabled()

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
        except TimeoutException:
            raise

    def enter_section_input(self, value):
        self.wait.until(EC.presence_of_element_located(self.SECTION_INPUT)).send_keys(value)

    def enter_slide_input(self, value):
        self.wait.until(EC.presence_of_element_located(self.SLIDE_INPUT)).send_keys(value)
    
    def get_topic_value(self):
        return self.driver.find_element(*self.TOPIC_INPUT).get_attribute("value")

    def get_instruction_value(self):
        return self.driver.find_element(*self.INSTRUCTION_AREA).get_attribute("value")

    def get_section_value(self):
        return self.driver.find_element(*self.SECTION_INPUT).get_attribute("value")

    def get_slide_value(self):
        return self.driver.find_element(*self.SLIDE_INPUT).get_attribute("value")
    
    def turn_on_deep_toggle(self):
        toggle_input = self.wait.until(
            EC.presence_of_element_located(self.DEEP_TOGGLE_INPUT)
        )
        if not toggle_input.is_selected():
            toggle_input.click()
            self.wait.until(lambda d: toggle_input.is_selected())
    
    def get_topic_error_text(self):
        try:
            return self.driver.find_element(*self.TOPIC_ERROR_TEXT).text
        except TimeoutException:
            return None
    
    def get_instruction_error_text(self):
        try:
            return self.driver.find_element(*self.INSTRUCTION_ERROR_TEXT).text
        except TimeoutException:
            return None

        
