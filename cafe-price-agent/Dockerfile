FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia requirements e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do projeto para /app
COPY . .

# Expõe a porta
EXPOSE 8000

# Comando para iniciar o uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
