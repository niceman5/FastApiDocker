# tests/test_posts.py
from fastapi.testclient import TestClient

def test_create_post(client: TestClient):
    """게시물 생성 테스트"""
    # 게시물을 작성할 사용자 먼저 생성
    user_response = client.post(
        "/users/",
        json={"id": "postuser", "email": "postuser@example.com", "user_name": "Post User"},
    )
    assert user_response.status_code == 200
    user_no = user_response.json()["user_no"]

    # 게시물 생성
    post_response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "This is a test content.", "user_no": user_no},
    )
    assert post_response.status_code == 200
    data = post_response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test content."
    assert data["user_no"] == user_no
    assert "post_no" in data

def test_create_post_for_nonexistent_user(client: TestClient):
    """존재하지 않는 사용자의 게시물 생성 시도 테스트"""
    response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "This is a test content.", "user_no": 999},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Owner User not found"}