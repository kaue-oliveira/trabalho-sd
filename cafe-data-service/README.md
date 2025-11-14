# ☕ Cafe Data Service

## 📄 Descrição

Este projeto é um **microsserviço especializado em persistência e acesso a dados** para o sistema de cafeicultura, parte de um sistema distribuído de apoio à decisão. O serviço atua como uma camada de abstração sobre o banco de dados, fornecendo uma API REST para operações CRUD (Create, Read, Update, Delete) sobre os dados de usuários e análises de café.

## 🚀 Funcionalidades

- 👥 **Gerenciamento de Usuários**: Criação, listagem e consulta de usuários (Produtores e Cooperativas)
- 📊 **Gerenciamento de Análises**: Operações completas (CRUD) para análises de café
- 🗃️ **Persistência Estruturada**: Armazenamento em banco de dados PostgreSQL com relacionamentos
- 🔌 **API REST**: Endpoints RESTful para integração com outros agentes do sistema
- 🐳 **Containerizado**: Pronto para execução em Docker
- 📈 **Validação de Dados**: Usando Pydantic para validação de entradas
- 📖 **Documentação Interativa**: Swagger UI e ReDoc automáticos
- 🗄️ **Interface Visual**: pgAdmin incluído para gerenciamento do banco

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
│   │   └── analises.py      # Operações de CRUD para análises
│   └── routes/
│       ├── __init__.py
│       ├── usuarios.py      # Rotas para usuários
│       └── analises.py      # Rotas para análises
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
- **pgAdmin** - Interface web para gerenciamento do banco

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
pgAdmin: http://localhost:8080
```

### Verificação do Serviço

```bash
# Health check
curl http://localhost:8001/health

# Página inicial
curl http://localhost:8001/
```

## 📡 Endpoints da API

### GET `/health`
- **Descrição**: Verifica se o serviço está online
- **Resposta**: `{"status": "healthy", "service": "Cafe Data Service"}`

### GET `/`
- **Descrição**: Página inicial com informações do serviço
- **Resposta**: `{"message": "Cafe Data Service - API REST", ...}`

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

#### PUT `/analises/{analise_id}`
- **Descrição**: Atualiza uma análise existente
- **Body** (campos opcionais):
```json
{
  "tipo_cafe": "Novo Tipo",
  "quantidade": 1200.50,
  "decisao": "AGUARDAR",
  "explicacao_decisao": "Nova explicação"
}
```

#### DELETE `/analises/{analise_id}`
- **Descrição**: Remove uma análise

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

### Criar uma análise
```bash
curl -X POST "http://localhost:8001/analises/" \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": 1,
    "tipo_cafe": "Bourbon",
    "data_colheita": "2024-05-20",
    "quantidade": 800.25,
    "cidade": "Carmo de Minas",
    "estado": "MG",
    "estado_cafe": "verde",
    "data_analise": "2024-06-10",
    "decisao": "VENDER_PARCIALMENTE",
    "explicacao_decisao": "Café de alta qualidade, preço pode valorizar"
  }'
```

### Listar análises de um usuário
```bash
curl -X GET "http://localhost:8001/analises/usuario/1"
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

### pgAdmin (Gerenciamento do Banco)
```
http://localhost:8080
```
- **Email**: `admin@admin.com`
- **Senha**: `admin`

**Configuração do pgAdmin:**
1. Adicione um novo servidor
2. **Name**: `CafeQuality DB`
3. **Host**: `db`
4. **Port**: `5432`
5. **Username**: `postgres`
6. **Password**: `password`

## 🔍 Testes com cURL

### Health Check
```bash
curl -X GET "http://localhost:8001/health"
```

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
DB_PORT=5433
DB_NAME=cafequality
DB_USER=postgres
DB_PASSWORD=password
```

## 🌐 Integração com o Sistema Maior

Este serviço é projetado para integrar-se com um **API Gateway** central que orquestra múltiplos agentes:

- **Agente Climático** - Dados meteorológicos
- **Agente de Preços** - Cotações do café
- **Agente Agronômico** - Análise e decisão integrada
- **Data Service** (este projeto) - Persistência e consulta de dados

## 📈 Monitoramento

O serviço inclui endpoints básicos de saúde:
- `/health` - Status do serviço
- `/` - Informações básicas

## 🐛 Solução de Problemas

### Erro: Porta já em uso
- Altere as portas no `docker-compose.yml` se as portas estiverem ocupadas

### Erro: "Cannot connect to database"
- Verifique se o container do PostgreSQL está rodando
- Confirme as credenciais no `.env`

### Erro de importação de módulos
- Verifique a estrutura de diretórios e arquivos `__init__.py`

### Dependências faltantes
- Verifique se todas as dependências estão no `requirements.txt`

## 📊 Dados Iniciais

O sistema inclui dados de exemplo:
- 2 usuários (1 produtor, 1 cooperativa)
- 8 análises com diferentes decisões e tipos de café
- Dados realistas para regiões cafeeiras de MG e ES

## 📝 Licença

Este projeto faz parte do trabalho de Sistemas Distribuídos da UFLA.

## 👥 Autor

- Kauê de Oliveira Silva

---

**💡 OBS**: ---