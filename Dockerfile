FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/

EXPOSE 3000
EXPOSE 8080

CMD ["uvicorn", "src.entrypoint:app", "--host", "0.0.0.0", "--port", "8080"]
