# Imagem base
FROM python:3.11-slim

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do agente
COPY app ./app

# Expor porta do FastAPI
EXPOSE 8000

# Comando para iniciar o serviço
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
