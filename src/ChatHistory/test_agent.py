from src.pages.agent_page import AgentPage
import time
from src.resources.testdata.test_data import EXPECTED_AGENT_URL, SEARCN_AGENT_KEYWORD


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

def test_search_agent_success(logged_in_driver):
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

    # 검색 결과가 업데이트 될 때까지 5초 기다리기
    time.sleep(5)

    after_result = agent.count_keyword_list(SEARCN_AGENT_KEYWORD)
    print(f"실제 결과: {after_result}")
    assert set(before_result) == set(after_result) and len(before_result) == len(after_result), "❌ 기대 결과와 실제 결과가 일치하지 않습니다."
    print("✅ 검증 성공: 기대 결과와 실제 결과가 일치합니다.")

    print("🔚 [F1HEL-T4] TC 종료")