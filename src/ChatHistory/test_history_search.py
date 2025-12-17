from src.resources.testdata.test_data import NEW_KEYWORD, MODIFY_TITLE_NAME
import logging
import pytest

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

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
    logger.info("--- 🆕 [F1HEL-T19] TC 실행: 타이틀 수정 후 검색 확인 ---")
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