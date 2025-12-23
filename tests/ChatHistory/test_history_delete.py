from src.utils.logger import get_logger

logger = get_logger(__file__)

# 히스토리 삭제 성공 테스트
def test_delete_history(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T8] TC 실행: 히스토리 삭제 성공 ---")
    main = logged_in_main_page_setup
    
    history_menu_modal = main.find_history_menu(0)
    main.click_delete_btn(history_menu_modal)
    logger.debug("액션: '삭제' 버튼 클릭 (모달 열기)")

    main.click_history_delete_confirm_btn(history_menu_modal)

    main.capture_toast_message(title="delete history")
    logger.info(f"✅ 액션: 인덱스 0의 히스토리 항목 삭제 완료")

    logger.info("✅ 액션: 히스토리 삭제 요청 성공")
    logger.info("--- 🔚 [F1HEL-T8] TC 종료 ---")

def test_history_delete_cancel(logged_in_main_page_setup):
    logger.info("--- 🆕 [F1HEL-T20] TC 실행: 히스토리 삭제 취소 ---")
    main = logged_in_main_page_setup

    history_menu_modal = main.find_history_menu(0)
    main.click_delete_btn(history_menu_modal)
    logger.debug("액션: '삭제' 버튼 클릭 (모달 열기)")

    main.click_cancel_btn(history_menu_modal)

    logger.info("✅ 액션: 히스토리 삭제 취소 요청 성공")
    logger.info("--- 🔚 [F1HEL-T20] TC 종료 ---")