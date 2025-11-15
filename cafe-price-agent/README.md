☕ Agente de Preço do Café — Price Agent
Este serviço é um microserviço FastAPI responsável por:

Fazer scraping dos preços de Café Arábica e Robusta diretamente do site:
https://www.noticiasagricolas.com.br/cotacoes/cafe

Enviar novos preços para o Gateway, que salva no DataService.

Buscar o histórico dos últimos 90 dias via Gateway.

Calcular 30 médias, cada uma referente a um bloco de 3 dias.

Expor endpoints REST para serem consumidos pelo Gateway e pelo frontend.

📁 Estrutura de Pastas
text
cafe-price-agent/
│── app/
│   ├── main.py
│   ├── routes/
│   │   └── price.py
│   ├── services/
│   │   ├── scraper.py
│   │   └── dataservice.py
│   └── utils/
│       └── calc.py
│
├── requirements.txt
└── Dockerfile
🚀 Como Executar
Pré-requisitos
Python 3.11+

Virtual Environment

🔧 Configuração e Execução
1. Configurar Ambiente Virtual
bash
cd cafe-price-agent
python3 -m venv venv
source venv/bin/activate
2. Instalar Dependências
bash
pip install -r requirements.txt
3. Executar o Serviço
bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
📡 Endpoints
POST /price/update/{tipo_cafe}
Descrição: Atualiza o preço do café e retorna estatísticas

Parâmetros: tipo_cafe = "arabica" ou "robusta"

Resposta:

json
{
  "tipo": "arabica",
  "data": "2025-11-14",
  "preco": 2204.71,
  "medias_3em3dias": [2200.50, 2195.30, ...]
}
🧪 Testar o Serviço
bash
curl -X POST http://localhost:8002/price/update/arabica
🔄 Fluxo do Agente
Scraping → Obtém preço atual do site

Salvar → Envia preço para DataService via Gateway

Buscar Histórico → Obtém 90 dias de preços

Calcular Médias → Gera 30 médias de 3 em 3 dias

Retornar JSON → Formato padronizado para o Gateway

⚙️ Configuração
Conexão com Data Service
O agente conecta-se diretamente ao Data Service na porta 8001:

python
DATA_SERVICE_URL = "http://localhost:8001"
Porta do Serviço
Price Agent: Porta 8002

Data Service: Porta 8001

🐳 Execução com Docker (Opcional)
bash
docker build -t cafe-price-agent .
docker run -p 8002:8002 cafe-price-agent
📊 Funcionalidades
✅ Scraping em tempo real dos preços do café

✅ Integração completa com Data Service

✅ Cálculo automático de 30 médias móveis

✅ Validação de dados e tratamento de erros

✅ API REST documentada e padronizada

🎯 Exemplo de Uso
bash
# Atualizar preço do Arábica
curl -X POST http://localhost:8002/price/update/arabica

# Atualizar preço do Robusta  
curl -X POST http://localhost:8002/price/update/robusta
Serviço rodando em: http://localhost:8002

📝 Notas
O serviço requer que o Data Service esteja rodando na porta 8001

O scraping é feito diretamente do site Notícias Agrícolas

As médias são calculadas sempre sobre os últimos 90 dias de histórico

O formato de retorno é padronizado para integração com o Gateway