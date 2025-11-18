# ☕ CafeQuality - Testes Completos da API

## 🚀 Subindo o sistema

```bash
# Opcional: parar e limpar containers antigos
docker-compose down

# Subir toda a infraestrutura
docker-compose up --build -d

# Frontend (opcional)
cd cafe-frontend && yarn dev
```

---

## 🧪 1️⃣ Health Check

### **1.1 Health do Gateway**

```bash
curl http://localhost:3000/health
curl http://localhost:3000/health/full
```

### **1.2 Health direto dos serviços**

```bash
curl http://localhost:8001/health  # Data Service
curl http://localhost:8002/health  # Climate Agent
```

> Confirme que todos estão `healthy` antes de testar rotas.

---

## 🧑‍💻 2️⃣ Testes Diretos no Data Service

> Base URL Data Service: `http://localhost:8001`

### **2.1 Criar usuários**

```bash
# Produtor
curl -X POST http://localhost:8001/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome":"Carlos Silva","email":"carlos.fazenda@email.com","senha":"Fazenda2024","tipo_conta":"PRODUTOR"}'

# Cooperativa
curl -X POST http://localhost:8001/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome":"Coop Sul de Minas","email":"coopsul@email.com","senha":"Coop2024!","tipo_conta":"COOPERATIVA"}'
```

### **2.2 Listar usuários**

```bash
curl -X GET http://localhost:8001/usuarios
```

### **2.3 Atualizar usuário (falta implementar no data-service)**

```bash
curl -X PUT http://localhost:8001/usuarios/1 \
  -H "Content-Type: application/json" \
  -d '{"nome":"Carlos Atualizado"}'
```

### **2.4 Deletar usuário (falta implementar no data-service)**

```bash
curl -X DELETE http://localhost:8001/usuarios/1
```

---

## 🔑 3️⃣ Testes via Gateway

> Base URL Gateway: `http://localhost:3000`

### **3.1 Criar usuário via Gateway**

```bash
curl -X POST http://localhost:3000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome":"Ana Costa","email":"ana.cafeicultora@email.com","senha":"CafeAna123","tipo_conta":"PRODUTOR"}'
```

### **3.2 Login e obter token**

```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"ana.cafeicultora@email.com","password":"CafeAna123"}'

# Exportar token para usar nas próximas chamadas
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZW1haWwiOiJhbmEuY2FmZWljdWx0b3JhQGVtYWlsLmNvbSIsImV4cCI6MTc2MzUwNzU2Mn0.i0oaptuigcYkwAdmy1lsdXJlUxGsz1HjP_H3UjQ3PYw"
```

### **3.3 Listar usuários via Gateway**

```bash
curl -X GET http://localhost:3000/usuarios \
  -H "Authorization: Bearer $TOKEN"
```

### **3.4 Atualizar usuário logado**

```bash
curl -X PUT http://localhost:3000/usuarios/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Ana Costa Atualizada","tipo_conta":"PRODUTOR"}'
```

### **3.5 Deletar usuário logado**

```bash
curl -X DELETE http://localhost:3000/usuarios/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🌡️ 4️⃣ Testes de Análises

### **4.1 Criar análise**

```bash
curl -X POST http://localhost:3000/analises \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_cafe":"Arábica",
    "data_colheita":"2024-05-20",
    "quantidade":2500.75,
    "cidade":"Carmo de Minas",
    "estado":"MG",
    "estado_cafe":"verde",
    "data_analise":"2024-05-25",
    "decisao":"VENDER",
    "explicacao_decisao":"Qualidade excelente",
    "usuario_id":1
  }'
```

### **4.2 Listar análises do usuário**

```bash
curl -X GET http://localhost:3000/analises \
  -H "Authorization: Bearer $TOKEN"
```


### **4.3 Deletar análise(falta implementar no gateway)**

```bash
curl -X DELETE http://localhost:3000/analises/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🌤️ 5️⃣ Testes dos Agentes

### **5.1 Agente Climático**

```bash
curl -X GET "http://localhost:3000/climate/forecast?cidade=Lavras&estado=MG" \
  -H "Authorization: Bearer $TOKEN"
```


### **5.2 Agente de Preço**

```bash
curl -X GET "http://localhost:3000/price/robusta" \
  -H "Authorization: Bearer $TOKEN"
```


### **5.3 Agente Agronômico**
```bash
curl -X POST http://localhost:3000/agro/recommend \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_cafe": "arabica",
    "data_colheita": "2025-11-11",
    "quantidade": 150.5,
    "cidade": "Santos",
    "estado": "SP",
    "estado_cafe": "verde"
  }'
```
---


## ✅ Dicas de Debug

```bash
docker-compose logs -f gateway
docker-compose logs -f data-service
docker-compose logs -f climate-agent
```

---
