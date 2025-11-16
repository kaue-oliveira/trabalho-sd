# Imagem base Python oficial com versão slim para reduzir tamanho
FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho na aplicação
WORKDIR /app

# Copiar arquivo de dependências primeiro (otimiza cache do Docker)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY app ./app

# Expor porta do FastAPI (ajustada para 8002 conforme seu agente)
EXPOSE 8002

# Comando para iniciar o serviço FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]