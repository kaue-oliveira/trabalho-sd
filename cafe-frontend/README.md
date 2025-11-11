# Café Frontend

Frontend para sistema de análise inteligente de café com recomendações de venda baseadas em IA.

## 🚀 Funcionalidades

### Autenticação & Usuário
- **Login/Registro** - Sistema de autenticação com validações
- **Recuperação de Senha** - Fluxo completo de redefinição
- **Perfil do Usuário** - Edição de dados e exclusão de conta
- **Tipos de Conta** - Produtor ou Cooperativa

### Análises de Café
- **Nova Análise** - Formulário com dados da safra para recomendação de venda
- **Recomendações IA** - Decisões: VENDER, VENDER_PARCIALMENTE ou AGUARDAR
- **Histórico** - Lista de análises anteriores salvas
- **Dashboard** - Visão geral das análises recentes

### Dados da Análise
- **Tipo de Café**: Arábica ou Robusta
- **Localização**: Cidade e Estado
- **Quantidade**: Em kg com validação
- **Data da Colheita**: Período da safra
- **Estado do Café**: Verde, Torrado ou Moído

## 🛠️ Tecnologias

- **React 19** - Biblioteca principal
- **TypeScript** - Tipagem estática
- **React Router DOM** - Navegação SPA
- **Vite** - Build tool e dev server
- **CSS Modules** - Estilização componentizada

## 📦 Estrutura do Projeto

```
src/
├── Components/
│   ├── Modal/           # Modal de notificações
│   ├── Sidebar/         # Navegação lateral
│   └── Form/            # Componentes de formulário
├── context/
│   └── AuthContext.tsx  # Gerenciamento de autenticação
├── hooks/
│   └── useNotification.ts # Hook para notificações
├── pages/
│   ├── AuthPages/       # Login, Registro, Recuperação
│   ├── Dashboard/       # Página inicial
│   ├── NewAnalysis/     # Nova análise
│   ├── HistoricAnalyses/# Histórico
│   ├── Profile/         # Perfil do usuário
│   └── PublicHome/      # Landing page pública
├── types/
│   └── auth.types.ts    # Tipos TypeScript
└── utils/
    └── Validations.ts   # Validações de formulários
```

## 🚀 Como Executar

```bash
# Instalar dependências
yarn install

# Desenvolvimento (http://localhost:5173)
yarn dev

# Build de produção
yarn build

# Preview do build
yarn preview
```

## ⚠️ Status Atual

**🚧 Desenvolvimento em Andamento**

- ✅ **Frontend completo** com todas as páginas
- ✅ **Sistema de autenticação** mockado funcionando
- ✅ **Validações** de formulários implementadas
- ❌ **Integração com backend** pendente
- ❌ **IA real** para análises (atualmente mockada)

---

**Desenvolvido para Trabalho de Sistemas Distribuídos**