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
sudo docker-compose up -d agente_agronomico
```

### Testes Básicos

1. **Verificar se está funcionando**
```bash
curl http://localhost:8001/
```

2. **Pedir recomendação de venda**
```bash
curl -X POST http://localhost:8001/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "localidade": "Brasília",
    "tipo_grao": "arábica",
    "data_colheita": "2025-06-01"
  }'
```

3. **Ver logs dos PDFs consultados**
```bash
sudo docker logs agente_agronomico --tail 5
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
  "decision": "aguardar",
  "explanation": "Com base no clima e preços..."
}
```

## Dependências
- Gateway rodando (porta 3000)
- Ollama com modelo `phi3:mini`
- RAG Service com PDFs carregados