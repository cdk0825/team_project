from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class QUIZCreatePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 300)
    
    # locators
    QUIZ_TAB = (By.XPATH, "//p[text()='퀴즈 생성']")
    TOOL_TAB = (By.XPATH, "//span[text()='도구']")
    NEWCHAT_TAB = (By.XPATH, "//span[text()='새 대화']")

    OPTION_TYPE_SELECT = (By.XPATH, "//*[@id='mui-component-select-quiz_configs.0.option_type']")
    OPTION_TYPE_SINGLE = (By.XPATH, "//li[@data-value='0']")  # 객관식(단일)
    OPTION_TYPE_MULTI = (By.XPATH, "//li[@data-value='1']")   # 객관식(복수)
    OPTION_TYPE_SUBJECTIVE = (By.XPATH, "//li[@data-value='3']")  # 주관식
    
    DIFFICULTY_SELECT = (By.XPATH,"//*[@id='mui-component-select-quiz_configs.0.difficulty']")
    DIFFICULTY_HIGH = (By.XPATH, "//li[@data-value='Level3']")  # 상
    DIFFICULTY_MIDDLE = (By.XPATH, "//li[@data-value='Level2']")  # 중
    DIFFICULTY_LOW = (By.XPATH, "//li[@data-value='Level1']")  # 하

    TOPIC_TEXTAREA = (By.XPATH, "//textarea[@name='content' and @placeholder='퀴즈 주제를 입력해주세요.']")
    TOPIC_ERROR_TEXT = (By.XPATH, "//p[contains(text(),'1자 이상 입력해주세요.')]")

    CREATE_BTN = (By.XPATH, "//button[@form='tool-factory-create_quiz_from_context']")
    REGENERATE_BTN = (By.XPATH, "//button[contains(@class,'css-1thd9aa') and normalize-space(.)='다시 생성']")

    STOP_ICON = (By.XPATH, "//*[@data-testid='stopIcon']" )
    STOP_MESSAGE = (By.XPATH, "//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]")

    SUCCESS_MESSAGE = (By.XPATH, "//p[contains(text(),'입력하신 내용 기반으로 퀴즈를 생성했습니다')]")
    QUESTION_ICON = (By.XPATH, "//*[contains(@data-testid,'square-question')]")
    LEARNING_GOAL_TITLE = (By.XPATH, "//p[contains(text(),'학습 목표')]")
    OPTION_A = (By.XPATH, "//div[contains(@class,'MuiPaper-root') and normalize-space(.)='A']")
    EXPLANATION_TITLE = (By.XPATH, "//p[contains(normalize-space(.),'해설')]")
    
    # actions
    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)
    
    def click_tool_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.TOOL_TAB)).click()
        
    def click_quiz_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.QUIZ_TAB)).click()
        
    def clear_inputs(self):
        self.clear_topic()

    def clear_topic(self):
        topic = self.wait.until(EC.element_to_be_clickable(self.TOPIC_TEXTAREA))
        topic.click()
        topic.send_keys(Keys.CONTROL, "a")
        topic.send_keys(Keys.BACKSPACE)
        
    def select_option_type(self):
        self.wait.until(EC.element_to_be_clickable(self.OPTION_TYPE_SELECT)).click()

    def select_difficulty(self):
        self.wait.until(EC.element_to_be_clickable(self.DIFFICULTY_SELECT)).click()

    def select_option_type_single(self):
        select = self.wait.until(EC.presence_of_element_located(self.OPTION_TYPE_SELECT))
        self.js_click(select)
        option = self.wait.until(EC.presence_of_element_located(self.OPTION_TYPE_SINGLE))
        self.js_click(option)

    def select_option_type_multi(self):
        select = self.wait.until(EC.presence_of_element_located(self.OPTION_TYPE_SELECT))
        self.js_click(select)
        option = self.wait.until(EC.presence_of_element_located(self.OPTION_TYPE_MULTI))
        self.js_click(option)

    def select_option_type_subjective(self):
        select = self.wait.until(EC.presence_of_element_located(self.OPTION_TYPE_SELECT))
        self.js_click(select)
        option = self.wait.until(EC.presence_of_element_located(self.OPTION_TYPE_SUBJECTIVE))
        self.js_click(option)

    def select_difficulty_high(self):
        select = self.wait.until(EC.presence_of_element_located(self.DIFFICULTY_SELECT))
        self.js_click(select)
        option = self.wait.until(EC.presence_of_element_located(self.DIFFICULTY_HIGH))
        self.js_click(option)

    def select_difficulty_middle(self):
        select = self.wait.until(EC.presence_of_element_located(self.DIFFICULTY_SELECT))
        self.js_click(select)
        option = self.wait.until(EC.presence_of_element_located(self.DIFFICULTY_MIDDLE))
        self.js_click(option)

    def select_difficulty_low(self):
        select = self.wait.until(EC.presence_of_element_located(self.DIFFICULTY_SELECT))
        self.js_click(select)
        option = self.wait.until(EC.presence_of_element_located(self.DIFFICULTY_LOW))
        self.js_click(option)
    
    def enter_topic(self, topic):
        self.wait.until(EC.presence_of_element_located(self.TOPIC_TEXTAREA)).send_keys(topic)
    
    def get_topic_error_text(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.TOPIC_ERROR_TEXT)).text
        except:
            return None

    def is_create_button_enabled(self):
        return self.driver.find_element(*self.CREATE_BTN).is_enabled()

    def click_create(self):
        self.wait.until(EC.element_to_be_clickable(self.CREATE_BTN)).click()

    def click_regenerate(self):
        self.wait.until(EC.element_to_be_clickable(self.REGENERATE_BTN)).click()

    def wait_generation_complete(self):
        self.wait.until(EC.invisibility_of_element_located(self.STOP_ICON))
    
    def click_stop_icon(self):
        self.wait.until(EC.element_to_be_clickable(self.STOP_ICON)).click()

    def get_stop_message_text(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.STOP_MESSAGE)).text
        except:
            return None
    
    def wait_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))

    def is_question_displayed(self):
        return self.wait.until(EC.visibility_of_element_located(self.QUESTION_ICON)).is_displayed()

    def is_learning_goal_displayed(self):
        return self.wait.until(EC.visibility_of_element_located(self.LEARNING_GOAL_TITLE)).is_displayed()

    def is_option_displayed(self):
        return self.wait.until(EC.visibility_of_element_located(self.OPTION_A)).is_displayed()

    def is_explanation_displayed(self):
        return self.wait.until(EC.visibility_of_element_located(self.EXPLANATION_TITLE)).is_displayed()
