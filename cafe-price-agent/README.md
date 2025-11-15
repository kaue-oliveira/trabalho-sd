# ☕ Price Agent — Agente de Preço do Café

## 📄 Descrição

O **Price Agent** é um microserviço FastAPI responsável por obter, armazenar e processar preços de **Café Arábica e Robusta**. Ele realiza scraping em tempo real do site Notícias Agrícolas, envia dados ao Data Service, recupera o histórico de 90 dias e calcula estatísticas (30 médias móveis de 3 em 3 dias) para consumo pelo Gateway e pelo frontend.

## 🚀 Funcionalidades

- 🔎 **Scraping de Preços em Tempo Real**: Extração automatizada dos preços de café do site https://www.noticiasagricolas.com.br/cotacoes/cafe
- 🔄 **Integração com Data Service**: Envio de novos preços ao Gateway, que persiste os dados no Data Service
- 📥 **Consulta de Histórico**: Recuperação dos últimos 90 dias de preços históricos
- 📊 **Cálculo de Médias Móveis**: Geração de 30 médias (blocos de 3 dias) para análise de tendências
- 🌐 **API REST**: Endpoints para integração com Gateway e frontend
- 🧩 **Arquitetura Modular**: Separação clara entre scraping, cálculos, rotas e integrações
- 🐳 **Containerizado**: Pronto para execução em Docker

## 🏗️ Arquitetura

```
cafe-price-agent/
├── app/
│   ├── main.py              # Aplicação FastAPI principal
│   ├── routes/
│   │   └── price.py         # Rotas de preços
│   ├── services/
│   │   ├── scraper.py       # Serviço de scraping
│   │   └── dataservice.py   # Integração com Data Service
│   └── utils/
│       └── calc.py          # Cálculos e estatísticas
├── requirements.txt
└── Dockerfile
```

## 📦 Tecnologias Utilizadas

- **Python 3.11** + **FastAPI** - API web moderna e rápida
- **BeautifulSoup4** / **Selenium** - Scraping de dados web
- **Requests** - Cliente HTTP para integração com serviços
- **Docker** - Containerização
- **Uvicorn** - Servidor ASGI de alta performance

## 🔧 Como Executar

### Pré-requisitos

- Python 3.11+
- Data Service rodando na porta 8001

### Execução Rápida

1. **Clone e acesse o projeto:**
```bash
git clone <repositorio>
cd cafe-price-agent
```

2. **Crie e ative o ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate    # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Execute o serviço:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

5. **Acesse os serviços:**
```
API: http://localhost:8002
Documentação: http://localhost:8002/docs
```

## 📡 Endpoints da API

### POST `/price/update/{tipo_cafe}`
- **Descrição**: Atualiza o preço do café via scraping, salva no Data Service e retorna estatísticas
- **Parâmetros**: 
  - `tipo_cafe`: `"arabica"` ou `"robusta"`
- **Resposta**:
```json
{
  "tipo": "arabica",
  "data": "2025-11-14",
  "preco": 2204.71,
  "medias_3em3dias": [
    2200.50,
    2195.30,
    2190.75,
    ...
  ]
}
```

## 🔄 Fluxo de Operação

1. **Scraping** → Obtém preço atual no site Notícias Agrícolas
2. **Salvar** → Envia novo preço ao Data Service (via Gateway)
3. **Buscar Histórico** → Obtém últimos 90 dias de preços
4. **Calcular Médias** → Gera 30 médias móveis (3 em 3 dias)
5. **Retornar JSON** → Estrutura padronizada para o Gateway

## 🎯 Exemplos de Uso

### Atualizar preço do Arábica
```bash
curl -X POST "http://localhost:8002/price/update/arabica"
```

### Atualizar preço do Robusta
```bash
curl -X POST "http://localhost:8002/price/update/robusta"
```

## ⚙️ Configuração

### Endpoints Internos

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| Price Agent | 8002 | Serviço atual |
| Data Service | 8001 | Armazenamento e histórico |

### Variáveis de Ambiente

Crie um arquivo `.env`:
```env
DATA_SERVICE_URL=http://localhost:8001
PORT=8002
```

O Price Agent envia dados ao Data Service usando:
```python
DATA_SERVICE_URL = "http://localhost:8001"
```

## 🐳 Execução com Docker

### Build
```bash
docker build -t cafe-price-agent .
```

### Execução
```bash
docker run -p 8002:8002 cafe-price-agent
```

## 📊 Funcionalidades Técnicas

- **Scraping Robusto**: Extração atualizada e confiável do site Notícias Agrícolas
- **Conexão Direta com Data Service**: Integração seamless para persistência de dados
- **Cálculo de Médias Móveis**: 30 médias calculadas sobre blocos de 3 dias
- **Tratamento de Erros**: Validações e exceções tratadas adequadamente
- **Documentação Automática**: Swagger UI e ReDoc via FastAPI

## 🧪 Testes Rápidos

### Atualizar Arábica
```bash
curl -X POST http://localhost:8002/price/update/arabica
```

### Atualizar Robusta
```bash
curl -X POST http://localhost:8002/price/update/robusta
```

### Verificação do Serviço
```bash
# Health check
curl http://localhost:8002/
```

## 🖥️ Interfaces Visuais para Teste

### Swagger UI (Documentação Interativa)
```
http://localhost:8002/docs
```

### ReDoc
```
http://localhost:8002/redoc
```

## 🌐 Integração com o Sistema Maior

Este serviço é parte de um **sistema distribuído de apoio à decisão** para cafeicultura:

- **Price Agent** (este projeto) - Obtenção e processamento de preços
- **Data Service** - Persistência de dados históricos
- **Agente Climático** - Dados meteorológicos
- **Agente Agronômico** - Análise e decisão integrada
- **API Gateway** - Orquestração central dos agentes

## 📝 Notas Importantes

- ⚠️ O Data Service deve estar rodando na porta 8001
- 🌐 O scraping é extraído do site https://www.noticiasagricolas.com.br/cotacoes/cafe
- 📈 As médias são sempre calculadas sobre os últimos 90 dias disponíveis
- 📤 O retorno segue o padrão esperado pelo Gateway para integração com outros agentes

## 🛠️ Desenvolvimento

### Execução em Ambiente de Desenvolvimento

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate    # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar localmente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```


**💡 Nota**: Este agente fornece dados atualizados de preços de café com análise estatística integrada, essencial para tomada de decisão no sistema de cafeicultura distribuído.
