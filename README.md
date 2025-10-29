# ☕ Sistema Distribuído de Análise Climática, de Preço e Decisão Agronômica na Cafeicultura

### 🧠 Projeto de Sistemas Distribuídos — UFLA  
**Autores:**  
- Gabriel Jardim de Souza  
- Kauê de Oliveira Silva  
- Paulo Henrique Dos Anjos Silveira  
- Thiago Ferreira Azevedo  

---

## 📄 Descrição

Este projeto propõe um **sistema distribuído de apoio à decisão** para produtores de café, integrando **dados climáticos**, **séries de preços** e **informações agronômicas**.  
O objetivo é **gerar recomendações automáticas** sobre o melhor momento para venda da safra, com base em dados históricos e previsões.  

O sistema é composto por **múltiplos agentes autônomos** que coletam, processam e analisam informações de fontes externas (APIs, sites e relatórios técnicos), retornando uma **análise explicável e centralizada** para o usuário final.  

---

## 🚀 Funcionalidades principais

- 🌤️ **Coleta climática automática** via APIs (Open-Meteo, OpenWeatherMap, INMET, etc.)  
- 💰 **Coleta de preços** da saca de café em fontes como CEPEA, B3 e ICO  
- 🌱 **Análise agronômica** baseada em relatórios e indicadores técnicos  
- 🧾 **Geração de recomendações** textuais e interpretáveis (ex.: *“Tendência de valorização devido à estiagem”*)  
- 🗄️ **Armazenamento e histórico** de dados climáticos e financeiros  
- ⚙️ **Arquitetura modular e distribuída**, com cada agente em container próprio  

---

## 🏗️ Arquitetura

A arquitetura é baseada em **microserviços containerizados**, onde cada agente desempenha uma função específica e se comunica via **API REST**.  

### 🔹 Componentes principais

- **Agente Climático:** consome APIs climáticas (como Open-Meteo, INMET, OpenWeather), coleta previsões de tempo e retorna um JSON padronizado.  
- **Agente de Preços:** realiza scraping ou consultas a APIs de preços (CEPEA, B3, ICO) e retorna dados estruturados em JSON.  
- **Agente Agronômico:** integra as informações de clima e preço, interpreta relatórios técnicos e, com apoio de um modelo de linguagem, gera recomendações explicáveis para o produtor.  
- **Ollama (LLM Local):** executa modelos de linguagem (ex.: Llama 3, Mistral, Phi) de forma **local e privada**, permitindo que o **Agente Agronômico** utilize processamento de linguagem natural   (NLP) e geração de texto sem depender de APIs externas.  
- **Banco de Dados / Storage:** armazena históricos climáticos, séries de preços, relatórios e logs de execução.  
- **API Gateway / Frontend:** expõe os resultados dos agentes, centraliza as requisições e gerencia autenticação e segurança.  

---
## 🧩 Fluxograma / Data Flow

![Fluxograma do Sistema](DiagramasSD-Fluxograma.drawio.png)

---

## 🏗️ Arquitetura

![Arquitetura do Sistema](DiagramasSD-Arquitetura.drawio.png)

## 🧠 Justificativa da Arquitetura

A arquitetura proposta adota um **modelo distribuído baseado em microserviços** com comunicação via **API REST**, visando garantir **modularidade, escalabilidade e isolamento funcional** entre os agentes de Inteligência Artificial.  

O sistema foi dividido em **camadas bem definidas**, cada uma responsável por um aspecto específico do processamento, promovendo **baixo acoplamento e alta coesão**, conforme os princípios de arquitetura de sistemas distribuídos modernos.  

---

### 🏗️ 1. Estrutura em Camadas

A separação em camadas facilita a **manutenção, o monitoramento e a evolução independente** de cada módulo.  

| Camada | Função Principal | Justificativa |
|--------|-----------------|---------------|
| 👨‍🌾 **Camada do Usuário (Cliente)** | Interação com o sistema via interface web. | Garante acesso simples e multiplataforma, abstraindo a complexidade dos agentes distribuídos. |
| 🚪 **Camada Gateway / API REST** | Centraliza o roteamento, autenticação e comunicação externa. | Atua como ponto único de entrada, reforçando a segurança e o controle de chamadas. |
| 🌱 **Camada Agronômica (Orquestração)** | Responsável pela orquestração entre os agentes. | Implementa a lógica principal do domínio, coordenando as consultas aos serviços especializados e gerando a decisão final. |
| ☁️💰 **Camada de Serviços Especializados** | Contém os agentes Climático e de Preço do Café. | Segrega responsabilidades: cada agente executa uma tarefa específica, facilitando reuso e paralelização. |
| 🧠 **Camada de IA (Ollama)** | Realiza geração textual e interpretação semântica. | Centraliza as tarefas de NLP e explicabilidade, utilizando modelo local containerizado. |
| 💾 **Camada de Dados** | Armazena históricos de análises e relatórios técnicos. | Garante persistência e auditabilidade, além de permitir análises futuras. |
| 🌎 **Camada de Fontes Externas** | APIs meteorológicas e fontes de preço (CEPEA, B3, ICO). | Mantém a arquitetura extensível e aberta à integração com novos provedores. |

---

### ⚙️ 2. Comunicação e Integração

Os agentes se comunicam via **API REST**, utilizando mensagens no formato **JSON**, conforme boas práticas de integração entre microserviços.  
A escolha dessa abordagem se justifica por:

- **Simplicidade e padronização** (HTTP + JSON são amplamente suportados).  
- **Escalabilidade horizontal**, permitindo execução distribuída em diferentes containers.  
- **Compatibilidade com o modelo de containers Docker**, conforme exigido no trabalho.

---

### 🧠 3. Papéis dos Agentes de IA

- ☁️ **Agente Climático:** coleta e processa informações de APIs meteorológicas, transformando dados em resumos textuais padronizados.  
- 💰 **Agente de Preço do Café:** realiza crawling e análise de fontes de mercado (CEPEA, B3, ICO), gerando resumos sobre variação e tendência de preços.  
- 🌱 **Agente Agronômico:** orquestra os demais agentes, correlacionando clima, produtividade e preço, e produzindo recomendações de venda ou espera.  
- 🧠 **Serviço Ollama:** recebe o contexto gerado pelo Agente Agronômico e gera um texto explicativo interpretável para o usuário final.

Essa divisão garante **independência funcional**, **facilidade de substituição** (ex.: trocar o modelo de IA sem alterar os demais serviços) e **paralelismo de execução**.

---

### 🧱 4. Motivação Técnica

- **Uso de Microserviços** → cada agente é containerizado, garantindo escalabilidade e isolamento.  
- **Arquitetura orientada a mensagens (RESTful)** → simplifica a comunicação distribuída e integra facilmente novas fontes.  
- **Modelo local de IA (Ollama)** → atende ao requisito de possuir pelo menos um modelo de IA local containerizado.  
- **Docker Compose (ou equivalente)** → facilita o deploy e o controle das dependências.  

---

