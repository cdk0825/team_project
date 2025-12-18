import pandas as pd
import random
import string

def create_large_excel(path="large_test.xlsx", rows=50000, cols=100, strlen=1000):
    # 랜덤 문자열 생성 함수
    def random_text(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    # 데이터 생성 (랜덤 문자열로 채움)
    data = {f"col{i}": [random_text(strlen) for _ in range(rows)] for i in range(cols)}
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)
    return path

# 실행
create_large_excel("large_test.xlsx")
