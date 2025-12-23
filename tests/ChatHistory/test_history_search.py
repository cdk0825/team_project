from data.chat_history_data import NEW_KEYWORD, MODIFY_TITLE_NAME, SPECIAL_CHAR_SAMPLES, NONE_TEXT
import pytest

from src.utils.logger import get_logger

logger = get_logger(__file__)

# 히스토리 검색 모달창 확인 테스트
def test_open_search_history_modal(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T3] TC 실행: 히스토리 검색 모달창 확인 ---")
    main = logged_in_main_page_setup
    main.side_menu.click_search_history_btn()

    is_history_modal_present = main.check_search_history_modal()
    
    if not is_history_modal_present:
        logger.error("❌ 히스토리 검색 모달 창을 찾지 못했습니다.")
        pytest.fail("히스토리 검색 모달 창 열기 실패")
        
    logger.info("✅ 액션: 히스토리 검색 모달 창 열기 성공")
    logger.info("--- 🔚 [F1HEL-T3] TC 종료 ---")

def test_history_search_case_sensitive(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T18] TC 실행: 히스토리 검색 대소문자 구분 ---")
    main = logged_in_main_page_setup
    
    # 전제 조건: 검색 대상 히스토리 항목 생성
    main.setup_function_with_precondition(NEW_KEYWORD)
    
    lower_new_keyword = NEW_KEYWORD.lower()
    upper_new_keyword = NEW_KEYWORD.upper()

    count_lower = main.search_history_with_keyword(lower_new_keyword)
    count_upper = main.search_history_with_keyword(upper_new_keyword)
    
    logger.info(f"소문자('{lower_new_keyword}') 검색 결과 수: {count_lower}")
    logger.info(f"대문자('{upper_new_keyword}') 검색 결과 수: {count_upper}")
    
    if count_lower != count_upper:
        logger.error("❌ 대소문자 검색 결과가 다릅니다.")
        pytest.fail("대소문자 구분 없는 검색 실패")
        
    logger.info(f"✅ 검증 성공: '{NEW_KEYWORD}'가 대소문자 구분 없이 정상적으로 검색되었습니다.")

    logger.info("--- 🔚 [F1HEL-T18] TC 종료 ---")

def test_search_rename_title(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T19] TC 실행: 타이틀 수정 후 변경된 타이틀로 검색 ---")
    main = logged_in_main_page_setup
    
    # 전제 조건: 검색 대상 히스토리 항목 생성
    main.setup_function_with_precondition(NEW_KEYWORD)

    count_before_keyword = main.search_history_with_keyword(NEW_KEYWORD)
    count_after_keyword = main.search_history_with_keyword(MODIFY_TITLE_NAME)

    logger.info(f"수정 전 '{NEW_KEYWORD}'로 검색 결과: {count_before_keyword}")
    logger.info(f"수정 전 '{MODIFY_TITLE_NAME}'로 검색 결과: {count_after_keyword}")

    # 타이틀 수정 액션
    main.modify_history_title(keyword=MODIFY_TITLE_NAME, i=0)

    # 수정 후 검색
    modified_count_before_keyword = main.search_history_with_keyword(NEW_KEYWORD)
    modified_count_after_keyword = main.search_history_with_keyword(MODIFY_TITLE_NAME)

    logger.info(f"수정 후 '{NEW_KEYWORD}'로 검색 결과: {modified_count_before_keyword}")
    logger.info(f"수정 후 '{MODIFY_TITLE_NAME}'로 검색 결과: {modified_count_after_keyword}")
    
    expected_before = count_before_keyword - 1
    expected_after = count_after_keyword + 1
    
    if modified_count_before_keyword != expected_before or modified_count_after_keyword != expected_after:
        logger.error(f"❌ 변경된 타이틀이 정상적으로 검색되지 않았습니다.")
        logger.error(f"  > '{NEW_KEYWORD}' 기대: {expected_before}, 실제: {modified_count_before_keyword}")
        logger.error(f"  > '{MODIFY_TITLE_NAME}' 기대: {expected_after}, 실제: {modified_count_after_keyword}")
        pytest.fail("타이틀 수정 후 검색 결과 불일치")
        
    logger.info(f"✅ 검증 성공: 변경된 타이틀이 정상적으로 검색되었습니다.")

    logger.info("--- 🔚 [F1HEL-T19] TC 종료 ---")

