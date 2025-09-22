# tests/test_users.py
from fastapi.testclient import TestClient

# `client`는 conftest.py에 정의된 fixture입니다.
# 이 fixture 덕분에 각 테스트 함수는 API에 요청을 보낼 수 있는 TestClient 객체를 인자로 받습니다.
def test_create_user(client: TestClient):
    """
    정상적인 사용자 생성 API('/users/') 호출을 테스트합니다.
    """
    # API에 POST 요청을 보냅니다. json 파라미터로 생성할 사용자 정보를 전달합니다.
    response = client.post(
        "/users/",
        json={"id": "testuser", "email": "test@example.com", "user_name": "Test User"},
    )
    # 응답 상태 코드가 200 (성공)인지 확인합니다.
    assert response.status_code == 200, response.text
    # 응답으로 받은 JSON 데이터를 파싱합니다.
    data = response.json()
    # 응답 데이터의 email과 id가 요청한 데이터와 일치하는지 확인합니다.
    assert data["email"] == "test@example.com"
    assert data["id"] == "testuser"
    # 응답 데이터에 'user_no' 필드가 포함되어 있는지 확인합니다. (DB에 정상적으로 저장되었는지 간접 확인)
    assert "user_no" in data

def test_create_duplicate_user_id(client: TestClient):
    """
    이미 존재하는 ID로 사용자를 생성하려고 할 때, API가 올바르게 400 에러를 반환하는지 테스트합니다.
    """
    # 테스트를 위한 첫 번째 사용자를 생성합니다.
    client.post(
        "/users/",
        json={"id": "testuser", "email": "test@example.com", "user_name": "Test User"},
    )
    # 동일한 'id'를 사용하여 두 번째 사용자 생성을 시도합니다.
    response = client.post(
        "/users/",
        json={"id": "testuser", "email": "another@example.com", "user_name": "Another User"},
    )
    # 응답 상태 코드가 400 (Bad Request)인지 확인합니다.
    assert response.status_code == 400
    # 응답 메시지가 예상대로 "ID already registered"인지 확인합니다.
    assert response.json() == {"detail": "ID already registered"}

def test_read_users(client: TestClient):
    """
    전체 사용자 목록을 조회하는 API('/users/')를 테스트합니다.
    """
    # 테스트 데이터로 두 명의 사용자를 생성합니다.
    client.post(
        "/users/",
        json={"id": "testuser1", "email": "test1@example.com", "user_name": "Test User 1"},
    )
    client.post(
        "/users/",
        json={"id": "testuser2", "email": "test2@example.com", "user_name": "Test User 2"},
    )
    # 전체 사용자 목록을 조회하는 GET 요청을 보냅니다.
    response = client.get("/users/")
    # 응답 상태 코드가 200 (성공)인지 확인합니다.
    assert response.status_code == 200
    data = response.json()
    # 응답으로 받은 사용자 목록의 길이가 2인지 확인합니다.
    assert len(data) == 2
    # 각 사용자의 ID가 올바르게 반환되었는지 확인합니다.
    assert data[0]["id"] == "testuser1"
    assert data[1]["id"] == "testuser2"

def test_read_user(client: TestClient):
    """
    특정 사용자 한 명을 조회하는 API('/users/{user_no}')를 테스트합니다.
    """
    # 테스트할 사용자를 먼저 생성합니다.
    response = client.post(
        "/users/",
        json={"id": "testuser", "email": "test@example.com", "user_name": "Test User"},
    )
    # 생성된 사용자의 'user_no'를 응답에서 추출합니다.
    user_no = response.json()["user_no"]

    # 추출한 'user_no'를 사용하여 특정 사용자 조회 API를 호출합니다.
    response = client.get(f"/users/{user_no}")
    # 응답 상태 코드가 200 (성공)인지 확인합니다.
    assert response.status_code == 200
    data = response.json()
    # 응답 데이터가 생성했던 사용자의 정보와 일치하는지 확인합니다.
    assert data["id"] == "testuser"
    assert data["user_no"] == user_no