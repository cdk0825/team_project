from src.resources.testdata.test_data import EXPECTED_AGENT_URL, EXPECTED_CHAT_URL, FIELDSET_OUTLINE_COLOR, MAX_LENGTH_TITLE

import time

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

# 히스토리 검색 모달창 확인 테스트
def test_open_search_history_modal(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T3] TC 실행")
    main = logged_in_main_page_setup
    main.side_menu.click_search_history_btn()

    is_history_modal_present= main.check_search_history_modal()
    assert is_history_modal_present, f"❌ 히스토리 검색 모달 창을 찾지 못했습니다."
    print("✅ 액션: 히스토리 검색 모달 창 열기 성공")

    print("🔚 [F1HEL-T3] TC 종료")

# 히스토리 타이틀 변경 성공 테스트
def test_modify_history_title(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T6] TC 실행")
    main = logged_in_main_page_setup

    before_history_title = main.get_first_history().text
    print(f"변경 전 히스토리 타이틀: {before_history_title}")
    main.modify_first_history()

    time.sleep(5)
    after_history_title = main.get_first_history().text
    print(f"변경 후 히스토리 타이틀: {after_history_title}")

    print("🔚 [F1HEL-T6] TC 종료")

# 히스토리 삭제 성공 테스트
def test_delete_history(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T8] TC 실행")
    main = logged_in_main_page_setup
    before_total_histories = main.count_all_history_items()
    print(f"삭제 전 히스토리 개수: {before_total_histories}")

    main.scroll_to_top()

    main.delete_first_history()
    time.sleep(5)

    after_total_histories = main.count_all_history_items()
    print(f"삭제 후 히스토리 개수: {after_total_histories}")

    assert before_total_histories - 1 == after_total_histories, "❌ 히스토리 삭제가 정상적으로 이루어지지 않았습니다."
    print("✅ 액션: 히스토리 삭제 성공")
    print("🔚 [F1HEL-T8] TC 종료")

# 히스토리 타이틀 변경 시 입력값을 공백으로 주었을 때 테스트
def test_modify_history_title_to_empty(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T10] TC 실행")
    main = logged_in_main_page_setup

    fieldset_color, is_enabled = main.modify_history_title_empty()
    assert fieldset_color == FIELDSET_OUTLINE_COLOR, "❌ fieldset의 outline 색상이 제대로 변경되지 않았습니다."
    print(f"✅ fieldset outline 색상: {fieldset_color}")

    assert not is_enabled, "❌ 저장 버튼이 비활성화 되지 않았습니다."
    print(f"✅ 저장 버튼 활성화 상태: {is_enabled}")
    print("🔚 [F1HEL-T10] TC 종료")

# 히스토리 타이틀 최대 글자수로 변경 테스트
def test_max_length_title_edit_and_verification(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T11] TC 실행")
    main = logged_in_main_page_setup
    before_text_length = len(MAX_LENGTH_TITLE)
    print(f"입력된 글자 수: {before_text_length}")

    modified_text = main.modify_history_title_max_length(MAX_LENGTH_TITLE)
    after_text_length = len(modified_text)
    print(f"변경된 타이틀: {modified_text}")
    print(f"변경된 글자 수: {after_text_length}")

    assert before_text_length == after_text_length, "❌ 입력된 글자 수와 변경된 타이틀의 글자 수가 일치하지 않습니다."
    print(f"✅ 타이틀이 정상적으로 변경되었습니다.")
    print("🔚 [F1HEL-T11] TC 종료")

# 히스토리 타이틀 수정 후 목록 정렬 테스트
def test_modify_and_reorder(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T12] TC 실행")
    main = logged_in_main_page_setup
    
    print("🔚 [F1HEL-T12] TC 종료")