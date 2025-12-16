import pytest
from src.resources.testdata.test_data import MODIFY_TITLE_NAME, FIELDSET_OUTLINE_COLOR, MAX_LENGTH_TITLE

# 히스토리 타이틀 변경 성공 테스트
def test_modify_history_title(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T6] TC 실행")
    main = logged_in_main_page_setup

    before_history_title = main.get_first_history().text
    print(f"변경 전 히스토리 타이틀: {before_history_title}")
    main.modify_history_title(MODIFY_TITLE_NAME, 0)

    after_history_title = main.get_first_history().text
    print(f"변경 후 히스토리 타이틀: {after_history_title}")

    print("🔚 [F1HEL-T6] TC 종료")

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
@pytest.mark.xfail(reason="타이틀 수정 시 최대 입력 가능 길이(100자)와 실제 저장 길이가 다름(50자로 잘림)")
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
    
    is_not_reordered = main.check_modify_and_order(MODIFY_TITLE_NAME, 1)
    if is_not_reordered:
        print(f"✅ 검증 성공: 타이틀 수정으로 항목의 순서가 변경되지 않았습니다.")
    else:
        print(f"❌ 검증 실패: 타이틀 수정 후 항목의 순서가 변경되었습니다.")

    print("🔚 [F1HEL-T12] TC 종료")