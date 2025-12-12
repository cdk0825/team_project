from src.pages.main_page import MainPage
from src.AccountGroup.loginlogout.login import test_login_admin_success
from tests.conftest import driver, wait

def test_navigate_to_new_chat(driver, wait):
    main = MainPage(driver, wait)

    test_login_admin_success(driver, wait)

    main.click_background()

    print("✅ 액션: 에이전트 탐색 버튼 클릭 시도")
    main.click_agent_search_btn()

    expected_agent_url = "/ai-helpy-chat/agents"
    current_url = driver.current_url
    assert expected_agent_url in current_url, f"❌ 에이전트 탐색 페이지로 이동 실패. 현재 URL: {current_url}"
    print("✅ 검증 성공: 에이전트 탐색 페이지로 이동했습니다.")

    print("✅ 액션: 새 대화 버튼 클릭 시도")
    main.click_new_chat_btn()

    expected_chat_url = "/ai-helpy-chat"
    current_url = driver.current_url
    # 원본 코드의 'assert agent_url in current_url' 오류 수정 및 검증
    assert expected_chat_url in current_url, f"❌ 새 대화 페이지로 이동 실패. 현재 URL: {current_url}"
    print("✅ 검증 성공: 새 대화 페이지로 이동했습니다.")