# 베이스 이미지 (경량 Python 슬림)
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 로그 폴더 미리 생성 (Gunicorn 로그용)
RUN mkdir logs

# 소스 코드 전체 복사
COPY . .

# 실행 (백그라운드 옵션 없이 작성 - Docker 실행 시 처리함)
CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:5000", "app:app"]