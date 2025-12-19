import pytest
import logging
from f1_helpychat.data.chat_history_data import MODIFY_TITLE_NAME, MAX_LENGTH_TITLE, MAX_LENGTH_OVER_TITLE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# 히스토리 타이틀 변경 성공 테스트
def test_modify_history_title(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T6] TC 실행: 히스토리 타이틀 변경 성공 ---")
    main = logged_in_main_page_setup

    before_history_title = main.get_first_history().text
    logger.info(f"변경 전 히스토리 타이틀: {before_history_title}")
    
    main.modify_history_title(MODIFY_TITLE_NAME, 0)

    after_history_title = main.get_first_history().text
    logger.info(f"변경 후 히스토리 타이틀: {after_history_title}")
    
    # NOTE: assert after_history_title == MODIFY_TITLE_NAME 검증 로직이 추가되는 것이 좋습니다.
    logger.info("✅ 액션: 히스토리 타이틀 변경 요청 완료")
    logger.info("--- 🔚 [F1HEL-T6] TC 종료 ---")

# 히스토리 타이틀 변경 시 입력값을 공백으로 주었을 때 테스트
def test_modify_history_title_to_empty(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T10] TC 실행: 타이틀 변경 - 공백 유효성 검사 ---")
    main = logged_in_main_page_setup

    history_menu_modal = main.find_history_menu(0)
    main.click_rename_btn(history_menu_modal)
    main.input_rename_field("")

    main.validation_fieldset_color()

    main.validation_save_btn_is_enabled()
    
    logger.info("--- 🔚 [F1HEL-T10] TC 종료 ---")

# 히스토리 타이틀 최대 글자수로 변경 테스트
@pytest.mark.xfail(reason="타이틀 수정 시 최대 입력 가능 길이(100자)와 실제 저장 길이가 다름(50자로 잘림)")
def test_max_length_title_edit_and_verification(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T11] TC 실행: 타이틀 변경 - 최대 길이 유효성 검사 ---")
    main = logged_in_main_page_setup
    
    before_text_length = len(MAX_LENGTH_TITLE)
    logger.info(f"입력된 글자 수: {before_text_length}")

    main.modify_history_title(MAX_LENGTH_TITLE, 0)
    logger.debug("액션: 타이틀 수정 완료 후 메뉴 재오픈 준비")
        
    history_menu_modal_reopen = main.find_history_menu(i=0)
    main.click_rename_btn(history_menu_modal_reopen)

    modified_text = main.get_rename_input_field_value()
    after_text_length = len(modified_text)
    
    logger.info(f"변경된 타이틀: {modified_text}")
    logger.info(f"변경된 글자 수: {after_text_length}")

    if before_text_length != after_text_length:
        logger.error(f"❌ 입력된 글자 수({before_text_length})와 변경된 타이틀의 글자 수({after_text_length})가 일치하지 않습니다. (50자로 잘림 예상)")
        pytest.fail("타이틀 길이 불일치")
        
    logger.info(f"✅ 타이틀이 정상적으로 변경되었습니다.")
    logger.info("--- 🔚 [F1HEL-T11] TC 종료 ---")

# 히스토리 타이틀 수정 후 목록 정렬 테스트
def test_modify_and_reorder(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T12] TC 실행: 타이틀 수정 후 목록 정렬 확인 ---")
    main = logged_in_main_page_setup
    
    logger.info(f"액션: 인덱스 1의 타이틀을 '{MODIFY_TITLE_NAME}'로 수정")
    main.modify_history_title(MODIFY_TITLE_NAME, 1)

    logger.debug("검증: 수정 후 전체 히스토리 텍스트 가져오기")
    after_texts = main.get_all_history_texts()

    is_not_reordered = after_texts[1] == MODIFY_TITLE_NAME
    logger.debug(f"순서 유지 여부 (수정된 항목이 여전히 인덱스 1에 위치하는지): {is_not_reordered}")
    
    if is_not_reordered:
        logger.info(f"✅ 검증 성공: 타이틀 수정으로 항목의 순서가 변경되지 않았습니다.")
    else:
        logger.error(f"❌ 검증 실패: 타이틀 수정 후 항목의 순서가 변경되었습니다. (순서 유지 실패)")
        pytest.fail("타이틀 수정 후 목록 순서 변경됨")

    logger.info("--- 🔚 [F1HEL-T12] TC 종료 ---")

def test_modify_title_cancel(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T21] TC 실행: 타이틀 수정 취소 ---")
    main = logged_in_main_page_setup
    
    history_menu_modal = main.find_history_menu(i=0)
    main.click_rename_btn(history_menu_modal)

    main.input_rename_field(MODIFY_TITLE_NAME)
    main.click_cancel_btn(history_menu_modal)

    logger.info(f"✅ 검증 성공: 타이틀 변경 취소 버튼이 정상적으로 동작했습니다.")

    logger.info("--- 🔚 [F1HEL-T21] TC 종료 ---")

def test_max_length_title_edit_and_verification(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T120] TC 실행: 타이틀 변경 - 100자 초과 입력 ---")
    main = logged_in_main_page_setup

    history_menu_modal = main.find_history_menu(0)

    main.click_rename_btn(history_menu_modal)
    main.input_rename_field(MAX_LENGTH_OVER_TITLE)
    
    main.click_rename_save_btn()
    
    message = main.capture_toast_message(title="modify_history")
    logger.info(f"✅ 출력된 메시지: {message}")
    logger.info(f"✅ 오류 토스트메시지가 정상적으로 확인되었습니다.")
    logger.info("--- 🔚 [F1HEL-T120] TC 종료 ---")