def test_history_search_with_title(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T36] TC 실행: 타이틀로 히스토리 검색 ---")
    main = logged_in_main_page_setup
    count_keyword = main.search_history_with_keyword(NEW_KEYWORD)

    logger.info(f"✅ {NEW_KEYWORD}가 포함된 {count_keyword}개의 히스토리가 검색되었습니다.")

    logger.info("--- 🔚 [F1HEL-T36] TC 종료 ---")

@pytest.mark.parametrize("special_char, description", SPECIAL_CHAR_SAMPLES)
def test_history_search_with_special_characters(logged_in_main_page_setup, special_char, description):
    logger.info("--- 🆕 [F1HEL-T38] TC 실행: 특수문자로 히스토리 검색 ---")
    main = logged_in_main_page_setup
    logger.info(f"--- TC 실행: {description} ({special_char}) 검색 확인 ---")

    main.setup_function_with_precondition(special_char)

    count = main.search_history_with_keyword(special_char)

    assert count > 0, f"❌ 오류: '{description}'({special_char}) 검색 결과가 0개입니다."

    logger.info("--- 🔚 [F1HEL-T38] TC 종료 ---")

def test_history_search_no_result(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T104] TC 실행: 히스토리 검색 결과가 없을 때 오류 메시지 표시 ---")
    main = logged_in_main_page_setup
    
    main.side_menu.click_search_history_btn()
    main.perform_search(NONE_TEXT)
    is_exist_no_result_msg = main.get_no_result_msg()
    
    assert is_exist_no_result_msg, "❌ 오류: '검색 결과가 없습니다.' 메시지가 표시되지 않습니다."
    logger.info(f"✅ 검증: '검색 결과가 없습니다.' 메시지가 정상적으로 표시되었습니다.")

    logger.info("--- 🔚 [F1HEL-T104] TC 종료 ---")

def test_select_history_in_search_list(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T108] TC 실행: 히스토리 검색 모달의 하단 목록에서 직접 히스토리 선택 ---")
    main = logged_in_main_page_setup

    main.get_first_history().click()
    main.wait_for_skeleton_disappear()

    selected_chat_id = main.extract_chat_id(main.driver.current_url)

    main.side_menu.click_search_history_btn()

    main.get_first_history_id_in_search_modal().click()
    main.wait_for_skeleton_disappear()

    first_history_chat_id = main.extract_chat_id(main.driver.current_url)
    assert selected_chat_id == first_history_chat_id, "❌ 오류: "
    logger.info(f"before: {selected_chat_id}, after: {first_history_chat_id}")    
    
    logger.info("--- 🔚 [F1HEL-T108] TC 종료 ---")

def test_get_modal_histories(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T37] TC 실행: 모달 창에서 히스토리 목록 조회 ---")
    main = logged_in_main_page_setup

    all_history_titles = main.get_all_history_texts()[:20]

    main.side_menu.click_search_history_btn()
    main.wait_for_skeleton_disappear()

    all_history_titles_in_modal = main.get_all_history_texts_in_searched_list()
    min_length = min(len(all_history_titles), len(all_history_titles_in_modal))
    for i in range(min_length):
        try:
            assert all_history_titles[i] == all_history_titles_in_modal[i]
            logger.info(f"✅ {i}번째 타이틀: {all_history_titles[i]}")
        except AssertionError:
            logger.error(f"❌ 불일치 [{i+1}]: \n 메인: '{all_history_titles[i]}' \n 모달: '{all_history_titles_in_modal[i]}'")
            raise 
    logger.info("--- 🔚 [F1HEL-T37] TC 종료 ---")