FROM python:3.11-slim


WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


COPY main.py /app/


ENV OLLAMA_URL=http://ollama:11434 \
OLLAMA_EMBED_MODEL=nomic-embed-text \
CHROMA_PATH=/data/chroma


VOLUME ["/data"]
EXPOSE 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]