import os
import pytest

from src.utils.logger import get_logger
from src.utils import login
from src.pages.chat_basic_page import ChatBasicPage
from data.config import USERNAME1, PASSWORD1
from data.chat_basic_data import TEXT1, TEXT2, TEXT3, TEXT4, TEXT5, TEXT6, TEXT7, TEXT8

# === logger 설정 시작 ===
logger = get_logger(__file__)
# === logger 설정 끝 ===

# === 환경 변수 설정 ===
BASE_URL = os.environ.get("BASE_URL", "https://qaproject.elice.io")
WAIT_TIMEOUT = 200


# =====================

# @pytest.mark.skip(reason="임시 비활성화")
def test_chat_basic_flow(driver):
    chat_basic_page = ChatBasicPage(driver)
    
    logger.info(" [SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USERNAME1, PASSWORD1)
    
    logger.info(" [SETUP] ⚙️ 액션: 1. 일반 텍스트 질문 시작")
    chat_basic_page.send_message(TEXT1)
    logger.info(" ✅ 검증 성공: 1. 일반 텍스트 질문 답변 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 2. 다른 맥락 텍스트 질문 시작")
    chat_basic_page.wait_for_loadinngIcon()
    chat_basic_page.send_message(TEXT2)
    logger.info(" ✅ 검증 성공: 2. 다른 맥락 텍스트 질문 답변 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 3. 복잡한 텍스트 질문 시작")
    chat_basic_page.wait_for_loadinngIcon()
    chat_basic_page.send_message(TEXT3)
    logger.info(" ✅ 검증 성공: 3.복잡한 텍스트 질문 답변 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 4. 의미없는(오타) 텍스트 질문 시작")
    chat_basic_page.wait_for_loadinngIcon()
    chat_basic_page.send_message(TEXT4)
    logger.info(" ✅ 검증 성공: 4. 의미없는(오타) 텍스트 질문 답변 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 5. 오타가 포함된 텍스트 질문 시작")
    chat_basic_page.wait_for_loadinngIcon()
    chat_basic_page.send_message(TEXT5)
    logger.info(" ✅ 검증 성공: 5. 오타가 포함된 텍스트 질문 답변 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 6. 연관된 질문을 연속으로 질문 시작")
    chat_basic_page.wait_for_loadinngIcon()
    chat_basic_page.send_message(TEXT6)
    logger.info(" ✅ 검증 성공: 6. 연관된 질문을 연속으로 질문 답변 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 7. 200자 이상 질문 시작")
    chat_basic_page.wait_for_loadinngIcon()
    chat_basic_page.send_message(TEXT7)
    logger.info(" ✅ 검증 성공: 7. 200자 이상 질문 답변 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 8. 대화중 새 대화 테스트 시작")
    chat_basic_page.new_conversation()
    chat_basic_page.send_message(TEXT8)
    logger.info(" ✅ 검증 성공: 8. 대화중 새 대화 태스트 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 9. 일반 텍스트 질문 다시 생성 시작")
    chat_basic_page.send_message(TEXT1)
    chat_basic_page.recreate()
    logger.info(" ✅ 검증 성공: 9. 일반 텍스트 질문 다시 생성 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 10. 일반 대화 전송 버튼 테스트 시작")
    chat_basic_page.send_btn_is_disabled()
    chat_basic_page.send_btn_is_enable(TEXT1)
    logger.info(" ✅ 검증 성공: 10. 일반 대화 전송 버튼 테스트 완료")


# @pytest.mark.skip(reason="임시 비활성화")
def test_chat_edit(driver):
    chat_basic_page = ChatBasicPage(driver)

    logger.info(" [SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USERNAME1, PASSWORD1)
    
    logger.info(" [SETUP] ⚙️ 액션: 1. 일반 텍스트 질문 시작")
    chat_basic_page.send_message(TEXT5)
    logger.info(" ✅ 검증 성공: 1. 일반 텍스트 질문 답변 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 2. 이미 보낸 메시지 수정 시작")
    chat_basic_page.edit_btn_click(TEXT2)
    chat_basic_page.wait_for_loadinngIcon()
    logger.info(" ✅ 검증 성공: 2. 이미 보낸 메시지 수정 완료")