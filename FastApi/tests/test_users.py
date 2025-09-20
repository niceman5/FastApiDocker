# tests/test_users.py
from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    """사용자 생성 테스트"""
    response = client.post(
        "/users/",
        json={"id": "testuser", "email": "test@example.com", "user_name": "Test User"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["id"] == "testuser"
    assert "user_no" in data

def test_create_duplicate_user_id(client: TestClient):
    """중복 ID로 사용자 생성 시도 테스트"""
    # 첫 번째 사용자 생성
    client.post(
        "/users/",
        json={"id": "testuser", "email": "test@example.com", "user_name": "Test User"},
    )
    # 동일한 ID로 두 번째 사용자 생성 시도
    response = client.post(
        "/users/",
        json={"id": "testuser", "email": "another@example.com", "user_name": "Another User"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "ID already registered"}

def test_read_users(client: TestClient):
    """전체 사용자 조회 테스트"""
    client.post(
        "/users/",
        json={"id": "testuser1", "email": "test1@example.com", "user_name": "Test User 1"},
    )
    client.post(
        "/users/",
        json={"id": "testuser2", "email": "test2@example.com", "user_name": "Test User 2"},
    )
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == "testuser1"
    assert data[1]["id"] == "testuser2"

def test_read_user(client: TestClient):
    """특정 사용자 조회 테스트"""
    response = client.post(
        "/users/",
        json={"id": "testuser", "email": "test@example.com", "user_name": "Test User"},
    )
    user_no = response.json()["user_no"]

    response = client.get(f"/users/{user_no}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "testuser"
    assert data["user_no"] == user_no