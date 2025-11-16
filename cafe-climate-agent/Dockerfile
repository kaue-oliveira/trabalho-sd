# cafe-climate-agent/Dockerfile (dev, com reload)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY cafe-climate-agent/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copiar código (assume sua estrutura src/)
COPY cafe-climate-agent/src/ /app/

EXPOSE 8002

# usa uvicorn para rodar main:app (recomendado) — se seu main faz uvicorn.run internamente, pode usar "python main.py"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
