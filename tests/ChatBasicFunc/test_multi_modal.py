import os
from src.utils.logger import get_logger
from src.utils import login
from src.pages.chat_basic_page import ChatBasicPage
from data.config import USERNAME1, PASSWORD1

# === logger 설정 시작 ===
logger  = get_logger(__file__)
# === logger 설정 끝 ===

# === 환경 변수 설정 ===
BASE_URL = os.environ.get("BASE_URL", "https://qaproject.elice.io")
WAIT_TIMEOUT = 200

TEXT1 = "호랑이 배경으로 1월 달력 만들어줘"
TEXT2 = "실사 하늘 사진 만들어줘"
FILE1 = os.path.abspath("C:/Users/cdk08/OneDrive/Desktop/1차프로젝트/TC-cross-check-F1.xlsx")


def test_multi_modal(driver):
    chat_basic_page = ChatBasicPage(driver)
    
    logger.info(" [SETUP] ⚙️ 액션: 관리자 로그인 시작")
    login(driver, USERNAME1, PASSWORD1)
    
    logger.info(" [SETUP] ⚙️ 액션: 1. 채팅창 배지 선택&삭제 시작")
    chat_basic_page.chat_badge_check("A")           ## 배지 선택(A: 이미지 생성, B: 웹 검색)
    chat_basic_page.badge_delete()                  ## 배지 삭제
    logger.info("✅ 검증 성공: 1. 채팅창 배지 선택&삭제 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 2. 채팅창 배지선택 후 텍스트 없이 보내기 시작")
    chat_basic_page.chat_badge_check("A")           ## 배지 선택(A: 이미지 생성, B: 웹 검색)
    chat_basic_page.no_textInput_send_btn_click()   ## 보내기 버튼 disabled
    logger.info("✅ 검증 성공: 2. 채팅창 배지선택 후 텍스트 없이 보내기 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 3. 채팅창 배지선택 후 텍스트 넣어 보내기 시작")
    chat_basic_page.chat_badge_check("A")           ## 배지 선택(A: 이미지 생성, B: 웹 검색)
    chat_basic_page.send_message(TEXT1)             ## 텍스트 입려 후 보내기
    chat_basic_page.wait_for_loadinngIcon()         ## 채팅 완료때까지 대기
    logger.info("✅ 검증 성공: 3. 채팅창 배지선택 후 텍스트 넣어 보내기 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 4. 이미지 생성 후 취소, 재생성 시작")
    chat_basic_page.chat_badge_check("A")           ## 배지 선택(A: 이미지 생성, B: 웹 검색)
    chat_basic_page.send_message(TEXT2)             ## 텍스트 입려 후 보내기
    chat_basic_page.chat_stop()                     ## 생성 취소
    chat_basic_page.recreate()                      ## 재생성
    chat_basic_page.wait_for_loadinngIcon()         ## 채팅 완료때까지 대기
    logger.info("✅ 검증 성공: 4. 이미지 생성 후 취소, 재생성 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 5. 검색어 없이 웹 검색 시작")
    chat_basic_page.chat_badge_check("B")           ## 배지 선택(A: 이미지 생성, B: 웹 검색)
    chat_basic_page.no_textInput_send_btn_click()   ## 보내기 버튼 disabled
    logger.info("✅ 검증 성공: 5. 검색어 없이 웹 검색 완료")
    
    logger.info(" [SETUP] ⚙️ 액션: 6. 검색어 입력 후 웹 검색 시작")
    chat_basic_page.chat_badge_check("B")           ## 배지 선택(A: 이미지 생성, B: 웹 검색)
    chat_basic_page.send_message(TEXT2)             ## 텍스트 입려 후 보내기
    chat_basic_page.wait_for_loadinngIcon()         ## 채팅 완료때까지 대기
    logger.info("✅ 검증 성공: 6. 검색어 입력 후 웹 검색 완료")
    
    """
        selenium으로 자동화 불가능
        <input type="file> 이 DOM에 존재하는 순간이 없어 생성과 동시에 clik() 이벤트가 실행돠어 OS파일창을 불러오는데
        selenium으로는 외부 창을 컨트롤 할 수 없음.
        파일은 첨부되지만 외부 창을 닫을 수 없어 테스트 진행 안됨
    """
    # logger.info(" [SETUP] ⚙️ 액션: 7. 엑셀 파일 업로드와 질문 시작")
    # chat_basic_page.chat_badge_check("C")           ## 배지 선택(A: 이미지 생성, B: 웹 검색)
    # chat_basic_page.file_upload(FILE1)
    # logger.info("✅ 검증 성공: 7. 엑셀 파일 업로드와 질문 완료")