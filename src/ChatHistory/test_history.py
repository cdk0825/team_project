from src.resources.testdata.test_data import (EXPECTED_AGENT_URL, EXPECTED_CHAT_URL, FIELDSET_OUTLINE_COLOR, MAX_LENGTH_TITLE, MODIFY_TITLE_NAME, NEW_SESSION_CHAT_KEYWORD, NEW_KEYWORD)
from src.pages.chat_basic_page import chatBasicPage
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
    main.modify_history_title(MODIFY_TITLE_NAME, 0)

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

    main.delete_history(0)
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

    fieldset_color, is_enabled = main.check_rename_validation_empty()
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

    modified_text = main.check_rename_validation_max_length(MAX_LENGTH_TITLE)
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
    
    is_reordered = main.check_modify_and_order(MODIFY_TITLE_NAME, 1)
    if is_reordered:
        print(f"✅ 검증 성공: 타이틀 수정으로 항목의 순서가 변경되지 않았습니다.")
    else:
        print(f"❌ 검증 실패: 타이틀 수정 후 항목의 순서가 변경되었습니다.")

    print("🔚 [F1HEL-T12] TC 종료")

def test_history_is_created_from_new_chat(driver, logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T15] TC 실행")
    main = logged_in_main_page_setup
    main.setup_function_with_precondition(NEW_SESSION_CHAT_KEYWORD)

    first_history_title = main.get_first_history().text
    chat_id = main.get_chat_id_from_url()

    assert chat_id is not None, "❌ 새로운 채팅 시작 및 메시지 전송 후, URL에 유효한 Chat ID가 생성되지 않았습니다."
    assert first_history_title in NEW_SESSION_CHAT_KEYWORD, "❌ 히스토리 목록이 생성되지 않았습니다."
    print(f"✅ 검증 성공: 현재 세션의 chat_id: {chat_id}")
    
    print("🔚 [F1HEL-T15] TC 종료")

def test_history_search_case_sensitive(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T18] TC 실행")
    main = logged_in_main_page_setup
    main.setup_function_with_precondition(NEW_KEYWORD)
    
    lower_new_keyword = NEW_KEYWORD.lower()
    upper_new_keyword = NEW_KEYWORD.upper()

    count_lower = main.search_history_with_keyword(lower_new_keyword)
    count_upper = main.search_history_with_keyword(upper_new_keyword)
    assert count_lower == count_upper, "❌ 대소문자 검색 결과가 다릅니다."
    print(f"✅ 검증 성공: {NEW_KEYWORD}가 대소문자 구분 없이 정상적으로 검색되었습니다.")

    print("🔚 [F1HEL-T18] TC 종료")

def test_search_rename_title(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T19] TC 실행")
    main = logged_in_main_page_setup
    main.setup_function_with_precondition(NEW_KEYWORD)

    count_before_keyword = main.search_history_with_keyword(NEW_KEYWORD)
    count_after_keyword = main.search_history_with_keyword(MODIFY_TITLE_NAME)

    print(f"{NEW_KEYWORD}로 검색 결과: {count_before_keyword}")
    print(f"{MODIFY_TITLE_NAME}로 검색 결과: {count_after_keyword}")

    main.modify_history_title(keyword=MODIFY_TITLE_NAME)

    modified_count_before_keyword = main.search_history_with_keyword(NEW_KEYWORD)
    modified_count_after_keyword = main.search_history_with_keyword(MODIFY_TITLE_NAME)

    print(f"수정 후 {NEW_KEYWORD}로 검색 결과: {modified_count_before_keyword}")
    print(f"수정 후 {MODIFY_TITLE_NAME}로 검색 결과: {modified_count_after_keyword}")
    
    assert count_before_keyword - 1 == modified_count_before_keyword and count_after_keyword + 1 == modified_count_after_keyword, "❌ 변경된 타이틀이 정상적으로 검색되지 않았습니다."
    print(f"✅ 검증 성공: 변경된 타이틀이 정상적으로 검색되었습니다.")

    print("🔚 [F1HEL-T19] TC 종료")