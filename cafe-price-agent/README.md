# ☕ Cafe Price Agent

## 📄 Descrição

O **Cafe Price Agent** é um microserviço FastAPI especializado na coleta, processamento e análise de dados históricos de preços do café Arábica e Robusta.

O sistema realiza scraping automatizado do **CEPEA (Centro de Estudos Avançados em Economia Aplicada)**, processa a planilha XLS oficial, normaliza os dados e calcula estatísticas — como médias móveis de 3 em 3 dias e desvio padrão de 10 em 10 dias, dos últimos 90 dias — fornecendo informações essenciais para análise e tomada de decisão no mercado cafeeiro.

## 🚀 Funcionalidades

- 🌐 **Scraping Automatizado**: Download direto dos dados oficiais do CEPEA
- 📊 **Processamento de Dados**: Conversão XLS → CSV → Estruturas Python
- 📈 **Cálculo de Médias Móveis (3 em 3 dias)**: Geração de até 30 médias móveis
- 📉 **Cálculo de Desvio Padrão (10 em 10 dias)**: Análise estatística por períodos
- 🔍 **Validação Rígida**: Aceita apenas arabica ou robusta
- 🧹 **Limpeza de Recursos**: Exclusão automática de arquivos temporários
- ⚡ **API REST**: Implementada em FastAPI com execução assíncrona

## 🏗️ Arquitetura do Sistema

```
cafe-price-agent/
├── app/
│   ├── main.py              # Aplicação FastAPI principal
│   ├── routes/
│   │   └── price.py         # Endpoints REST para preços
│   ├── services/
│   │   ├── scraper.py       # Serviço de scraping CEPEA (XLS)
│   │   └── processor.py     # Processamento e ordenação dos dados
│   └── utils/
│       └── calc.py          # Cálculos estatísticos (médias & desvios)
├── requirements.txt
└── README.md
```

## 📦 Stack Tecnológica

- **Python 3.11+** – Linguagem principal
- **FastAPI** – Framework moderno para APIs
- **Pandas** – Tratamento de dados
- **Calamine** – Leitura de arquivos Excel .xls
- **Requests** – Cliente HTTP
- **Uvicorn** – Servidor ASGI de alta performance

## 🔧 Instalação e Execução

### Pré-requisitos

- Python 3.11 ou superior
- Instalar dependências do requirements.txt

### Configuração do Ambiente

1. **Clone o repositório:**

```bash
git clone https://github.com/kaue-oliveira/trabalho-sd.git
cd cafe-price-agent
```

2. **Crie e ative o ambiente virtual:**

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac

# ou
venv\Scripts\activate      # Windows
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

```
API Principal: http://localhost:8002
Swagger UI: http://localhost:8002/docs
Redoc: http://localhost:8002/redoc
```

## 📡 Endpoints da API

### GET /preco/{tipo_cafe}

Obtém preços atualizados, médias móveis e desvios padrão para o tipo de café especificado.

**Parâmetros:**

- `tipo_cafe`: "arabica" ou "robusta"

**Exemplo de resposta:**

```json
{
  "tipo_cafe": "arabica",
  "dias_analisados": 90,
  "data_mais_recente": "17/11/2025",
  "preco_atual": 1250.75,
  "desvio_padrao_10_dias": [
    {
      "periodo": "01/11/2025 a 10/11/2025",
      "desvio_padrao": 4.21
    }
  ],
  "medias_moveis_3_dias": [
    {
      "periodo": "15/11/2025 a 17/11/2025",
      "media": 1248.50
    }
  ]
}
```

## 🔄 Fluxo de Processamento

1. **Scraping CEPEA** → Download do arquivo XLS (últimos ~120 dias)
2. **Conversão XLS → CSV** → Extração das células de data/preço
3. **Processamento** → Normalização, limpeza, ordenação por data
4. **Filtragem** → Seleção dos 90 dias mais recentes
5. **Cálculo Estatístico** →
   - Médias móveis (3 em 3 dias)
   - Desvio padrão (10 em 10 dias)
6. **Resposta JSON** → Retorno estruturado
7. **Limpeza de Temporários** → Exclusão dos arquivos XLS/CSV

## 🎯 Exemplos de Uso

### Consulta Arábica

```bash
curl -X GET "http://localhost:8002/preco/arabica"
```

### Consulta Robusta

```bash
curl -X GET "http://localhost:8002/preco/robusta"
```

### Health Check

```bash
curl -X GET "http://localhost:8002/"
```

## ⚙️ Características Técnicas

### Gestão Temporal

- **Período Base**: ~120 dias buscados para garantir 90 dias úteis
- **Filtragem**: Seleção dos 90 registros mais recentes
- **Datas**: Padrão DD/MM/AAAA

### Processamento de Dados

- **Conversão**: XLS → CSV → Estruturas Python
- **Normalização**: Preços convertidos para float internacional
- **Ordenação**: Lista ordenada da data mais recente para a mais antiga

## 🧪 Testes e Validação

### Testes via Curl

```bash
curl -X GET "http://localhost:8002/preco/arabica"
curl -X GET "http://localhost:8002/preco/robusta"
curl -X GET "http://localhost:8002/preco/expresso"
```

### Testes via Interface Web

- **Swagger UI**: http://localhost:8002/docs
- **ReDoc**: http://localhost:8002/redoc

## 📊 Metodologia Estatística

### Médias Móveis

- **Blocos**: 3 dias sequenciais
- **Cálculo**: Média aritmética
- **Limite**: Até 30 períodos (90 dias)
- **Ordenação**: Cronológica crescente

### Desvio Padrão

- **Períodos**: Grupos de 10 dias
- **Cálculo**: statistics.stdev
- **Retorno**: Até 9 blocos válidos

### Consistência dos Dados

- **Fonte**: CEPEA/ESALQ-USP
- **Conversão**: Formato brasileiro → float internacional
- **Deduplicação**: Remoção de registros duplicados
- **Atualidade**: Sempre retorna o dado mais recente disponível

## 🚨 Tratamento de Exceções

| Código HTTP | Cenário | Ação |
|------------|---------|------|
| 400 | Tipo de café inválido | Mensagem explicativa |
| 404 | Nenhum dado encontrado | Retorno padronizado |
| 500 | Erro interno | Log detalhado e tratamento seguro |

## 🔍 Detalhes de Implementação

### Scraping CEPEA

- Sessão HTTP persistente
- Requisições AJAX
- Identificação de tabelas CEPEA:
  - **23** → Arábica
  - **24** → Robusta
- Datas em formato DD/MM/AAAA
- Download automático do arquivo .xls

### Processamento CSV

- Engine Calamine para leitura
- Extração de datas e preços em células adjacentes
- Normalização do formato monetário
- Salvamento padronizado UTF-8

## 💡 Observações Importantes

- ⏰ Considera somente dias de mercado (exclui fins de semana)
- 📈 Dados provenientes diretamente do CEPEA
- 🎯 Valores calculados com precisão de 2 casas decimais

## 🌐 Contexto Institucional

O CEPEA, ligado à ESALQ/USP, é referência nacional na coleta e divulgação de preços agrícolas, usado por produtores, cooperativas, indústrias, instituições financeiras e órgãos reguladores.

---

**Desenvolvido para análise e acompanhamento do mercado cafeeiro brasileiro** ☕📊
