from fastapi import FastAPI


# FastAPI 앱 인스턴스 생성
app = FastAPI()


# 루트 경로 핸들러
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI in Docker!4444 🐳"}