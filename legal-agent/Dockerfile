FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml .
COPY . .

RUN pip install poetry && poetry lock && poetry install

# entrypoint.sh에 실행 권한 부여
RUN chmod +x entrypoint.sh

# entrypoint.sh 실행
CMD ["./entrypoint.sh"]