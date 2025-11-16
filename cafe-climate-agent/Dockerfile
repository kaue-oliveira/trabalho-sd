FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# CORRIGIDO: caminho relativo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# CORRIGIDO: caminho relativo
COPY src/ ./

EXPOSE 8000

# CORRIGIDO: removi --reload para produção
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]