# ☕ Price Agent — Agente de Preço do Café

Microserviço FastAPI responsável por coletar, armazenar e processar preços de Café **Arábica** e **Robusta**, integrando scraping, cálculos estatísticos e comunicação com o Gateway/DataService.

---

## 📌 Funcionalidades

- ✔ Scraping em tempo real dos preços do site Notícias Agrícolas  
- ✔ Envio do preço atualizado para o Data Service  
- ✔ Consulta de histórico dos últimos 90 dias  
- ✔ Cálculo automático de **30 médias** em janelas de **3 dias**  
- ✔ API REST documentada (Swagger)  
- ✔ Arquitetura em microsserviços integrada ao Gateway e frontend  

---

## 🚀 Como Executar

### 🔧 Pré-requisitos
- Python **3.11+**
- Virtual environment (venv)

### 1. Criar ambiente virtual
```bash
cd cafe-price-agent
python3 -m venv venv
source venv/bin/activate

2. Instalar dependências
pip install -r requirements.txt

3. Executar o serviço
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002


A API ficará disponível em:
👉 http://localhost:8002

📡 Endpoints
POST /price/update/{tipo_cafe}

Atualiza o preço via scraping e retorna estatísticas.

Parâmetros:

tipo_cafe: "arabica" ou "robusta"

Exemplo de resposta:
{
    "tipo": "arabica",
    "data": "2025-11-14",
    "preco": 2204.71,
    "medias_3em3dias": [
        2200.50,
        2195.30,
        ...
    ]
}

🧪 Testes Rápidos
Atualizar preço do Arábica
curl -X POST http://localhost:8002/price/update/arabica

Atualizar preço do Robusta
curl -X POST http://localhost:8002/price/update/robusta

🔄 Fluxo do Agente

Scraping → obtém o preço mais recente do site

Envio ao Data Service → salva via Gateway

Coleta do histórico → últimos 90 dias

Cálculo das médias → 30 médias com blocos de 3 dias

Retorno JSON → resposta padronizada para o Gateway

⚙️ Configuração
Data Service:
http://localhost:8001

Portas:

Price Agent → 8002

Data Service → 8001

🐳 Executar com Docker (Opcional)
docker build -t cafe-price-agent .
docker run -p 8002:8002 cafe-price-agent

🎯 Exemplos de Uso
curl -X POST http://localhost:8002/price/update/arabica
curl -X POST http://localhost:8002/price/update/robusta

📝 Notas

O Data Service deve estar rodando na porta 8001

O scraping é feito diretamente do site Notícias Agrícolas

As médias são calculadas com base nos últimos 90 dias

O retorno segue modelo padronizado para integração com o Gateway
