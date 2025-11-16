FROM python:3.11-slim

WORKDIR /app

COPY rag_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rag_service/ .

EXPOSE 8010

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]