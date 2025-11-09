-- Script de inicialização do banco de dados CafeQuality

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo_conta VARCHAR(20) NOT NULL CHECK (tipo_conta IN ('PRODUTOR', 'COOPERATIVA')),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de análises
CREATE TABLE IF NOT EXISTS analises (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    tipo_cafe VARCHAR(100) NOT NULL,
    data_colheita DATE NOT NULL,
    quantidade DECIMAL(10,2) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    estado_cafe VARCHAR(20) NOT NULL CHECK (estado_cafe IN ('verde', 'torrado', 'moído')),
    data_analise DATE NOT NULL,
    decisao VARCHAR(20) NOT NULL CHECK (decisao IN ('VENDER', 'VENDER_PARCIALMENTE', 'AGUARDAR')),
    explicacao_decisao TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dados iniciais de exemplo
INSERT INTO usuarios (nome, email, senha, tipo_conta) VALUES
    ('João Silva', 'joao.produtor@email.com', 'senha123', 'PRODUTOR'),
    ('Cooperativa Café Mineiro', 'coop.mineira@email.com', 'senha456', 'COOPERATIVA')
ON CONFLICT (email) DO NOTHING;

-- Análises para João Silva
INSERT INTO analises (usuario_id, tipo_cafe, data_colheita, quantidade, cidade, estado, estado_cafe, data_analise, decisao, explicacao_decisao) VALUES
    (1, 'Arábica', '2024-05-15', 1500.50, 'Varginha', 'MG', 'verde', '2024-06-01', 'VENDER', 'Preço atual favorável para café Arábica de alta qualidade. Clima úmido pode afetar estoque se aguardar. Recomenda-se venda total nos próximos 14 dias.'),
    (1, 'Bourbon', '2024-04-20', 800.75, 'Varginha', 'MG', 'verde', '2024-05-10', 'VENDER_PARCIALMENTE', 'Café Bourbon com nota excelente (86), mas preço pode subir com chegada do inverno. Vender 60% agora e aguardar valorização do restante.'),
    (1, 'Catuaí', '2024-03-10', 1200.00, 'Varginha', 'MG', 'verde', '2024-04-05', 'AGUARDAR', 'Mercado saturado de Catuaí neste período. Preços abaixo da média. Condições climáticas estáveis permitem armazenamento por mais 30 dias.'),
    (1, 'Arábica', '2024-06-01', 950.25, 'Varginha', 'MG', 'torrado', '2024-06-20', 'VENDER', 'Café torrado tem prazo de validade reduzido. Preço atual compensa venda imediata. Alta demanda por torrados premium.'),
    (1, 'Mundo Novo', '2024-02-15', 1800.00, 'Varginha', 'MG', 'verde', '2024-03-10', 'VENDER_PARCIALMENTE', 'Grande volume disponível. Vender 40% para capital rápido e aguardar contratos de exportação que fecham em 3 semanas.'),
    (1, 'Bourbon', '2024-01-20', 750.50, 'Varginha', 'MG', 'moído', '2024-02-15', 'VENDER', 'Produto moído tem alta rotatividade. Preço está 15% acima da média sazonal. Vender todo estoque para evitar perda de aroma.')
ON CONFLICT (id) DO NOTHING;

-- Análises para Cooperativa Café Mineiro
INSERT INTO analises (usuario_id, tipo_cafe, data_colheita, quantidade, cidade, estado, estado_cafe, data_analise, decisao, explicacao_decisao) VALUES
    (2, 'Conilon', '2024-03-10', 3000.00, 'Linhares', 'ES', 'verde', '2024-04-05', 'AGUARDAR', 'Mercado de Conilon em baixa. Previsão de geada no Paraná pode elevar preços nas próximas semanas. Condições de armazenamento adequadas.'),
    (2, 'Robusta', '2024-04-15', 2500.75, 'Linhares', 'ES', 'verde', '2024-05-20', 'VENDER', 'Alta demanda por Robusta para blends. Preço atingiu patamar ideal. Clima quente do ES pode comprometer qualidade se armazenado por muito tempo.')
ON CONFLICT (id) DO NOTHING;

-- Mensagem de confirmação
DO $$ 
BEGIN
    RAISE NOTICE 'Banco de dados CafeQuality inicializado com sucesso!';
    RAISE NOTICE 'Usuários inseridos: 1 PRODUTOR, 1 COOPERATIVA';
    RAISE NOTICE 'Análises inseridas: 6 para João Silva, 2 para Cooperativa';
END $$;