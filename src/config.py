# 설정값을 모아두는 파이썬 모듈
# 환경변수 값을 사용할 수 있도록 함

import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("ADMIN_ID")
PASSWORD = os.getenv("ADMIN_PW")
