import pytest
from src.utils import login
from src.ChatAdvancedFunc.ppt.pages.ppt_create_page import PPTCreatePage


def test_success_create(driver):
    """
    PPT 정상 생성 테스트
    - 필수 입력값 입력
    - 심층조사모드 ON
    - 생성 → 다시 생성
    - 다운로드 버튼 노출 확인
    """
    
    print("\n==============================")
    print("[TEST START] PPT Success Create")
    
    # given
    login(driver, "qa3team01@elicer.com", "20qareset25elice!")
    print("[STEP] 관리자 로그인 완료")

    ppt_page = PPTCreatePage(driver)

    # when
    ppt_page.click_tool_tab()
    assert "/tools" in driver.current_url
    print("[STEP] PPT 생성 탭 클릭")

    ppt_page.click_ppt_tab()
    print("[STEP] 입력값 초기화")

    ppt_page.clear_inputs()
    print("[STEP] 주제 입력: 이순신 장군")

    ppt_page.enter_topic("이순신 장군")
    print("[완료] 주제 입력")

    print("[ASSERT] 생성 버튼 활성화 확인")
    assert ppt_page.is_create_button_enabled() is True
    print("[ASSERT PASS] 생성 버튼 활성화 상태")

    ppt_page.enter_instruction("이순신에 대해서 텍스트, 이미지, 표를 활용하여 생성")
    print("[STEP] 지시사항 입력")

    print("[STEP] 심층조사 토글 상태 확인")
    final_toggle_value = ppt_page.turn_on_deep_toggle_if_off()
    assert final_toggle_value == "true"
    print("[ASSERT PASS] 심층조사 토글 ON 확인")

    ppt_page.click_create()
    print("[STEP] 생성 버튼 클릭")

    ppt_page.click_regenerate()
    print("[STEP] 다시 생성 버튼 클릭")

    # then    
    print("[WAIT] PPT 생성 완료 대기 (STOP 아이콘 사라질 때까지)")
    ppt_page.wait_generation_complete()

    download_btn = ppt_page.wait_download_button()
    print("[RESULT] 다운로드 버튼 확인")

    assert download_btn.is_displayed()

    print("[ASSERT PASS] 다운로드 버튼 정상 노출")

    print("[TEST END] PPT Success Create")
    print("==============================\n")