# ☕ Cafe Price Agent — Agente de Preços do Café CEPEA

## 📄 Descrição

O **Cafe Price Agent** é um microserviço FastAPI especializado na coleta, processamento e análise de dados históricos de preços do café Arábica e Robusta. O sistema realiza scraping automatizado do site do **CEPEA (Centro de Estudos Avançados em Economia Aplicada)**, processa os dados e calcula estatísticas para apoio à decisão no mercado cafeeiro.

## 🚀 Funcionalidades

- 🌐 **Scraping Automatizado do CEPEA**: Coleta de dados históricos diretamente da fonte oficial
- 📊 **Processamento de Dados**: Conversão e normalização de formatos (XLS → CSV → Estruturas Python)
- 📈 **Cálculo de Médias Móveis**: Geração de 30 médias móveis de 3 em 3 dias
- 🔍 **Validação de Tipos**: Suporte exclusivo para café Arábica e Robusta
- 🧹 **Gestão de Recursos**: Limpeza automática de arquivos temporários
- ⚡ **API REST High-Performance**: Implementada com FastAPI e operação assíncrona

## 🏗️ Arquitetura do Sistema

```
cafe-price-agent/
├── app/
│   ├── main.py              # Aplicação FastAPI principal
│   ├── routes/
│   │   └── price.py         # Endpoints REST para preços
│   ├── services/
│   │   ├── scraper.py       # Serviço de scraping CEPEA
│   │   └── processor.py     # Processamento de dados
│   └── utils/
│       └── calc.py          # Cálculos estatísticos
├── requirements.txt
└── README.md
```

## 📦 Stack Tecnológica

- **Python 3.11+** - Linguagem de programação
- **FastAPI** - Framework web moderno para APIs
- **Pandas** - Processamento e análise de dados
- **Calamine** - Engine para leitura de arquivos Excel (.xls)
- **Requests** - Cliente HTTP para scraping
- **Uvicorn** - Servidor ASGI de alta performance

## 🔧 Instalação e Execução

### Pré-requisitos

- Python 3.11 ou superior
- Dependências: pandas, fastapi, requests, calamine

### Configuração do Ambiente

1. **Clone e acesse o projeto:**

```bash
git clone <repositorio>
cd cafe-price-agent
```

2. **Crie e ative ambiente virtual:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate    # Windows
```

3. **Instale dependências:**

```bash
pip install -r requirements.txt
```

4. **Execute o serviço:**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

### Acesso aos Serviços

- **API Principal:** http://localhost:8002
- **Documentação Interativa:** http://localhost:8002/docs
- **Documentação Alternativa:** http://localhost:8002/redoc

## 📡 Endpoints da API

### GET /preco/{tipo_cafe}

Obtém preços atualizados e médias móveis do café especificado.

**Parâmetros:**
- `tipo_cafe` (path): "arabica" ou "robusta"

**Resposta:**

```json
{
  "tipo_cafe": "arabica",
  "dias_analisados": 90,
  "data_mais_recente": "17/11/2025",
  "preco_atual": 1250.75,
  "medias_moveis_3_dias": [
    {
      "periodo": "15/11/2025 a 17/11/2025",
      "media": 1248.50
    },
    {
      "periodo": "12/11/2025 a 14/11/2025", 
      "media": 1245.25
    }
  ]
}
```

## 🔄 Fluxo de Processamento

1. **Scraping CEPEA** → Download de planilha XLS com 120 dias de dados
2. **Conversão CSV** → Transformação para formato estruturado
3. **Processamento** → Ordenação e filtragem dos 90 dias mais recentes
4. **Cálculo Estatístico** → Geração de 30 médias móveis (3 em 3 dias)
5. **Formatação Resposta** → Estruturação JSON padronizada
6. **Limpeza** → Remoção de arquivos temporários

## 🎯 Exemplos de Uso

### Consulta Preço Arábica

```bash
curl -X GET "http://localhost:8002/preco/arabica"
```

### Consulta Preço Robusta

```bash
curl -X GET "http://localhost:8002/preco/robusta"
```

### Health Check

```bash
curl -X GET "http://localhost:8002/"
```

## ⚙️ Características Técnicas

### Gestão Temporal

- **Período Base:** 120 dias de busca para garantir 90 dias úteis
- **Filtragem:** Seleção dos 90 registros mais recentes
- **Formatação:** Datas no padrão DD/MM/AAAA

### Processamento de Dados

- **Conversão:** XLS → CSV → Estruturas Python nativas
- **Normalização:** Preços no formato float internacional
- **Ordenação:** Cronológica decrescente para processamento

### Segurança e Robustez

- **Validação:** Tipos de café estritamente validados
- **Tratamento de Erros:** Exceções específicas por cenário
- **Limpeza:** Garantia de remoção de arquivos temporários

## 🧪 Testes e Validação

### Testes Manuais via Curl

```bash
# Teste Arábica
curl -X GET "http://localhost:8002/preco/arabica"

# Teste Robusta  
curl -X GET "http://localhost:8002/preco/robusta"

# Teste Tipo Inválido
curl -X GET "http://localhost:8002/preco/expresso"
```

### Interface Web para Testes

- **Swagger UI:** http://localhost:8002/docs
- **ReDoc:** http://localhost:8002/redoc

## 📊 Metodologia Estatística

### Médias Móveis

- **Período:** Blocos sequenciais de 3 dias
- **Cálculo:** Média aritmética simples
- **Limite:** Máximo de 30 períodos (90 dias)
- **Ordenação:** Cronológica crescente para análise temporal

### Garantia de Dados

- **Dias Úteis:** Busca de 120 dias para garantir 90 úteis
- **Consistência:** Remoção de duplicatas e validação de formatos
- **Atualidade:** Sempre os dados mais recentes disponíveis

## 🚨 Tratamento de Exceções

| Código HTTP | Cenário | Ação |
|-------------|---------|------|
| 400 | Tipo de café inválido | Mensagem de erro específica |
| 404 | Nenhum dado encontrado | Informa período sem dados |
| 500 | Erro interno | Log detalhado do processo |

## 🔍 Detalhes de Implementação

### Scraping CEPEA

- **Autenticação:** Sessão HTTP com cookies
- **Parâmetros:** Datas formatadas em DD/MM/AAAA
- **Tabelas:** ID 23 (Arábica) e 24 (Robusta)
- **Formato:** Requisição AJAX com header específico

### Processamento CSV

- **Encoding:** UTF-8 para caracteres especiais
- **Formato Data:** DD/MM/AAAA com validação
- **Formato Preço:** Float com conversão de formato brasileiro

## 💡 Observações Importantes

- ⏰ **Dias Úteis:** Sistema considera apenas dias de negociação (exclui fins de semana)
- 📈 **Fonte Confiável:** Dados obtidos diretamente do CEPEA, órgão oficial de pesquisa
- 🔄 **Atualização Diária:** Dados refletem preços de fechamento do dia anterior
- 🎯 **Precisão:** Cálculos com 2 casas decimais para valores monetários

## 🌐 Contexto Institucional

O CEPEA é ligado à ESALQ/USP e constitui fonte oficial de referência para preços de commodities agrícolas no Brasil, sendo amplamente utilizado por agentes do mercado, pesquisadores e formuladores de políticas públicas.