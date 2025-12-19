# 설정값을 모아두는 파이썬 모듈
# 환경변수 값을 사용할 수 있도록 함

import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("ADMIN_ID")
PASSWORD = os.getenv("ADMIN_PW")

USERNAME1 = os.getenv("USER1_ID")
PASSWORD1 = os.getenv("USER1_PW")
USERNAME2 = os.getenv("USER2_ID")
PASSWORD2 = os.getenv("USER2_PW")
USERNAME3 = os.getenv("USER3_ID")
PASSWORD3 = os.getenv("USER3_PW")
USERNAME4 = os.getenv("USER4_ID")
PASSWORD4 = os.getenv("USER4_PW")
USERNAME5 = os.getenv("USER5_ID")
PASSWORD5 = os.getenv("USER5_PW")
