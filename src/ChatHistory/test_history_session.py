from src.resources.testdata.test_data import (EXPECTED_AGENT_URL, EXPECTED_CHAT_URL, NEW_SESSION_CHAT_KEYWORD)
import logging
import pytest

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# 새 대화 세션 생성 테스트
def test_navigate_to_new_chat(driver, logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T2] TC 실행: 새 대화 세션으로 이동 ---")
    main = logged_in_main_page_setup
    
    # 1. 에이전트 탐색 페이지로 이동
    main.side_menu.click_agent_search_btn()

    current_url = driver.current_url
    if EXPECTED_AGENT_URL not in current_url:
        logger.error(f"❌ 에이전트 탐색 페이지로 이동 실패. 현재 URL: {current_url}")
        pytest.fail(f"에이전트 탐색 페이지 이동 실패: {current_url}")
        
    logger.info("✅ 검증 성공: 에이전트 탐색 페이지로 이동했습니다.")

    # 2. 새 대화 버튼 클릭
    main.side_menu.click_new_chat_btn()

    # URL 검증
    # 원본 코드의 'assert agent_url in current_url' 오류 수정 및 검증
    if EXPECTED_CHAT_URL not in current_url:
        logger.error(f"❌ 새 대화 페이지로 이동 실패. 현재 URL: {current_url}")
        pytest.fail(f"새 대화 페이지 이동 실패: {current_url}")
        
    logger.info("✅ 검증 성공: 새 대화 페이지로 이동했습니다.")
    logger.info("--- 🔚 [F1HEL-T2] TC 종료 ---")

# 새 채팅을 시작했을 때 세션이 제대로 생성되는지 테스트
def test_history_is_created_from_new_chat(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T15] TC 실행: 새 채팅 세션 생성 확인 ---")
    main = logged_in_main_page_setup
    
    # 전제 조건: 새 채팅 시작 및 메시지 전송
    logger.info(f"액션: 키워드 '{NEW_SESSION_CHAT_KEYWORD}'로 새 채팅 시작")
    main.setup_function_with_precondition(NEW_SESSION_CHAT_KEYWORD)

    first_history_title = main.get_first_history().text
    chat_id = main.get_chat_id_from_url()

    if chat_id is None:
        logger.error("❌ 새로운 채팅 시작 및 메시지 전송 후, URL에 유효한 Chat ID가 생성되지 않았습니다.")
        pytest.fail("Chat ID 생성 실패")

    if first_history_title not in NEW_SESSION_CHAT_KEYWORD:
        logger.error("❌ 히스토리 목록이 생성되지 않았습니다.")
        pytest.fail("히스토리 목록 생성 실패")
        
    logger.info(f"✅ 검증 성공: 현재 세션의 chat_id: {chat_id}")
    logger.info("✅ 검증 성공: 히스토리 목록이 정상적으로 생성되었습니다.")
    
    logger.info("--- 🔚 [F1HEL-T15] TC 종료 ---")