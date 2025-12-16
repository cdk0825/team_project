from src.pages.agent_page import AgentPage
from src.resources.testdata.test_data import EXPECTED_AGENT_URL, SEARCN_AGENT_KEYWORD, NON_EXISTENT_KEYWORD
import pytest

def test_agent_lists(logged_in_driver):
    print("\n🆕 [F1HEL-T4] TC 실행")
    driver = logged_in_driver
    agent = AgentPage(driver)
    agent.side_menu.click_agent_search_btn()

    current_url = driver.current_url
    assert EXPECTED_AGENT_URL in current_url, f"❌ 에이전트 탐색 페이지로 이동 실패. 현재 URL: {current_url}"
    print("✅ 검증 성공: 에이전트 탐색 페이지로 이동했습니다.")

    is_agent_list_present = agent.check_agent_list()
    print(is_agent_list_present)
    assert is_agent_list_present, f"❌ 에이전트 목록을 찾지 못했습니다."
    print("✅ 액션: 에이전트 목록 확인됨")
    print("🔚 [F1HEL-T4] TC 종료")

@pytest.mark.xfail(reason="기본 제공 에이전트 검색 불가")
def test_agent_search_success(logged_in_driver):
    print("\n🆕 [F1HEL-T5] TC 실행")
    driver = logged_in_driver
    agent = AgentPage(driver)
    agent.side_menu.click_agent_search_btn()

    current_url = driver.current_url
    assert EXPECTED_AGENT_URL in current_url, f"❌ 에이전트 탐색 페이지로 이동 실패. 현재 URL: {current_url}"
    print("✅ 검증 성공: 에이전트 탐색 페이지로 이동했습니다.")

    before_result = agent.count_keyword_list(SEARCN_AGENT_KEYWORD)
    print(f"기대 결과: {before_result}")
    agent.input_search_keyword(SEARCN_AGENT_KEYWORD)

    after_result = agent.count_keyword_list(SEARCN_AGENT_KEYWORD)
    print(f"실제 결과: {after_result}")
    assert set(before_result) == set(after_result) and len(before_result) == len(after_result), "❌ 기대 결과와 실제 결과가 일치하지 않습니다."
    print("✅ 검증 성공: 기대 결과와 실제 결과가 일치합니다.")

    print("🔚 [F1HEL-T4] TC 종료")

def test_agent_search_no_result(logged_in_driver):
    print("\n🆕 [F1HEL-T14] TC 실행")
    driver = logged_in_driver
    agent = AgentPage(driver)
    agent.side_menu.click_agent_search_btn()

    agent.input_search_keyword(NON_EXISTENT_KEYWORD)
    is_message_displayed = agent.check_no_result_message_is_displayed()

    assert is_message_displayed is True, f"❌ 검증 실패: 키워드 {NON_EXISTENT_KEYWORD} 검색 후 '검색 결과 없음' 메시지가 10초 내에 표시되지 않았습니다."
    print("✅ 검증 성공: 키워드 {NON_EXISTENT_KEYWORD} 검색 후 '검색 결과 없음' 메시지가 정상적으로 표시되었습니다.")
    print("🔚 [F1HEL-T14] TC 종료")

