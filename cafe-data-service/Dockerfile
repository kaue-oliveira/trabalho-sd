# cafe-data-service/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# copiar e instalar dependências
COPY cafe-data-service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copiar código fonte
COPY cafe-data-service/app /app/app
# optional: copy init.sql if you want DB boot script inside image (also mounted by compose)
COPY cafe-data-service/init.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE 8000

# comando: uvicorn apontando para a app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
