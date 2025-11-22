# Agente Agrônomico

## O que é
Serviço que analisa dados de café e **toma a decisão** de vender ou aguardar baseada em análise quantitativa. O modelo de IA (phi3:mini) é usado **apenas para gerar explicações**.

## Estrutura de Arquivos
```
agente-agronomico/
├── main.py              # API FastAPI
├── utils.py             # Comunicação com Gateway e Ollama
├── agronomic_agent.py   # Lógica de análise e DECISÃO
├── models.py            # Modelos de dados
└── Dockerfile           # Container
```

## Arquitetura de Decisão

O agente agronômico utiliza uma abordagem híbrida:

1. **Análise Quantitativa** (agronomic_agent.py)
   - `analyze_climate_factors()`: Avalia próximos 7 dias (temperatura, precipitação, vento) → score 0-1
   - `analyze_price_trends()`: Analisa médias móveis e tendências → score 0-1
   - `analyze_market_reports()`: Processa relatórios RAG → score 0-1
   - `calculate_decision_score()`: Combina scores com pesos (clima 35%, preço 40%, mercado 25%)

2. **Decisão FINAL do Agente**
   - Score ≥ 0.5 → **VENDER**
   - Score < 0.5 → **AGUARDAR**

3. **Geração de Explicação** (via Ollama)
   - Recebe decisão já tomada pelo agente
   - Gera explicação detalhada e técnica

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
time curl -X POST http://localhost:3000/agro/recommend \
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

3. **Ver logs do agente agronomico**
```bash
sudo docker logs agro-agent --tail 10
```

## Como Funciona
1. **Recebe requisição**: tipo de café, localidade, data de colheita, estado do café
2. **Busca paralela** (via Gateway):
   - Clima: previsão próximos 14 dias (Open-Meteo)
   - Preços: médias móveis e tendências
   - Relatórios técnicos (RAG)
3. **Análise quantitativa e DECISÃO** (agronomic_agent.py):
   - Calcula scores individuais (clima, preço, mercado)
   - Combina scores com pesos definidos
4. **Constrói prompt com decisão final**:
   - Decisão já tomada pelo agente
   - Dados numéricos estruturados
   - Scores calculados
   - Relatórios como contexto
5. **Consulta Ollama** (phi3:mini):
   - Recebe decisão
   - Gera explicação técnica e detalhada
6. **Retorna resposta**: decisão do agente + explicação do Ollama

## Resposta Esperada
```json
{
  "decisao": "vender",
  "explicacao_decisao": "A decisão de VENDER foi tomada com base no score quantitativo de 0.725. As condições climáticas dos próximos 7 dias são favoráveis com temperaturas entre 24-27°C e precipitação total de apenas 3mm, facilitando logística. O preço atual de R$1389,49 está 2.1% acima da média dos últimos 30 dias, e a tendência recente mostra queda de 4.2% nos últimos períodos, indicando momento oportuno antes de possível desvalorização adicional. Scores: clima 0.80, preço 0.72, mercado 0.65."
}
```

## Pesos da Decisão
- **Clima**: 35% - Próximos 7 dias (temperatura, precipitação, vento)
- **Preço**: 40% - Preço atual vs médias, tendências, volatilidade, momentum
- **Mercado**: 25% - Relatórios técnicos e análises RAG

## Dependências
- Gateway rodando (porta 3000)
- Ollama com modelo `phi3:mini`
- RAG Service com PDFs carregados