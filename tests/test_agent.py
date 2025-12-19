from src.pages.agent_page import AgentPage
from f1_helpychat.data.chat_history_data import EXPECTED_AGENT_URL, SEARCN_AGENT_KEYWORD, NON_EXISTENT_KEYWORD, QA_AGENT_TITLE
import pytest
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def test_agent_lists(logged_in_driver):
    logger.info("--- 🆕 [F1HEL-T4] TC 실행: 에이전트 목록 확인 ---")
    driver = logged_in_driver
    agent = AgentPage(driver)
    agent.side_menu.click_agent_search_btn()

    current_url = driver.current_url
    if EXPECTED_AGENT_URL not in current_url:
        logger.error(f"❌ 에이전트 탐색 페이지로 이동 실패. 현재 URL: {current_url}")
        pytest.fail(f"에이전트 탐색 페이지 이동 실패: {current_url}")

    logger.info("✅ 검증 성공: 에이전트 탐색 페이지로 이동했습니다.")

    is_agent_list_present = agent.get_agent_list().is_displayed()
    logger.info(f"✅ 검증: 에이전트 목록 섹션 표시 상태: {is_agent_list_present}")

    logger.debug(f"에이전트 목록 표시 상태: {is_agent_list_present}")

    if not is_agent_list_present:
        logger.error("❌ 에이전트 목록을 찾지 못했습니다.")
        pytest.fail("에이전트 목록 찾기 실패")
        
    logger.info("✅ 액션: 에이전트 목록 확인됨")
    logger.info("--- 🔚 [F1HEL-T4] TC 종료 ---")

@pytest.mark.xfail(reason="기본 제공 에이전트 검색 불가")
def test_agent_search_success(logged_in_driver):
    logger.info("--- 🆕 [F1HEL-T5] TC 실행: 에이전트 검색 성공 ---")
    driver = logged_in_driver
    agent = AgentPage(driver)
    agent.side_menu.click_agent_search_btn()

    current_url = driver.current_url
    if EXPECTED_AGENT_URL not in current_url:
        logger.error(f"❌ 에이전트 탐색 페이지로 이동 실패. 현재 URL: {current_url}")
        pytest.fail(f"에이전트 탐색 페이지 이동 실패: {current_url}")
    logger.info("✅ 검증 성공: 에이전트 탐색 페이지로 이동했습니다.")

    before_result = agent.count_keyword_list(SEARCN_AGENT_KEYWORD)
    logger.info(f"검색 전 목록 (기대): {before_result}")
    agent.input_search_keyword(SEARCN_AGENT_KEYWORD)

    after_result = agent.count_keyword_list(SEARCN_AGENT_KEYWORD)
    logger.info(f"검색 후 목록 (실제): {after_result}")
    
    if set(before_result) != set(after_result) or len(before_result) != len(after_result):
        logger.error("❌ 기대 결과와 실제 결과가 일치하지 않습니다. (목록 업데이트 실패 또는 결과 불일치)")
        pytest.fail("검색 성공 테스트 실패")
        
    logger.info("✅ 검증 성공: 기대 결과와 실제 결과가 일치합니다.")

    logger.info("--- 🔚 [F1HEL-T5] TC 종료 ---")

def test_agent_search_no_result(logged_in_driver):
    logger.info("--- 🆕 [F1HEL-T14] TC 실행: 에이전트 검색 결과 없음 ---")
    driver = logged_in_driver
    agent = AgentPage(driver)
    agent.side_menu.click_agent_search_btn()

    logger.info(f"액션: 키워드 '{NON_EXISTENT_KEYWORD}' 입력")
    agent.input_search_keyword(NON_EXISTENT_KEYWORD)

    is_message_displayed = agent.check_no_result_message_is_displayed()
    if is_message_displayed is not True:
        logger.error(f"❌ 검증 실패: 키워드 '{NON_EXISTENT_KEYWORD}' 검색 후 '검색 결과 없음' 메시지가 표시되지 않았습니다.")
        pytest.fail("검색 결과 없음 메시지 확인 실패")
        
    logger.info(f"✅ 검증 성공: 키워드 '{NON_EXISTENT_KEYWORD}' 검색 후 '검색 결과 없음' 메시지가 정상적으로 표시되었습니다.")
    logger.info("--- 🔚 [F1HEL-T14] TC 종료 ---")

def test_make_session_using_agent(logged_in_driver):
    logger.info("--- 🆕 [F1HEL-T105] TC 실행: 에이전트를 클릭하여 해당 에이전트로 새 세션 생성 ---")
    driver = logged_in_driver
    agent = AgentPage(driver)
    
    agent.side_menu.click_agent_search_btn()
    agent.input_search_keyword("QA")

    agent.wait_for_skeleton_disappear()
    agent.click_agent_btn()
    agent.wait_for_skeleton_disappear()

    agent_title = agent.get_agent_title()
    assert QA_AGENT_TITLE == agent_title, "❌ 선택한 에이전트로 새로운 세션이 만들어지지 않았습니다."
    logger.info(f"✅ 검증 성공: {agent_title}로 새로운 세션이 생성되었습니다.")

    logger.info("--- 🔚 [F1HEL-T105] TC 종료 ---")

def test_create_agent(logged_in_driver):
    logger.info("--- 에이전트 생성 ---")
    driver = logged_in_driver
    agent = AgentPage(driver)
    agent.side_menu.click_agent_search_btn()

    agent.create_agent()

    message = agent.capture_notistack('create_agent')
    logger.info(f"✅ 스낵바 알림 확인: {message}")
    logger.info("--- 에이전트 생성 종료 ---")


def test_delete_agent(logged_in_driver):
    logger.info("--- 🆕 [F1HEL-T106] TC 실행: 에이전트 삭제 ---")
    driver = logged_in_driver
    agent = AgentPage(driver)
    agent.side_menu.click_agent_search_btn()

    agent.create_agent()
    agent.click_go_back_btn()

    target_agent = agent.get_delete_target_agent()
    agent.scroll_to_bottom()

    agent.click_menu_icon(target=target_agent)
    agent.click_delete_menu_btn()
    agent.click_delete_confirm_btn()

    message = agent.capture_notistack('delete_agent')
    logger.info(f"✅ 스낵바 알림 확인: {message}")
    logger.info("--- 🔚 [F1HEL-T106] TC 종료 ---")
