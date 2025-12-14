from src.pages.agent_page import AgentPage

def test_agent_lists(driver, logged_in_driver):
    print("\n🆕 [F1HEL-T4] TC 실행")
    driver = logged_in_driver
    agent = AgentPage(driver)
    agent.side_menu.click_agent_search_btn()

    expected_agent_url = "/ai-helpy-chat/agents"
    current_url = driver.current_url
    assert expected_agent_url in current_url, f"❌ 에이전트 탐색 페이지로 이동 실패. 현재 URL: {current_url}"
    print("✅ 검증 성공: 에이전트 탐색 페이지로 이동했습니다.")

    is_agent_list_present = agent.AGENT_LIST.is_displayed()
    assert is_agent_list_present, f"❌ 에이전트 목록을 찾지 못했습니다."
    print("✅ 액션: 에이전트 목록 확인됨")
    print("\n🔚 [F1HEL-T4] TC 종료")