# ☕ Sistema Distribuído de Análise Climática, de Preço e Decisão Agronômica na Cafeicultura

### 🧠 Projeto de Sistemas Distribuídos — UFLA  
**Autores:**  
- Gabriel Jardim de Souza  
- Kauê de Oliveira Silva  
- Paulo Henrique Dos Anjos Silveira  
- Thiago Ferreira Azevedo  

---

## 📄 Descrição

Este projeto propõe um **sistema distribuído de apoio à decisão** voltado à **cafeicultura**, integrando dados **climáticos**, **de mercado** e **agronômicos** para auxiliar produtores e cooperativas a definirem **o melhor momento de venda da safra**.

A solução utiliza **múltiplos agentes inteligentes**, implementados como **microserviços autônomos**, que coletam, processam e cruzam informações de fontes externas (APIs e relatórios técnicos).  
O resultado final é uma **análise explicável**, entregue de forma integrada e segura ao usuário via **API Gateway**.

---

## 🚀 Funcionalidades Principais

- 🌤️ **Coleta climática automática** via APIs (Open-Meteo, OpenWeatherMap, INMET, etc.)  
- 💰 **Coleta de preços** da saca de café (CEPEA, B3, ICO)  
- 🌱 **Análise agronômica integrada**, considerando clima, solo e produtividade  
- 🧾 **Geração de recomendações textuais explicáveis**, como:  
  *“Recomenda-se aguardar duas semanas antes da venda devido à previsão de estiagem e alta de preços.”*  
- 🗄️ **Armazenamento histórico** de clima, preços e relatórios técnicos  
- ⚙️ **Arquitetura modular e distribuída**, com cada agente containerizado em Docker  

---

## 🏗️ Arquitetura

A arquitetura é **orientada a microserviços** e projetada para funcionar de forma **distribuída e orquestrada via REST**.  
Cada agente atua de maneira independente, mas integrada através de um **API Gateway**, que realiza o **roteamento, autenticação e comunicação entre os serviços**.

![Arquitetura do Sistema](DiagramasSD-Arquitetura.drawio.png)

---

## 🧠 Justificativa da Arquitetura

A arquitetura proposta segue o padrão de **sistemas distribuídos baseados em agentes IA e microserviços**, garantindo **modularidade, resiliência e escalabilidade**.  
A comunicação entre os módulos é realizada via **API REST**, simplificando a integração e permitindo que cada agente possa ser desenvolvido e implantado de forma independente.

Essa abordagem reflete um modelo **orientado à responsabilidade funcional**, em que cada componente é especializado em uma função do domínio e se comunica por meio de um gateway centralizado.

---

### 🏗️ 1. Estrutura e Papéis dos Componentes

| **Componente** | **Responsabilidade Principal** |
|----------------|--------------------------------|
| 👨‍🌾 **Usuário / WebUI** | Interface de acesso usada por cooperativas e produtores. Envia requisições e exibe resultados. |
| 🚪 **API Gateway** | Ponto único de entrada e roteamento. Gerencia autenticação, controle de acesso e redireciona requisições REST entre agentes. |
| 🌱 **Agente Agronômico** | Atua como **núcleo lógico de decisão**. Recebe solicitações via Gateway, requisita dados dos agentes de clima e preço (por meio do Gateway), integra os resultados e aplica análise preditiva. |
| 🌤️ **Agente Climático** | Consome APIs meteorológicas (Open-Meteo, INMET, WeatherAPI), processa e retorna dados estruturados sobre temperatura, precipitação e umidade. |
| 💰 **Agente de Preço do Café** | Consulta APIs e realiza scraping em fontes como CEPEA, B3 e ICO, retornando dados de preço e tendência de mercado. |
| 🧠 **Serviço Ollama (LLM Local)** | Modelo de linguagem local (Ollama) executado em container, responsável por gerar textos explicativos com base na análise do Agente Agronômico. |
| 🗄️ **Banco de Dados / Storage** | Armazena históricos climáticos, econômicos e relatórios técnicos. |
| 🌎 **Fontes Externas** | APIs e sites públicos de clima e mercado de commodities. |

---

### ⚙️ 2. Comunicação e Integração

A integração entre os agentes ocorre via **API Gateway**, utilizando o protocolo **HTTP REST** e mensagens **JSON padronizadas**.

O **Gateway** centraliza a comunicação e executa funções de:
- Autenticação e autorização;  
- Controle de requisições;  
- Encaminhamento entre serviços;  
- Balanceamento e segurança.  

**Vantagens dessa abordagem:**
- Baixo acoplamento entre serviços;  
- Escalabilidade horizontal;  
- Independência de desenvolvimento e deploy;  
- Facilita o monitoramento e logging centralizado.  

---

### 🧩 3. Fluxo de Execução

1. O **usuário** envia uma solicitação via WebUI, encaminhada ao **API Gateway**.  
2. O **Gateway** direciona a requisição ao **Agente Agronômico**.  
3. O **Agente Agronômico**, por meio do Gateway, requisita dados aos agentes de **Clima** e **Preço do Café**.  
4. Após o retorno das informações, o **Agente Agronômico** integra os dados e solicita ao **Ollama** a geração de um texto explicativo.  
5. O resultado é armazenado no **Banco de Dados** e retornado ao **usuário** via Gateway.  

---

### 🔒 4. Segurança e Confiabilidade

- Autenticação e autorização via tokens JWT no Gateway.  
- Criptografia HTTPS/TLS em todas as comunicações REST.  
- Sanitização e validação de entradas de usuário.

---

### 🧱 5. Justificativa Técnica

- **Microserviços containerizados:** garantem isolamento, escalabilidade e facilidade de implantação.  
- **Gateway como mediador:** centraliza segurança, controle e comunicação entre agentes.  
- **Agente Agronômico como núcleo lógico:** concentra a análise, sem acoplamento direto aos demais serviços.  
- **Modelo de IA local (Ollama):** atende ao requisito de conter um modelo de IA local containerizado.  
- **REST + JSON:** formato padrão, interoperável e simples de integrar.  
- **Facilidade de expansão:** novos agentes (por exemplo, de solo ou pragas) podem ser adicionados sem refatorar o sistema principal.  

---
