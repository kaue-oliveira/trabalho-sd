# ☕ Agente Climático para Cafeicultura

## 📄 Descrição

Este projeto é um **microsserviço especializado em dados climáticos** para cafeicultura, parte de um sistema distribuído de apoio à decisão. O agente coleta e processa dados meteorológicos da API Open-Meteo, retornando informações essenciais para o cultivo de café em formato JSON.

## 🚀 Funcionalidades

- 🌤️ **Previsão de 14 dias**: Retorna dados climáticos completos para as próximas duas semanas
- 🗺️ **Geocoding inteligente**: Converte nomes de cidades em coordenadas geográficas
- 📍 **Suporte a regiões cafeeiras**: Inclui cidades produtoras de café do Brasil
- 🐳 **Containerizado**: Pronto para execução em Docker
- 🔌 **API REST**: Endpoints GET e POST para consulta flexível
- 📊 **Dados específicos para cafeicultura**: Temperatura, precipitação, vento e condições gerais

## 🏗️ Arquitetura

```
cafe-climate-agent/
├── src/
│   ├── agents/           # Lógica principal do agente (FastAPI)
│   ├── services/         # Serviço de integração com Open-Meteo
│   ├── models/           # Modelos de dados Pydantic
│   └── utils/            # Utilitários (geocoding)
├── Dockerfile           # Configuração do container
└── docker-compose.yml   # Orquestração
```

## 📦 Tecnologias Utilizadas

- **Python 3.11** + **FastAPI** - API web moderna e rápida
- **Docker** + **Docker Compose** - Containerização e orquestração
- **Open-Meteo API** - Dados meteorológicos gratuitos
- **Pydantic** - Validação de dados e serialização
- **Uvicorn** - Servidor ASGI de alta performance

## 🔧 Como Executar

### Pré-requisitos

- Docker
- Docker Compose

### Execução Rápida

1. **Clone e acesse o projeto:**
```bash
git clone <repositorio>
cd cafe-climate-agent
```

2. **Execute com Docker Compose:**
```bash
docker-compose up --build
```

3. **Acesse a API:**
```
http://localhost:8000
```

### Verificação do Serviço

```bash
# Health check
curl http://localhost:8000/health

# Página inicial
curl http://localhost:8000/
```

## 📡 Endpoints da API

### GET `/health`
- **Descrição**: Verifica se o serviço está online
- **Resposta**: `{"status": "healthy"}`

### GET `/`
- **Descrição**: Página inicial com informações do serviço
- **Resposta**: `{"message": "Agente Climático para Cafeicultura - Online"}`

### GET `/climate/forecast/{localidade}`
- **Descrição**: Obtém previsão climática via parâmetro de URL
- **Exemplo**: 
```bash
curl "http://localhost:8000/climate/forecast/Barueri-SP"
```

### POST `/climate/forecast`
- **Descrição**: Obtém previsão climática via body JSON
- **Exemplo**:
```bash
curl -X POST "http://localhost:8000/climate/forecast" \
  -H "Content-Type: application/json" \
  -d '{"location": "Lavras-MG"}'
```

## 📊 Estrutura da Resposta

```json
{
  "location": "Barueri-SP",
  "latitude": -23.511,
  "longitude": -46.876,
  "timezone": "America/Sao_Paulo",
  "elevation": 719.0,
  "daily_forecast": [
    {
      "date": "2024-01-15",
      "temperature_2m_max": 28.5,
      "temperature_2m_min": 18.2,
      "precipitation_sum": 0.0,
      "precipitation_hours": 0.0,
      "windspeed_10m_max": 15.2,
      "winddirection_10m_dominant": 120,
      "weathercode": 0
    }
  ],
  "generated_time": "2024-01-15T10:30:00"
}
```

## 🎯 Cidades Suportadas

O agente inclui suporte nativo para regiões cafeeiras:

*Localidades são buscadas automaticamente via API de geocoding*

## 🔍 Exemplo de Uso no Insomnia

### 1. Health Check
```
GET http://localhost:8000/health
```

### 2. Previsão via GET
```
GET http://localhost:8000/climate/forecast/Barueri-SP
```

### 3. Previsão via POST
```
POST http://localhost:8000/climate/forecast
Content-Type: application/json

{
  "location": "Lavras-MG"
}
```

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
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Estrutura de Desenvolvimento

```python
# Modelos de dados (Pydantic)
models/climate_models.py

# Lógica da API FastAPI
agents/climate_agent.py

# Integração com Open-Meteo
services/open_meteo_service.py

# Conversão de localidades
utils/geocoding.py
```

## 🌐 Integração com o Sistema Maior

Este agente é projetado para integrar-se com um **API Gateway** central que orquestra múltiplos agentes:

- **Agente Climático** (este projeto) - Dados meteorológicos
- **Agente de Preços** - Cotações do café
- **Agente Agronômico** - Análise e decisão integrada

## 🔒 Considerações de Segurança

- Todas as comunicações devem usar HTTPS em produção
- Implementar rate limiting para evitar abuso
- Validar e sanitizar todas as entradas de usuário
- Usar tokens JWT para autenticação no gateway

## 📈 Monitoramento

O serviço inclui endpoints básicos de saúde:
- `/health` - Status do serviço
- `/` - Informações básicas

## 🐛 Solução de Problemas

### Erro: "Localização não encontrada"
- Verifique o formato: "Cidade-UF"
- Use cidades da lista suportada
- Para novas cidades, adicione coordenadas em `geocoding.py`

### Erro: Container não inicia
- Verifique se a porta 8000 está livre
- Execute `docker-compose down` e reconstrua
- Verifique logs: `docker-compose logs`

## 📝 Licença

Este projeto faz parte do trabalho de Sistemas Distribuídos da UFLA.

## 👥 Autor

- Kauê de Oliveira Silva  


---

**💡OBS**: Pode ser necessario configurar variáveis de ambiente para URLs de API e ajuste o timeout das requisições conforme necessário.
