import pytest
from src.utils.logger import get_logger 
from src.utils import login
from src.config import USERNAME1, PASSWORD1
from src.ChatAdvancedFunc.deep.pages.deep_create_page import DEEPCreatePage

logger = get_logger(__file__)

@pytest.mark.tc("F1HEL_T162") 
@pytest.mark.xfail(reason="심층조사 생성 화면 진입 시 입력값 자동 초기화 미구현")
def test_deep_input_reset_rules(driver):
  """
  입력값 초기화 검증
  - 심층조사 생성 화면 재진입 시
    이전에 입력한 값(주제/지시사항)이 자동으로 초기화되어야 함
  - 현재는 초기화되지 않아 xfail로 관리
  """

  logger.info("\n==============================")
  logger.info("[TEST START] DEEP Input Reset Rules Validation")

  try:
    login(driver, USERNAME1, PASSWORD1)
    logger.info("[STEP] 관리자 로그인 완료")

    deep_page = DEEPCreatePage(driver)

    deep_page.click_tool_tab()
    deep_page.click_deep_tab()
    logger.info("[STEP] 심층 조사 화면 진입")

    deep_page.clear_inputs()
    deep_page.enter_topic("AI 모델의 성능 비교")
    deep_page.enter_instruction(
        "최신 GPT, Gemini 모델의 차이를 표로 정리하라. "
        "참고한 근거를 단계별로 제시하라."
    )
    logger.info("[STEP] 주제/지시사항 입력 완료")
    
    is_enabled = deep_page.is_create_button_enabled()
    logger.info(f"[ASSERT] 생성 버튼 활성화 여부: {is_enabled}")
    
    if not is_enabled:
          logger.error("[ASSERT FAIL] 생성 버튼이 비활성화 상태")
    assert is_enabled is True

    deep_page.click_create()
    deep_page.click_regenerate()
    logger.info("[STEP] 생성 -> 다시 생성 클릭")

    logger.info("[WAIT] 심층 조사 생성 완료 대기 (STOP 아이콘 사라질 때까지)")
    deep_page.wait_generation_complete()
    
    success_message = deep_page.wait_success_message()
    logger.info("[ASSERT] 생성 완료 메시지 노출 여부 확인")

    if not success_message.is_displayed():
        logger.error("[ASSERT FAIL] 생성 완료 메시지 미노출")
    assert success_message.is_displayed()

    # 다시 심층조사 생성 화면 진입
    deep_page.click_newchat_tab()
    logger.info("[STEP] 새 대화 진입")
        
    deep_page.click_tool_tab()
    deep_page.click_deep_tab()
    logger.info("[STEP] 심층조사 탭 재진입")

    # 입력값 초기화 여부 확인
    topic_value = deep_page.get_topic_value()
    instruction_value = deep_page.get_instruction_value()

    logger.info(f"[RESULT] topic_value: '{topic_value}'")
    logger.info(f"[RESULT] instruction_value: '{instruction_value}'")
    logger.info("[EXPECT] 모든 입력값이 초기화되어 있어야 함")
    
    if topic_value != "":
      logger.error(f"[ASSERT FAIL] 주제 입력값 초기화 실패: '{topic_value}'")
    if instruction_value != "":
      logger.error(f"[ASSERT FAIL] 지시사항 입력값 초기화 실패: '{instruction_value}'")
    
    assert topic_value == "", "주제 입력값이 초기화되지 않음"
    assert instruction_value == "", "지시사항 입력값이 초기화되지 않음"

    logger.info("[ASSERT PASS] 입력값 자동 초기화 확인")

  except Exception:
      logger.exception("[TEST ERROR] 테스트 중 예외 발생")
      raise

  finally:
    logger.info("[TEST END] DEEP Input Reset Rules Validation")
    logger.info("==============================\n")
