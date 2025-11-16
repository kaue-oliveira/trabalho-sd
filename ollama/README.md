# Ollama

## O que é
Servidor local de IA que roda os modelos de linguagem. Fornece o cérebro do sistema - o modelo `phi3:mini` para análises e `nomic-embed-text` para busca em documentos.

## Modelos Usados
- **phi3:mini** (2.2GB) - Modelo principal para análise de café
- **nomic-embed-text** (274MB) - Modelo para busca nos PDFs

## Como Usar

### Iniciar o serviço
```bash
sudo docker-compose up -d ollama
```

### Baixar os modelos necessários
```bash
# Modelo principal (análise)
sudo docker exec ollama ollama pull phi3:mini

# Modelo de busca (embeddings)
sudo docker exec ollama ollama pull nomic-embed-text
```

### Testes Básicos

1. **Verificar se está funcionando**
```bash
curl http://localhost:11434/api/version
```

2. **Ver modelos instalados**
```bash
sudo docker exec ollama ollama list
```

3. **Testar modelo diretamente**
```bash
sudo docker exec ollama ollama run phi3:mini "Como está o mercado de café?"
```

4. **Testar via API**
```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "phi3:mini",
    "prompt": "Explique o café arábica",
    "stream": false
  }'
```

## Como é Usado no Sistema
- **Agente Agrônomico** → chama phi3:mini para análise
- **RAG Service** → usa nomic-embed-text para busca
- **Gateway** → roteia chamadas para /ollama/*

## Configuração GPU
- Suporte Intel GPU (configurado no docker-compose.yml)
- Acelera processamento 2-5x comparado com CPU

## Portas
- **11434** - API do Ollama (HTTP)