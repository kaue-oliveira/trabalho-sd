# RAG Service

## O que é
Sistema de busca em documentos PDF usando IA. Indexa 28 PDFs sobre café e permite buscar informações usando linguagem natural.

## Estrutura de Arquivos
```
rag_service/
├── main.py          
├── rag_loader.py    
├── pdfs/            
└── Dockerfile       
```

## Como Usar

### Iniciar o serviço
```bash
sudo docker-compose up -d rag-service
```

### Testes Básicos

1. **Verificar se está funcionando**
```bash
curl http://localhost:8102/
```

2. **Ver quantos documentos foram indexados**
```bash
curl http://localhost:8102/rag/status
```

3. **Buscar informação nos PDFs**
```bash
curl -X POST http://localhost:8102/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query": "mudanças climáticas no café", "k": 3}'
```

4. **Recarregar documentos**
```bash
curl -X POST http://localhost:8102/rag/reload
```

3. **Ver logs dos PDFs consultados**
```bash
sudo docker logs rag-service --tail 10
```


## Como Funciona
1. Lê PDFs da pasta `/pdfs`
2. Quebra em pequenos pedaços de texto
3. Transforma texto em números (embeddings) via Ollama
4. Salva no banco ChromaDB
5. Quando você busca, encontra os textos mais parecidos

## Dependências
- Ollama rodando com modelo `nomic-embed-text`
- ChromaDB para armazenar vetores
- FastAPI para a API web