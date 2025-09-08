# 1. 베이스 이미지 선택 (가볍고 안정적인 slim 버전 추천)
FROM python:3.10-slim


# 2. 컨테이너 내 작업 디렉토리 설정
WORKDIR /app


# 3. 의존성 파일 먼저 복사 (Docker 빌드 캐시 효율성 증대)
COPY requirements.txt .


# 4. 의존성 설치 (no-cache-dir로 이미지 용량 최적화)
RUN pip install --no-cache-dir -r requirements.txt


# 5. 애플리케이션 소스 코드 복사
COPY . .


# 6. 컨테이너가 리슨할 포트 지정 (문서화 목적)
EXPOSE 80


# 7. 애플리케이션 실행 명령어
# --host 0.0.0.0 옵션은 컨테이너 외부에서 접근을 허용하기 위해 필수
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]