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

-- Tabela de preços históricos do café Arábica (últimos 90 dias)
CREATE TABLE IF NOT EXISTS arabica_prices_90d (
    id BIGSERIAL PRIMARY KEY,
    price_date DATE NOT NULL,
    price NUMERIC(12,4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    CONSTRAINT uq_arabica_date UNIQUE (price_date)
);

-- Tabela de preços históricos do café Robusta (últimos 90 dias)
CREATE TABLE IF NOT EXISTS robusta_prices_90d (
    id BIGSERIAL PRIMARY KEY,
    price_date DATE NOT NULL,
    price NUMERIC(12,4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    CONSTRAINT uq_robusta_date UNIQUE (price_date)
);

-- Índices para otimizar consultas por data
CREATE INDEX IF NOT EXISTS idx_arabica_price_date ON arabica_prices_90d(price_date DESC);
CREATE INDEX IF NOT EXISTS idx_robusta_price_date ON robusta_prices_90d(price_date DESC);

-- Dados iniciais de exemplo
INSERT INTO usuarios (nome, email, senha, tipo_conta) VALUES
    ('João Silva', 'joao.produtor@email.com', 'senha123', 'PRODUTOR'),
    ('Cooperativa Café Mineiro', 'coop.mineira@email.com', 'senha456', 'COOPERATIVA')
ON CONFLICT (email) DO NOTHING;

-- Análises para João Silva (Produtor de Arábica)
INSERT INTO analises (usuario_id, tipo_cafe, data_colheita, quantidade, cidade, estado, estado_cafe, data_analise, decisao, explicacao_decisao) VALUES
    (1, 'Arábica', '2024-05-15', 1500.50, 'Varginha', 'MG', 'verde', '2024-06-01', 'VENDER', 'Preço atual favorável para café Arábica de alta qualidade. Clima úmido pode afetar estoque se aguardar. Recomenda-se venda total nos próximos 14 dias.'),
    (1, 'Arábica', '2024-04-20', 800.75, 'Varginha', 'MG', 'verde', '2024-05-10', 'VENDER_PARCIALMENTE', 'Café Arábica com nota excelente (86), mas preço pode subir com chegada do inverno. Vender 60% agora e aguardar valorização do restante.'),
    (1, 'Arábica', '2024-03-10', 1200.00, 'Varginha', 'MG', 'verde', '2024-04-05', 'AGUARDAR', 'Mercado saturado de Arábica neste período. Preços abaixo da média. Condições climáticas estáveis permitem armazenamento por mais 30 dias.'),
    (1, 'Arábica', '2024-06-01', 950.25, 'Varginha', 'MG', 'torrado', '2024-06-20', 'VENDER', 'Café torrado tem prazo de validade reduzido. Preço atual compensa venda imediata. Alta demanda por torrados premium.'),
    (1, 'Arábica', '2024-02-15', 1800.00, 'Varginha', 'MG', 'verde', '2024-03-10', 'VENDER_PARCIALMENTE', 'Grande volume disponível. Vender 40% para capital rápido e aguardar contratos de exportação que fecham em 3 semanas.'),
    (1, 'Arábica', '2024-01-20', 750.50, 'Varginha', 'MG', 'moído', '2024-02-15', 'VENDER', 'Produto moído tem alta rotatividade. Preço está 15% acima da média sazonal. Vender todo estoque para evitar perda de aroma.')
ON CONFLICT (id) DO NOTHING;

-- Análises para Cooperativa Café Mineiro (Robusta)
INSERT INTO analises (usuario_id, tipo_cafe, data_colheita, quantidade, cidade, estado, estado_cafe, data_analise, decisao, explicacao_decisao) VALUES
    (2, 'Robusta', '2024-03-10', 3000.00, 'Linhares', 'ES', 'verde', '2024-04-05', 'AGUARDAR', 'Mercado de Robusta em baixa. Previsão de geada no Paraná pode elevar preços nas próximas semanas. Condições de armazenamento adequadas.'),
    (2, 'Robusta', '2024-04-15', 2500.75, 'Linhares', 'ES', 'verde', '2024-05-20', 'VENDER', 'Alta demanda por Robusta para blends. Preço atingiu patamar ideal. Clima quente do ES pode comprometer qualidade se armazenado por muito tempo.')
ON CONFLICT (id) DO NOTHING;

-- Preços históricos realistas para Arábica (últimos 90 dias com variações sazonais)
INSERT INTO arabica_prices_90d (price_date, price) VALUES
    ('2024-08-15', 645.50), ('2024-08-16', 648.25), ('2024-08-17', 650.75), ('2024-08-18', 647.80), ('2024-08-19', 652.40),
    ('2024-08-20', 655.20), ('2024-08-21', 653.75), ('2024-08-22', 658.90), ('2024-08-23', 661.25), ('2024-08-24', 659.80),
    ('2024-08-25', 657.30), ('2024-08-26', 662.75), ('2024-08-27', 665.40), ('2024-08-28', 663.90), ('2024-08-29', 668.25),
    ('2024-08-30', 670.80), ('2024-08-31', 669.35), ('2024-09-01', 672.60), ('2024-09-02', 675.25), ('2024-09-03', 673.80),
    ('2024-09-04', 678.45), ('2024-09-05', 680.90), ('2024-09-06', 679.25), ('2024-09-07', 682.75), ('2024-09-08', 685.40),
    ('2024-09-09', 683.90), ('2024-09-10', 688.25), ('2024-09-11', 690.70), ('2024-09-12', 689.15), ('2024-09-13', 692.80),
    ('2024-09-14', 695.45), ('2024-09-15', 693.90), ('2024-09-16', 698.25), ('2024-09-17', 700.80), ('2024-09-18', 699.25),
    ('2024-09-19', 702.90), ('2024-09-20', 705.55), ('2024-09-21', 704.00), ('2024-09-22', 707.65), ('2024-09-23', 710.20),
    ('2024-09-24', 708.75), ('2024-09-25', 712.40), ('2024-09-26', 715.05), ('2024-09-27', 713.50), ('2024-09-28', 717.15),
    ('2024-09-29', 719.70), ('2024-09-30', 718.25), ('2024-10-01', 721.90), ('2024-10-02', 724.55), ('2024-10-03', 723.00),
    ('2024-10-04', 726.65), ('2024-10-05', 729.20), ('2024-10-06', 727.75), ('2024-10-07', 731.40), ('2024-10-08', 734.05),
    ('2024-10-09', 732.50), ('2024-10-10', 736.15), ('2024-10-11', 738.70), ('2024-10-12', 737.25), ('2024-10-13', 740.90),
    ('2024-10-14', 743.55), ('2024-10-15', 742.00), ('2024-10-16', 745.65), ('2024-10-17', 748.20), ('2024-10-18', 746.75),
    ('2024-10-19', 750.40), ('2024-10-20', 753.05), ('2024-10-21', 751.50), ('2024-10-22', 755.15), ('2024-10-23', 757.70),
    ('2024-10-24', 756.25), ('2024-10-25', 759.90), ('2024-10-26', 762.55), ('2024-10-27', 761.00), ('2024-10-28', 764.65),
    ('2024-10-29', 767.20), ('2024-10-30', 765.75), ('2024-10-31', 769.40), ('2024-11-01', 772.05), ('2024-11-02', 770.50),
    ('2024-11-03', 774.15), ('2024-11-04', 776.70), ('2024-11-05', 775.25), ('2024-11-06', 778.90), ('2024-11-07', 781.55),
    ('2024-11-08', 780.00), ('2024-11-09', 783.65), ('2024-11-10', 786.20), ('2024-11-11', 784.75), ('2024-11-12', 788.40),
    ('2024-11-13', 791.05), ('2024-11-14', 789.50)
ON CONFLICT (price_date) DO NOTHING;

-- Preços históricos realistas para Robusta (últimos 90 dias com variações sazonais)
INSERT INTO robusta_prices_90d (price_date, price) VALUES
    ('2024-08-15', 420.25), ('2024-08-16', 422.80), ('2024-08-17', 425.35), ('2024-08-18', 423.90), ('2024-08-19', 427.45),
    ('2024-08-20', 430.00), ('2024-08-21', 428.55), ('2024-08-22', 432.10), ('2024-08-23', 434.65), ('2024-08-24', 433.20),
    ('2024-08-25', 436.75), ('2024-08-26', 439.30), ('2024-08-27', 437.85), ('2024-08-28', 441.40), ('2024-08-29', 443.95),
    ('2024-08-30', 442.50), ('2024-08-31', 446.05), ('2024-09-01', 448.60), ('2024-09-02', 447.15), ('2024-09-03', 450.70),
    ('2024-09-04', 453.25), ('2024-09-05', 451.80), ('2024-09-06', 455.35), ('2024-09-07', 457.90), ('2024-09-08', 456.45),
    ('2024-09-09', 460.00), ('2024-09-10', 462.55), ('2024-09-11', 461.10), ('2024-09-12', 464.65), ('2024-09-13', 467.20),
    ('2024-09-14', 465.75), ('2024-09-15', 469.30), ('2024-09-16', 471.85), ('2024-09-17', 470.40), ('2024-09-18', 473.95),
    ('2024-09-19', 476.50), ('2024-09-20', 475.05), ('2024-09-21', 478.60), ('2024-09-22', 481.15), ('2024-09-23', 479.70),
    ('2024-09-24', 483.25), ('2024-09-25', 485.80), ('2024-09-26', 484.35), ('2024-09-27', 487.90), ('2024-09-28', 490.45),
    ('2024-09-29', 489.00), ('2024-09-30', 492.55), ('2024-10-01', 495.10), ('2024-10-02', 493.65), ('2024-10-03', 497.20),
    ('2024-10-04', 499.75), ('2024-10-05', 498.30), ('2024-10-06', 501.85), ('2024-10-07', 504.40), ('2024-10-08', 502.95),
    ('2024-10-09', 506.50), ('2024-10-10', 509.05), ('2024-10-11', 507.60), ('2024-10-12', 511.15), ('2024-10-13', 513.70),
    ('2024-10-14', 512.25), ('2024-10-15', 515.80), ('2024-10-16', 518.35), ('2024-10-17', 516.90), ('2024-10-18', 520.45),
    ('2024-10-19', 523.00), ('2024-10-20', 521.55), ('2024-10-21', 525.10), ('2024-10-22', 527.65), ('2024-10-23', 526.20),
    ('2024-10-24', 529.75), ('2024-10-25', 532.30), ('2024-10-26', 530.85), ('2024-10-27', 534.40), ('2024-10-28', 536.95),
    ('2024-10-29', 535.50), ('2024-10-30', 539.05), ('2024-10-31', 541.60), ('2024-11-01', 540.15), ('2024-11-02', 543.70),
    ('2024-11-03', 546.25), ('2024-11-04', 544.80), ('2024-11-05', 548.35), ('2024-11-06', 550.90), ('2024-11-07', 549.45),
    ('2024-11-08', 553.00), ('2024-11-09', 555.55), ('2024-11-10', 554.10), ('2024-11-11', 557.65), ('2024-11-12', 560.20),
    ('2024-11-13', 558.75), ('2024-11-14', 562.30)
ON CONFLICT (price_date) DO NOTHING;

-- Mensagem de confirmação
DO $$ 
DECLARE
    arabica_count INTEGER;
    robusta_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO arabica_count FROM arabica_prices_90d;
    SELECT COUNT(*) INTO robusta_count FROM robusta_prices_90d;
    
    RAISE NOTICE 'Banco de dados CafeQuality inicializado com sucesso!';
    RAISE NOTICE 'Usuários inseridos: 1 PRODUTOR, 1 COOPERATIVA';
    RAISE NOTICE 'Análises inseridas: 6 para João Silva, 2 para Cooperativa';
    RAISE NOTICE 'Preços históricos inseridos: % para Arábica, % para Robusta', arabica_count, robusta_count;
    RAISE NOTICE 'Período coberto: 15/08/2024 a 14/11/2024 (90 dias)';
    RAISE NOTICE 'Variação Arábica: R$ 645.50 → R$ 789.50 (+22.3%%)';
    RAISE NOTICE 'Variação Robusta: R$ 420.25 → R$ 562.30 (+33.8%%)';
END $$;