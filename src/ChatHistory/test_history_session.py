from src.resources.testdata.test_data import (EXPECTED_AGENT_URL, EXPECTED_CHAT_URL, NEW_SESSION_CHAT_KEYWORD)

# 새 대화 세션 생성 테스트
def test_navigate_to_new_chat(driver, logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T2] TC 실행")
    main = logged_in_main_page_setup
    main.side_menu.click_agent_search_btn()

    current_url = driver.current_url
    assert EXPECTED_AGENT_URL in current_url, f"❌ 에이전트 탐색 페이지로 이동 실패. 현재 URL: {current_url}"
    print("✅ 검증 성공: 에이전트 탐색 페이지로 이동했습니다.")

    main.side_menu.click_new_chat_btn()

    # 원본 코드의 'assert agent_url in current_url' 오류 수정 및 검증
    assert EXPECTED_CHAT_URL in current_url, f"❌ 새 대화 페이지로 이동 실패. 현재 URL: {current_url}"
    print("✅ 검증 성공: 새 대화 페이지로 이동했습니다.")
    print("🔚 [F1HEL-T2] TC 종료")

# 새 채팅을 시작했을 때 세션이 제대로 생성되는지 테스트
def test_history_is_created_from_new_chat(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T15] TC 실행")
    main = logged_in_main_page_setup
    main.setup_function_with_precondition(NEW_SESSION_CHAT_KEYWORD)

    first_history_title = main.get_first_history().text
    chat_id = main.get_chat_id_from_url()

    assert chat_id is not None, "❌ 새로운 채팅 시작 및 메시지 전송 후, URL에 유효한 Chat ID가 생성되지 않았습니다."
    assert first_history_title in NEW_SESSION_CHAT_KEYWORD, "❌ 히스토리 목록이 생성되지 않았습니다."
    print(f"✅ 검증 성공: 현재 세션의 chat_id: {chat_id}")
    
    print("🔚 [F1HEL-T15] TC 종료")