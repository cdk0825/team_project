import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time



# 테스트 실행 환경 (드라이버) 설정을 위한 Fixture
# @pytest.fixture
# def driver(driver)
# def test_login_admin_success(dirver)

@pytest.fixture
def driver():
    """크롬 브라우저를 열고 테스트 후 닫는 pytest fixture"""
    options = webdriver.ChromeOptions()
    # Headless 모드 실행 (UI 없이 백그라운드 실행, 필요에 따라 활성화)
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)  # Chrome 브라우저 열기
    driver.implicitly_wait(5)  # 암묵적 대기: 요소 로딩 최대 5초까지 대기
    yield driver
    driver.quit()  # 테스트 완료 후 브라우저 닫기
    
    
def test_success_create(driver):
    
    wait = WebDriverWait(driver, 10)
    
    # 1. 로그인 페이지 접속
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    # 2. 사용자명과 비밀번호 입력
    driver.find_element(By.NAME, "loginId").send_keys("qa3team01@elicer.com")
    driver.find_element(By.NAME, "password").send_keys("20qareset25elice!")
    # 3. 로그인 버튼 클릭
    driver.find_element(By.ID, ":r3:").click()
    # 4. 결과 확인: 대시보드로 이동하여 환영 메시지 표시 확인
    # driver.find_element(By.CSS_SELECTOR, '.MuiAvatar-root').click()
    # welcome_id = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/ul/div/div[1]/button/div/div/div[2]/div/p').text
    # welcome_email = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/ul/div/div[1]/button/div/div/div[2]/p').text
    # print("ID:", welcome_id)
    # print("Email:", welcome_email)

    print("로그인 성공")

    
    # 1. 도구탭 클릭
    print("[3] 도구 탭 클릭")
    tool_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='도구']")))
    tool_tab.click()

    # URL 이동 검증 (/tools)
    assert "/tools" in driver.current_url

    # 2. PPT 생성 탭 클릭
    ppt_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='PPT 생성']")))
    ppt_tab.click()
    print("[4] PPT 생성 탭 클릭")

    # # 주제 입력폼 존재 확인
    # wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='topic]")))
    # print("[ASSERT] 주제 입력폼 보이는지 확인")
    
    print("[초기화] 입력값 초기화 시작")
    
    # 주제 input
    topic_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='PPT 주제를 입력하세요'] | //label[contains(.,'주제')]/following::input[1]")
    ))
    topic_input.clear()

    # 지시사항 textarea
    instruction_area = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//textarea[@placeholder='AI가 PPT 생성 시 반영할 사항이나 고려할 점을 알려주세요.'] | //label[contains(.,'지시사항')]/following::textarea[1]")
    ))
    instruction_area.clear()
    
    print("[초기화] 입력값 초기화 완료")
    
    
    # # 3-1. 주제 입력
    # topic_input = driver.find_element(By.XPATH, "//input[@name='topic]")
    # print("[5] 주제 입력 → '이순신 장군'")
    # topic_input.send_keys("이순신 장군")

    # print("[ASSERT] 생성 버튼 활성화 확인")
    # # 생성 버튼 활성화 여부 확인
    # create_btn = driver.find_element(By.XPATH, "//button[@id=':rtr:']")
    # assert create_btn.is_enabled() is True

    # print("[6] 지시사항 입력")
    # # 3-2. 지시사항 입력
    # instruction_area = driver.find_element(By.XPATH, "//textarea[@id=':r7p:']")
    # instruction_area.send_keys("이순신에 대해서 텍스트, 이미지, 표를 활용하여 생성")

    # print("[7] 심층조사 토글 클릭")
    # # 3-5. 심층조사 토글 ON
    # deep_toggle = driver.find_element(By.XPATH, "//input[@id=':r7s:']")
    # deep_toggle.click()

    # print("[ASSERT] 토글 value가 true인지 확인")
    # # ON 되었는지 확인 (value='true')
    # value = deep_toggle.get_attribute("value")
    # assert value == "true"

    # print("[8] 생성 버튼 클릭")
    # # 4. 생성 버튼 클릭
    # create_btn.click()

    # # 생성 중 텍스트 표시 확인
    # loading_text = wait.until(
    #     EC.presence_of_element_located(
    #         (By.XPATH, "//span[contains(text(),'입력하는 정보를 바탕으로 생성 중입니다.')]")
    #     )
    # )
    # assert "생성 중" in loading_text.text

    # print("[9] 다시 생성 버튼 클릭")
    # # 다시 생성 버튼
    # regenerate_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id=':rtv:']")))
    # regenerate_btn.click()

    # print("[ASSERT] 생성 중 문구 포함 확인")
    # # 다시 생성 중 텍스트 확인
    # wait.until(
    #     EC.presence_of_element_located(
    #         (By.XPATH, "//span[contains(text(),'입력하는 정보를 바탕으로 생성 중입니다.')]")
    #     )
    # )

    # print("[10] 생성 완료 대기")
    # # 5. 생성 완료 → '생성 결과 다운받기' 버튼 확인
    # download_btn = wait.until(
    #     EC.presence_of_element_located((By.XPATH, "//a[contains(., '생성 결과 다운받기')]"))
    # )
    # assert download_btn is not None
    
    # print("[ASSERT] 다운로드 버튼이 보이는지 확인")
    # assert download_btn.is_displayed()

    # print("\n🎉 [TEST PASS] PPT 생성 테스트 정상 완료!\n")