import pytest
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from src.ChatAdvancedFunc.deep.pages.deep_create_page import DEEPCreatePage

def test_success_create(driver):
    """
    DEEP 정상 생성 테스트
    - 주제, 지시사항 입력
    - 생성 → 다시 생성
    - 생성 결과 확인 (생성메시지, 다운받기)
    """
    
    print("\n==============================")
    print("[TEST START] DEEP Success Create")
    
    login(driver, USERNAME1, PASSWORD1)
    print("[STEP] 관리자 로그인 완료")
    
    deep_page = DEEPCreatePage(driver)

    deep_page.click_tool_tab()
    print("[STEP] 도구 탭 클릭")

    deep_page.click_deep_tab()
    print("[STEP] 심층 조사 탭 클릭")

    deep_page.clear_inputs()
    print("[STEP] 주제 / 지시사항 입력값 초기화")

    deep_page.enter_topic("AI 모델의 성능 비교")
    print("[STEP] 주제 입력 완료")

    deep_page.enter_instruction(
        "최신 GPT, Gemini 모델의 차이를 표로 정리하라. "
        "참고한 근거를 단계별로 제시하라."
    )
    print("[STEP] 지시사항 입력 완료")

    is_enabled = deep_page.is_create_button_enabled()
    print(f"[ASSERT] 생성 버튼 활성화 여부: {is_enabled}")
    assert is_enabled is True, "생성 버튼이 활성화되지 않음"

    deep_page.click_create()
    print("[STEP] 생성 버튼 클릭")

    deep_page.click_regenerate()
    print("[STEP] 다시 생성 버튼 클릭")

    print("[WAIT] 심층 조사 생성 완료 대기 (STOP 아이콘 사라질 때까지)")
    deep_page.wait_generation_complete()

    print("[ASSERT] 생성 완료 메시지 확인")
    assert deep_page.wait_success_message().is_displayed()

    is_download_displayed = deep_page.is_download_button_displayed()
    print(f"[ASSERT] 다운받기 버튼 표시 여부: {is_download_displayed}")
    assert is_download_displayed is True, "다운받기 버튼이 표시되지 않음"
    
    deep_page.click_download_button()
    print("[STEP] 다운받기 버튼 클릭")

    assert deep_page.is_markdown_item_displayed() is True
    print("[ASSERT PASS] 마크다운 다운로드 항목 노출")

    assert deep_page.is_hwp_item_displayed() is True
    print("[ASSERT PASS] HWP 파일 다운로드 항목 노출")

    print("[TEST END] DEEP Success Create")
    print("==============================\n")