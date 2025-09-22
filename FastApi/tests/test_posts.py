# tests/test_posts.py
from fastapi.testclient import TestClient

# `client`는 conftest.py에 정의된 fixture입니다.
# 이 fixture 덕분에 각 테스트 함수는 API에 요청을 보낼 수 있는 TestClient 객체를 인자로 받습니다.
def test_create_post(client: TestClient):
    """
    정상적인 게시물 생성 API('/posts/') 호출을 테스트합니다.
    """
    # 게시물을 작성하려면 먼저 해당 게시물의 소유자(owner)가 될 사용자가 존재해야 합니다.
    # 따라서 테스트를 위한 사용자를 먼저 생성합니다.
    user_response = client.post(
        "/users/",
        json={"id": "postuser", "email": "postuser@example.com", "user_name": "Post User"},
    )
    # 사용자 생성이 성공했는지 확인합니다.
    assert user_response.status_code == 200
    # 생성된 사용자의 'user_no'를 응답에서 추출합니다. 이 번호는 게시물을 생성할 때 필요합니다.
    user_no = user_response.json()["user_no"]

    # 위에서 생성한 사용자의 'user_no'를 사용하여 게시물 생성을 요청합니다.
    post_response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "This is a test content.", "user_no": user_no},
    )
    # 게시물 생성이 성공했는지(상태 코드 200) 확인합니다.
    assert post_response.status_code == 200
    data = post_response.json()
    # 응답으로 받은 게시물의 제목, 내용, 사용자 번호가 요청한 값과 일치하는지 확인합니다.
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test content."
    assert data["user_no"] == user_no
    # 응답 데이터에 'post_no' 필드가 포함되어 있는지 확인합니다. (DB에 정상적으로 저장되었는지 간접 확인)
    assert "post_no" in data

def test_create_post_for_nonexistent_user(client: TestClient):
    """
    존재하지 않는 사용자(user_no)로 게시물을 생성하려고 할 때,
    API가 올바르게 404 (Not Found) 에러를 반환하는지 테스트합니다.
    """
    # 존재할 가능성이 없는 임의의 user_no(예: 999)를 사용하여 게시물 생성을 시도합니다.
    response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "This is a test content.", "user_no": 999},
    )
    # 응답 상태 코드가 404 (Not Found)인지 확인합니다.
    assert response.status_code == 404
    # 응답 메시지가 예상대로 "Owner User not found"인지 확인합니다.
    assert response.json() == {"detail": "Owner User not found"}