from src.resources.testdata.test_data import NEW_KEYWORD, MODIFY_TITLE_NAME

# 히스토리 검색 모달창 확인 테스트
def test_open_search_history_modal(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T3] TC 실행")
    main = logged_in_main_page_setup
    main.side_menu.click_search_history_btn()

    is_history_modal_present= main.check_search_history_modal()
    assert is_history_modal_present, f"❌ 히스토리 검색 모달 창을 찾지 못했습니다."
    print("✅ 액션: 히스토리 검색 모달 창 열기 성공")

    print("🔚 [F1HEL-T3] TC 종료")

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