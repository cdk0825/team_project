import strawberry
from typing import List

'''
로컬에서 그래프Ql 사용하기.
실행할 그래프ql 파일 위치로 이동
python -m strawberry dev main 서버 실행 명령어실행
http://0.0.0.0:8000/graphql 으로 실행하라고 설명하지만
실질적으로 http://loalhost:8000/graphql 으로 실행해야 접속가능함
'''

# 1. 데이터 구조 정의(Schema)
@strawberry.type
class User:
    name: str
    age: int
    
# 샘플 제이터
USER_DATA = [
    User(name="제미나이", age=2),
    User(name="홍길동", age=30),
]

# 2. 데이터를 가져오는 방식 정의 (Query)
@strawberry.type
class Query:
    @strawberry.field
    def get_users(self) -> List[User]:
        return USER_DATA
    
    @strawberry.field
    def search_user(self, name: str) -> User:
        for user in USER_DATA:
            if user.name == name:
                return user
        return None

# 3. 스키마 및 서버 설정
schema = strawberry.Schema(query=Query)
    