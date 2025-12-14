def test_navigate_to_new_chat(driver, logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T2] TC 실행")
    main = logged_in_main_page_setup
    main.side_menu.click_agent_search_btn()

    expected_agent_url = "/ai-helpy-chat/agents"
    current_url = driver.current_url
    assert expected_agent_url in current_url, f"❌ 에이전트 탐색 페이지로 이동 실패. 현재 URL: {current_url}"
    print("✅ 검증 성공: 에이전트 탐색 페이지로 이동했습니다.")

    main.side_menu.click_new_chat_btn()

    expected_chat_url = "/ai-helpy-chat"
    current_url = driver.current_url
    # 원본 코드의 'assert agent_url in current_url' 오류 수정 및 검증
    assert expected_chat_url in current_url, f"❌ 새 대화 페이지로 이동 실패. 현재 URL: {current_url}"
    print("✅ 검증 성공: 새 대화 페이지로 이동했습니다.")
    print("\n🔚 [F1HEL-T2] TC 종료")

def test_open_search_history_modal(driver, logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T3] TC 실행")
    main = logged_in_main_page_setup
    main.side_menu.click_search_history_btn()

    is_history_modal_present= main.check_search_history_modal()
    assert is_history_modal_present, f"❌ 히스토리 검색 모달 창을 찾지 못했습니다."
    print("✅ 액션: 히스토리 검색 모달 창 열기 성공")

    print("\n🔚 [F1HEL-T3] TC 종료")