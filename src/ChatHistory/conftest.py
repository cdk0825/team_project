import pytest
from src.pages.main_page import MainPage
from src.AccountGroup.loginlogout.test_login import test_login_admin_success

@pytest.fixture
def logged_in_main_page_setup(driver):
    print("\n[SETUP] ⚙️ 액션: 관리자 로그인 시작")
    test_login_admin_success(driver)
    print("[SETUP] ✅ 액션: 관리자 로그인 완료")

    main = MainPage(driver)

    try:
        main.click_background()
        print("[SETUP] ✅ 액션: 초기 모달 창 닫기 성공")
    except Exception as e:
        print(f"[SETUP] ⚠️ 주의: 모달 창 닫기 중 예외 발생 (모달이 이미 닫혔거나 없음): {e}")

    return main

@pytest.fixture
def logged_in_driver(driver):
    print("\n[SETUP] ⚙️ 액션: 관리자 로그인 시작")
    test_login_admin_success(driver)
    print("[SETUP] ✅ 액션: 관리자 로그인 완료")

    main = MainPage(driver)

    try:
        main.click_background()
        print("[SETUP] ✅ 액션: 초기 모달 창 닫기 성공")
    except Exception as e:
        print(f"[SETUP] ⚠️ 주의: 모달 창 닫기 중 예외 발생 (모달이 이미 닫혔거나 없음): {e}")

    return driver