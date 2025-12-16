# 히스토리 삭제 성공 테스트
def test_delete_history(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T8] TC 실행")
    main = logged_in_main_page_setup

    main.delete_history(0)

    print("✅ 액션: 히스토리 삭제 성공")
    print("🔚 [F1HEL-T8] TC 종료")

def test_history_delete_cancel(logged_in_main_page_setup):
    print("\n🆕 [F1HEL-T20] TC 실행")
    main = logged_in_main_page_setup
    
    main.delete_history_cancel(0)

    print("🔚 [F1HEL-T20] TC 종료")