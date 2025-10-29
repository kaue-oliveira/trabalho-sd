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

- **Agente Climático:** coleta previsões de tempo e gera resumos normalizados.  
- **Agente de Preços:** realiza scraping ou consultas a APIs de preços e calcula tendências.  
- **Agente Agronômico:** integra clima + preço + relatórios técnicos, aplica regras e gera decisões.  
- **Banco de Dados / Storage:** armazena históricos e logs.  
- **API Gateway / Frontend (opcional):** expõe os resultados e gerencia autenticação.  
- **Camada de Orquestração:** gerencia containers (Docker Compose ou Kubernetes).  

---
## 🧩 Fluxograma / Data Flow

![Fluxograma do Sistema](DiagramasSD-Fluxograma.drawio.png)

---

## 🏗️ Arquitetura

![Arquitetura do Sistema](DiagramasSD-Arquitetura.drawio.png)

## 🧠 Justificativa da Arquitetura

### 1. 🧩 Microserviços + Docker
Cada agente é **independente** e cumpre uma **responsabilidade única**, garantindo modularidade e flexibilidade.  
Essa abordagem:
- Permite **escalar partes específicas** do sistema (por exemplo, o agente de análise climática) sem afetar os demais módulos.  
- Facilita **testes, manutenção e substituição** de componentes isoladamente.  
- Aumenta a **resiliência** — se um agente falhar, o restante do sistema continua operando.  

---

### 2. 🌐 Comunicação via API REST
A comunicação entre os agentes ocorre por meio de **APIs REST**, garantindo:
- **Simplicidade e interoperabilidade**, já que REST é amplamente suportado.  
- Possibilidade de **evolução futura** para sistemas de mensageria (como **Kafka** ou **RabbitMQ**) caso a escala do projeto aumente.  

---

### 3. ⏰ Jobs Agendados
A coleta de dados climáticos e de preços ocorre em **intervalos regulares**, garantindo:
- **Consistência temporal** das informações, já que clima e preços são séries temporais.  
- Capacidade de realizar **análises comparativas** entre períodos (ex.: variação semanal).  

---

### 4. 🧩 Explicabilidade
O agente agronômico combina **regras heurísticas** e **NLP leve** para gerar **recomendações textuais explicáveis**.  
Assim, o produtor entende **por que** uma decisão foi sugerida (ex.: “valorização provável devido à estiagem”).  

---

### 5. 💾 Banco de Dados Centralizado
O uso de um banco de dados central:
- Garante **histórico completo** das informações coletadas.  
- Permite **rastreamento e auditoria** das decisões tomadas.  
- Facilita análises retrospectivas e melhoria contínua do modelo.  

---

## 🧰 Tecnologias Sugeridas

| **Categoria** | **Tecnologia** |
|----------------|----------------|
| **Linguagens** | Python (Agentes, ML), Node.js (API Gateway) |
| **Containers** | Docker, Docker Compose, Kubernetes |
| **Banco de Dados** | PostgreSQL / TimescaleDB |
| **NLP / ML** | spaCy, Transformers (modelos pequenos) |
| **Scheduler** | Cron, Celery, Airflow |
| **Frontend** | React ou Next.js |
| **Mensageria (opcional)** | RabbitMQ, Kafka |

---
