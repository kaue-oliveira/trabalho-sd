# ☕ Cafe Data Service

## 📄 Descrição

Este projeto é um **microsserviço especializado em persistência e acesso a dados** para o sistema de cafeicultura, parte de um sistema distribuído de apoio à decisão. O serviço atua como uma camada de abstração sobre o banco de dados, fornecendo uma API REST para operações CRUD (Create, Read, Update, Delete) sobre os dados de usuários, análises de café e preços históricos.

## 🚀 Funcionalidades

- 👥 **Gerenciamento de Usuários**: Criação, listagem e consulta de usuários (Produtores e Cooperativas)
- 📊 **Gerenciamento de Análises**: Operações completas (CRUD) para análises de café
- 💰 **Gerenciamento de Preços Históricos**: CRUD completo para preços do café Arábica e Robusta
- 🗃️ **Persistência Estruturada**: Armazenamento em banco de dados PostgreSQL com relacionamentos
- 🔌 **API REST**: Endpoints RESTful para integração com outros agentes do sistema
- 🐳 **Containerizado**: Pronto para execução em Docker
- 📈 **Validação de Dados**: Usando Pydantic para validação de entradas
- 📖 **Documentação Interativa**: Swagger UI e ReDoc automáticos

## 🏗️ Arquitetura

```
cafe-data-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação FastAPI principal
│   ├── database.py          # Configuração do banco de dados
│   ├── config.py            # Configurações de ambiente
│   ├── models/
│   │   ├── __init__.py
│   │   ├── models.py        # Modelos SQLAlchemy
│   │   └── schemas.py       # Schemas Pydantic
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── usuarios.py      # Operações de CRUD para usuários
│   │   ├── analises.py      # Operações de CRUD para análises
│   │   └── precos.py        # Operações de CRUD para preços históricos
│   └── routes/
│       ├── __init__.py
│       ├── usuarios.py      # Rotas para usuários
│       ├── analises.py      # Rotas para análises
│       └── precos.py        # Rotas para preços históricos
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── init.sql                 # Script de inicialização do banco
```

## 📦 Tecnologias Utilizadas

- **Python 3.11** + **FastAPI** - API web moderna e rápida
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Banco de dados relacional
- **Docker** + **Docker Compose** - Containerização e orquestração
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
cd cafe-data-service
```

2. **Execute com Docker Compose:**
```bash
docker-compose up --build
```

3. **Acesse os serviços:**
```
API: http://localhost:8001
Documentação: http://localhost:8001/docs
```

### Verificação do Serviço

```bash
# Health check
curl http://localhost:8001/

# Listar preços do Arábica
curl http://localhost:8001/precos/arabica/
```

## 📡 Endpoints da API

### GET `/`
- **Descrição**: Página inicial com informações do serviço
- **Resposta**: `{"message": "Cafe Data Service API"}`

### 👥 **Usuários**

#### GET `/usuarios/`
- **Descrição**: Lista todos os usuários
- **Resposta**: Lista de usuários

#### GET `/usuarios/{usuario_id}`
- **Descrição**: Busca um usuário específico por ID
- **Resposta**: Dados do usuário

#### POST `/usuarios/`
- **Descrição**: Cria um novo usuário
- **Body**:
```json
{
  "nome": "Nome do Usuário",
  "email": "email@example.com",
  "senha": "senha123",
  "tipo_conta": "PRODUTOR"
}
```

### ☕ **Análises**

#### GET `/analises/`
- **Descrição**: Lista todas as análises
- **Parâmetros Opcionais**: `skip` (padrão 0), `limit` (padrão 100)

#### GET `/analises/{analise_id}`
- **Descrição**: Busca uma análise específica por ID
- **Resposta**: Dados da análise

#### GET `/analises/usuario/{usuario_id}`
- **Descrição**: Lista análises de um usuário específico
- **Parâmetros Opcionais**: `skip` (padrão 0), `limit` (padrão 100)

#### POST `/analises/`
- **Descrição**: Cria uma nova análise
- **Body**:
```json
{
  "usuario_id": 1,
  "tipo_cafe": "Arábica",
  "data_colheita": "2024-06-15",
  "quantidade": 1500.75,
  "cidade": "Varginha",
  "estado": "MG",
  "estado_cafe": "verde",
  "data_analise": "2024-07-01",
  "decisao": "VENDER",
  "explicacao_decisao": "Preço atual favorável"
}
```

#### DELETE `/analises/{analise_id}`
- **Descrição**: Remove uma análise

### 💰 **Preços Históricos**

#### **Arábica**

##### GET `/precos/arabica/`
- **Descrição**: Lista todos os preços do Arábica (ordenados por data decrescente)

##### GET `/precos/arabica/{price_id}`
- **Descrição**: Busca um preço específico do Arábica por ID

##### GET `/precos/arabica/data/{price_date}`
- **Descrição**: Busca preço do Arábica por data específica

##### GET `/precos/arabica/ultimo/`
- **Descrição**: Retorna o último preço registrado do Arábica

##### POST `/precos/arabica/`
- **Descrição**: Adiciona novo preço do Arábica
- **Body**:
```json
{
  "price_date": "2024-11-14",
  "price": 650.50
}
```

##### DELETE `/precos/arabica/{price_id}`
- **Descrição**: Remove preço do Arábica por ID

##### DELETE `/precos/arabica/ultimo/`
- **Descrição**: Remove o último preço registrado do Arábica

##### DELETE `/precos/arabica/antigo/`
- **Descrição**: Remove o preço mais antigo do Arábica

#### **Robusta**

##### GET `/precos/robusta/`
- **Descrição**: Lista todos os preços do Robusta (ordenados por data decrescente)

##### GET `/precos/robusta/{price_id}`
- **Descrição**: Busca um preço específico do Robusta por ID

##### GET `/precos/robusta/data/{price_date}`
- **Descrição**: Busca preço do Robusta por data específica

##### GET `/precos/robusta/ultimo/`
- **Descrição**: Retorna o último preço registrado do Robusta

##### POST `/precos/robusta/`
- **Descrição**: Adiciona novo preço do Robusta
- **Body**:
```json
{
  "price_date": "2024-11-14",
  "price": 450.25
}
```

##### DELETE `/precos/robusta/{price_id}`
- **Descrição**: Remove preço do Robusta por ID

##### DELETE `/precos/robusta/ultimo/`
- **Descrição**: Remove o último preço registrado do Robusta

##### DELETE `/precos/robusta/antigo/`
- **Descrição**: Remove o preço mais antigo do Robusta

## 🗃️ Estrutura do Banco de Dados

### Tabela `usuarios`
- `id` (Serial, Primary Key)
- `nome` (Varchar)
- `email` (Varchar, Unique)
- `senha` (Varchar)
- `tipo_conta` (Varchar) - "PRODUTOR" ou "COOPERATIVA"
- `criado_em` (Timestamp)

### Tabela `analises`
- `id` (Serial, Primary Key)
- `usuario_id` (Integer, Foreign Key)
- `tipo_cafe` (Varchar)
- `data_colheita` (Date)
- `quantidade` (Decimal)
- `cidade` (Varchar)
- `estado` (Varchar(2))
- `estado_cafe` (Varchar) - "verde", "torrado", "moído"
- `data_analise` (Date)
- `decisao` (Varchar) - "VENDER", "VENDER_PARCIALMENTE", "AGUARDAR"
- `explicacao_decisao` (Text)
- `criado_em` (Timestamp)

### Tabela `arabica_prices_90d`
- `id` (BigSerial, Primary Key)
- `price_date` (Date, Unique)
- `price` (Numeric(12,4))
- `created_at` (Timestamp)

### Tabela `robusta_prices_90d`
- `id` (BigSerial, Primary Key)
- `price_date` (Date, Unique)
- `price` (Numeric(12,4))
- `created_at` (Timestamp)

## 🎯 Exemplos de Uso

### Criar um usuário produtor
```bash
curl -X POST "http://localhost:8001/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Produtor",
    "email": "joao.produtor@email.com",
    "senha": "senha123",
    "tipo_conta": "PRODUTOR"
  }'
