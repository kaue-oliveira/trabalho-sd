---

# ☕ **Cafe Data Service**

## 📄 **Descrição**

Este projeto é um **microsserviço especializado em persistência e acesso a dados** para o sistema de cafeicultura, parte de um sistema distribuído de apoio à decisão. O serviço atua como uma camada de abstração sobre o banco de dados PostgreSQL, fornecendo uma API REST completa para operações CRUD (Create, Read, Update, Delete) sobre os dados de usuários e análises de café.

---

# 🚀 **Funcionalidades**

* 👥 **Gerenciamento de Usuários**: CRUD completo para usuários (Produtores e Cooperativas)
* 📊 **Gerenciamento de Análises**: Operações completas para análises de café com decisões de venda
* 🔐 **Autenticação JWT**: Sistema seguro de login com tokens
* 🗃️ **Persistência Estruturada**: Armazenamento em PostgreSQL com relacionamentos
* 🔌 **API REST**: Endpoints RESTful para integração com outros agentes do sistema
* 🐳 **Containerização**: Pronto para execução em Docker
* 📈 **Validação de Dados**: Usando Pydantic para validação robusta
* 📖 **Documentação Interativa**: Swagger UI e ReDoc automáticos

---

# 🏗️ **Arquitetura**

```
cafe-data-service/
├── app/
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── usuarios.py      # Operações de CRUD para usuários
│   │   └── analises.py      # Operações de CRUD para análises
│   ├── models/
│   │   ├── __init__.py
│   │   ├── models.py        # Modelos SQLAlchemy
│   │   └── schemas.py       # Schemas Pydantic
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── usuarios.py      # Rotas para usuários
│   │   ├── analises.py      # Rotas para análises
│   │   └── auth.py          # Rotas de autenticação
│   ├── config.py            # Configurações de ambiente
│   ├── database.py          # Configuração do banco de dados
│   ├── jwt_utils.py         # Utilitários JWT
│   └── main.py              # Aplicação FastAPI principal
├── init.sql                 # Script de inicialização do banco
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 📦 **Tecnologias Utilizadas**

* **Python 3.11** + **FastAPI**
* **SQLAlchemy**
* **PostgreSQL**
* **Docker**
* **Pydantic**
* **JWT**
* **bcrypt**
* **Uvicorn**

---

# 🔧 **Como Executar**

## **Pré-requisitos**

* Docker
* Docker Compose (opcional)

---

## **Execução com Docker**

### 1. Construir e executar o container

```bash
docker build -t cafe-data-service .
docker run -p 8001:8000 cafe-data-service
```

### 2. Acesse os serviços

```
API: http://localhost:8001
Documentação: http://localhost:8001/docs
Health Check: http://localhost:8001/health
```

---

## **Execução com Docker Compose**

```bash
# Em desenvolvimento - usar docker-compose.yml se disponível
docker-compose up --build
```

---

## **Verificação do Serviço**

```bash
# Health check
curl http://localhost:8001/health

# Listar usuários
curl http://localhost:8001/usuarios/
```

---

# 📡 **Endpoints da API**

## 🔐 **Autenticação**

### POST `/auth/login`

**Descrição:** Realiza login e retorna token JWT
**Body:**

```json
{
  "email": "usuario@email.com",
  "password": "senha123"
}
```

---

## 👥 **Usuários**

### GET `/usuarios/`

Lista todos os usuários

### GET `/usuarios/{usuario_id}`

Busca usuário por ID

### POST `/usuarios/`

Cria novo usuário
**Body:**

```json
{
  "nome": "João Produtor",
  "email": "joao.produtor@email.com",
  "senha": "senha123",
  "tipo_conta": "PRODUTOR"
}
```

### PUT `/usuarios/{usuario_id}`

Atualiza dados

### DELETE `/usuarios/{usuario_id}`

Remove usuário e suas análises

---

## ☕ **Análises**

### GET `/analises/`

Lista todas as análises
Parâmetros opcionais: `skip`, `limit`

### GET `/analises/{analise_id}`

Busca análise por ID

### GET `/analises/usuario/{usuario_id}`

Lista análises por usuário
Parâmetros opcionais: `skip`, `limit`

### POST `/analises/`

Cria nova análise
**Body:**

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
  "explicacao_decisao": "Preço atual favorável para café de alta qualidade"
}
```

### PUT `/analises/{analise_id}`

Atualiza dados

### DELETE `/analises/{analise_id}`

Remove análise

---

# 🗃️ **Estrutura do Banco de Dados**

## **Tabela `usuarios`**

* id
* nome
* email
* senha (bcrypt)
* tipo_conta
* criado_em

## **Tabela `analises`**

* id
* usuario_id
* tipo_cafe
* data_colheita
* quantidade
* cidade
* estado
* estado_cafe
* data_analise
* decisao
* explicacao_decisao
* criado_em

---

# 🎯 **Exemplos de Uso**

## Criar usuário

```bash
curl -X POST "http://localhost:8001/usuarios/" ...
```

## Login

```bash
curl -X POST "http://localhost:8001/auth/login" ...
```

## Criar análise

```bash
curl -X POST "http://localhost:8001/analises/" ...
```

## Listar análises de um usuário

```bash
curl -X GET "http://localhost:8001/analises/usuario/1"
```

---

# 🖥️ **Interfaces Visuais**

### Swagger UI

`http://localhost:8001/docs`

### ReDoc

`http://localhost:8001/redoc`

---

# 🔍 **Testes com cURL**

Exemplos:

```bash
curl -X GET "http://localhost:8001/usuarios/"
curl -X GET "http://localhost:8001/usuarios/1"
curl -X GET "http://localhost:8001/analises/"
curl -X DELETE "http://localhost:8001/analises/1"
```

---

# 📊 **Dados Iniciais**

Incluídos via `init.sql`:

* 2 usuários
* 8 análises
* Cenários realistas MG/ES
* Decisões baseadas em mercado e qualidade

---

# 🔐 **Segurança**

* Senhas com bcrypt
* Autenticação JWT
* Validação com Pydantic
* Proteção SQL Injection via SQLAlchemy

---

# 🌐 **Integração com o Sistema Maior**

Parte do ecossistema:

* Agente Climático
* Agente de Preços
* Agente Agronômico
* Data Service (este)

---

# 🛠️ **Desenvolvimento**

```
cafe-data-service/
├── app/
│   ├── crud/
│   ├── models/
│   ├── routes/
│   └── *.py
├── init.sql
├── requirements.txt
└── Dockerfile
```

## Variáveis de Ambiente

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cafequality
DB_USER=postgres
DB_PASSWORD=password
SECRET_KEY=dev_secret_key_change_in_production
```

---

# 📝 **Licença**

Este projeto faz parte do trabalho de Sistemas Distribuídos da UFLA.

# 👥 **Autor**

Kauê de Oliveira Silva

---

