-- 회원 정보를 저장하는 'users' 테이블
-- IF NOT EXISTS: 테이블이 존재하지 않을 경우에만 테이블을 생성합니다.
CREATE TABLE IF NOT EXISTS users (
    user_no INTEGER PRIMARY KEY AUTOINCREMENT, -- 각 사용자를 식별하는 고유 ID (자동 증가)
    id TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,           -- 사용자 이메일 (고유해야 하며, 필수 값)
    phone_number TEXT UNIQUE,             -- 핸드폰 번호 (고유해야 하며, 선택 값)
    user_sex TEXT DEFAULT 'M' CHECK (user_sex IN ('M', 'F') ),      -- 성별 (선택 값)
    user_name TEXT NOT NULL,                   -- 이름 (필수 값)
    reg_date  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) -- 가입일자 (현재 시간으로 자동 설정)
);

CREATE INDEX users_IDX ON users (id);

-- 게시판 게시글을 저장하는 'posts' 테이블
CREATE TABLE IF NOT EXISTS posts (
    post_no INTEGER PRIMARY KEY AUTOINCREMENT, -- 각 게시글을 식별하는 고유 ID (자동 증가)
    title TEXT NOT NULL,                  -- 게시글 제목 (필수 값)
    content TEXT NOT NULL,                -- 게시글 내용 (필수 값)
    reg_date TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')), -- 작성일자 (현재 시간으로 자동 설정)
    user_no INTEGER NOT NULL,             -- 작성자 번호 (필수 값)
    -- 외래 키(FOREIGN KEY) 설정: posts.user_id가 users.id를 참조합니다.
    -- ON DELETE CASCADE: 참조하는 사용자가 삭제되면, 해당 사용자가 작성한 모든 게시글도 함께 삭제됩니다.
    -- ON DELETE CASCADE: 참조하는 사용자가 삭제되면, 해당 사용자가 작성한 모든 게시글도 함께 삭제됩니다. (SQLAlchemy 모델에서 ondelete="CASCADE"로 구현)
    FOREIGN KEY (user_no) REFERENCES users (user_no) ON DELETE CASCADE
);

CREATE INDEX posts_IDX ON posts (post_no);