```

### Adicionar preço do Arábica
```bash
curl -X POST "http://localhost:8001/precos/arabica/" \
  -H "Content-Type: application/json" \
  -d '{
    "price_date": "2024-11-14",
    "price": 650.50
  }'
```

### Deletar último preço do Robusta
```bash
curl -X DELETE "http://localhost:8001/precos/robusta/ultimo/"
```

### Listar preços do Arábica
```bash
curl -X GET "http://localhost:8001/precos/arabica/"
```

## 🖥️ Interfaces Visuais para Teste

### Swagger UI (Documentação Interativa)
```
http://localhost:8001/docs
```

### ReDoc
```
http://localhost:8001/redoc
```

## 🔍 Testes com cURL

### Listar Usuários
```bash
curl -X GET "http://localhost:8001/usuarios/"
```

### Criar Análise
```bash
curl -X POST "http://localhost:8001/analises/" \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 1,
    "tipo_cafe": "Arábica Premium",
    "data_colheita": "2024-06-15",
    "quantidade": 1500.75,
    "cidade": "Varginha",
    "estado": "MG",
    "estado_cafe": "verde",
    "data_analise": "2024-07-01",
    "decisao": "VENDER",
    "explicacao_decisao": "Preço atual favorável"
  }'
```

### Adicionar Preço Histórico
```bash
curl -X POST "http://localhost:8001/precos/arabica/" \
  -H "Content-Type: application/json" \
  -d '{
    "price_date": "2024-11-14",
    "price": 652.75
  }'
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
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Variáveis de Ambiente

Crie um arquivo `.env`:
```env
DB_HOST=localhost
DB_PORT=5435
DB_NAME=cafequality
DB_USER=postgres
DB_PASSWORD=password
```

## 🌐 Integração com o Sistema Maior

Este serviço é projetado para integrar-se com um **API Gateway** central que orquestra múltiplos agentes:

- **Agente Climático** - Dados meteorológicos
- **Agente de Preços** - Cotações do café em tempo real
- **Agente Agronômico** - Análise e decisão integrada
- **Data Service** (este projeto) - Persistência e consulta de dados históricos

## 📊 Dados Iniciais

O sistema inclui dados de exemplo:
- 2 usuários (1 produtor, 1 cooperativa)
- 8 análises com diferentes decisões e tipos de café
- Estrutura para preços históricos do Arábica e Robusta
- Dados realistas para regiões cafeeiras de MG e ES

## 📝 Licença

Este projeto faz parte do trabalho de Sistemas Distribuídos da UFLA.

## 👥 Autor

- Kauê de Oliveira Silva

---

**💡 Nota**: Este serviço fornece operações completas de CRUD para usuários, análises e preços históricos, com endpoints especializados para gerenciamento eficiente dos dados de café.