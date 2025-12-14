import pytest
from src.utils import login
from src.ChatAdvancedFunc.ppt.pages.ppt_create_page import PPTCreatePage


def test_ppt_generation_stop(driver):
    """
    PPT 생성 중지 기능 테스트
    1. 주제 / 지시사항 입력
    2. 심층조사모드 ON
    3. 생성 → 다시 생성
    4. STOP 아이콘 클릭
    5. 중지 안내 멘트 노출 확인
    """

    print("\n==============================")
    print("[TEST START] PPT Generation Stop")

    # given
    login(driver, "qa3team01@elicer.com", "20qareset25elice!")
    print("[STEP] 관리자 로그인 완료")

    ppt_page = PPTCreatePage(driver)

    ppt_page.click_tool_tab()
    assert "/tools" in driver.current_url
    print("[STEP] 도구 탭 진입")

    ppt_page.click_ppt_tab()
    print("[STEP] PPT 생성 탭 진입")

    ppt_page.clear_inputs()
    print("[STEP] 입력값 초기화")

    ppt_page.enter_topic("이순신")
    print("[STEP] 주제 입력: 이순신")

    ppt_page.enter_instruction(
        "이순신에 대해서 텍스트, 이미지, 표를 활용하여 생성"
    )
    print("[STEP] 지시사항 입력")

    # when
    ppt_page.click_create()
    print("[STEP] 생성 버튼 클릭")

    ppt_page.click_regenerate()
    print("[STEP] 다시 생성 버튼 클릭")

    ppt_page.click_stop_icon()
    print("[STEP] 생성 중지(STOP) 클릭")

    # then
    stop_message = ppt_page.get_stop_message_text()
    print(f"[RESULT] 중지 멘트: {stop_message}")

    assert stop_message is not None
    assert "요청에 의해 답변 생성을 중지했습니다." in stop_message

    print("[ASSERT PASS] 중지 안내 멘트 정상 노출")
    print("[TEST END] PPT Generation Stop")
    print("==============================\n")
