# Agente Agrônomico

## O que é
Serviço que analisa dados de café e recomenda se deve vender ou aguardar. Usa IA (phi3:mini) para tomar decisões baseadas em clima, preços e documentos técnicos.

## Estrutura de Arquivos
```
agente-agronomico/
├── main.py          # API FastAPI
├── utils.py         # Lógica de IA e HTTP
├── models.py        # Modelos de dados
└── Dockerfile       # Container
```

## Como Usar

### Iniciar o serviço
```bash
sudo docker-compose up -d agro-agent
```

### Testes Básicos

1. **Verificar se está funcionando**
```bash
curl http://localhost:8101/
```

2. **Pedir recomendação de venda**
```bash
time curl -X POST http://localhost:8101/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_cafe": "arabica",
    "data_colheita": "2025-07-15",
    "quantidade": 150.5,
    "cidade": "Patrocínio",
    "estado": "MG",
    "estado_cafe": "verde"
  }' 
```

2.1 **Pedir recomendação via gateway de venda logado**
```bash
curl -X POST http://localhost:3000/auth/login -H "Content-Type: application/json" -d '{"email":"ana.cafeicultora@email.com","password":"CafeAna123"}'
export TOKEN=""
curl -X POST http://localhost:3000/agro/recommend \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_cafe": "arabica",
    "data_colheita": "2025-07-15",
    "quantidade": 150.5,
    "cidade": "Patrocinio",
    "estado": "MG",
    "estado_cafe": "verde"
  }'
```

3. **Ver logs dos PDFs consultados**
```bash
sudo docker logs agro-agent --tail 20
```

## Como Funciona
1. Recebe dados: localidade, tipo de grão, data de colheita
2. Busca clima via Gateway
3. Busca preços via Gateway  
4. Consulta PDFs técnicos via RAG Service
5. Envia tudo para IA (phi3:mini via Ollama)
6. Retorna decisão: `vender` ou `aguardar` + explicação

## Resposta Esperada
```json
{
  "decisao": "aguardar",
  "explicacao_decisao": "Com base no clima e preços..."
}
```

## Dependências
- Gateway rodando (porta 3000)
- Ollama com modelo `phi3:mini`
- RAG Service com PDFs carregados