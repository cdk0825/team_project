import pytest
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from src.ChatAdvancedFunc.ppt.pages.ppt_create_page import PPTCreatePage
from src.utils.file_utils import wait_for_download


def test_success_create(driver, download_dir):
    """
    PPT 정상 생성 테스트
    - 필수 입력값 입력
    - 심층조사모드 ON
    - 생성
    - 다운로드 버튼 노출 확인
    """
    
    print("\n==============================")
    print("[TEST START] PPT Success Create")
    
    login(driver, USERNAME1, PASSWORD1)
    print("[STEP] 관리자 로그인 완료")

    ppt_page = PPTCreatePage(driver)

    ppt_page.click_tool_tab()
    assert "/tools" in driver.current_url
    
    print("[STEP] PPT 생성 탭 클릭")
    ppt_page.click_ppt_tab()
    
    print("[STEP] 입력값 초기화")
    ppt_page.clear_inputs()
    
    print("[STEP] 주제 입력: 이순신 장군")
    ppt_page.enter_topic("이순신 장군")
    
    print("[STEP] 지시사항 입력")
    ppt_page.enter_instruction("이순신에 대해서 텍스트, 이미지, 표를 활용하여 생성")
    
    print("[STEP] 섹션 입력: 2")
    ppt_page.enter_section_input(2)
    
    print("[STEP] 슬라이드 입력: 4")
    ppt_page.enter_slide_input(4)
    
    print("[STEP] 심층조사 모드 ON")
    ppt_page.turn_on_deep_toggle()
    
    print("[STEP] 입력값 입력 완료")

    print("[ASSERT] 생성 버튼 활성화 확인")
    assert ppt_page.is_create_button_enabled() is True
    print("[ASSERT PASS] 생성 버튼 활성화 상태")

    ppt_page.click_create()
    print("[STEP] 생성 버튼 클릭")

    ppt_page.click_regenerate()
    print("[STEP] 다시 생성 버튼 클릭")

    print("[WAIT] PPT 생성 완료 대기 (STOP 아이콘 사라질 때까지)")
    ppt_page.wait_generation_complete()

    download_btn = ppt_page.wait_download_button()
    print("[RESULT] 다운로드 버튼 확인")

    assert download_btn.is_displayed()
    print("[ASSERT PASS] 다운로드 버튼 정상 노출")
    
    print("[ASSERT] 다운로드 버튼 클릭")
    download_btn.click()

    downloaded_file = wait_for_download(download_dir, timeout=60)
    print(f"[RESULT] 다운로드된 파일: {downloaded_file}")

    assert downloaded_file is not None, "파일이 다운로드되지 않음"
    assert downloaded_file.endswith(".pptx"), (
        f"다운로드 파일 확장자 오류: {downloaded_file}"
    )

    print("[TEST END] PPT Success Create")
    print("==============================\n")