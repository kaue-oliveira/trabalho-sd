// HistoricAnalyses.tsx
import React, { useMemo, useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../../Components/Sidebar/Sidebar';
import styles from './HistoricAnalyses.module.css';

type Analysis = {
  date: string;
  coffeeType: string;
  decision: 'SELL' | 'HOLD' | 'PARTIAL SELL';
  summary: string;
};

const initialAnalyses: Analysis[] = [
  { date: '05/06/2023', coffeeType: 'Arábica - Bourbon Amarelo', decision: 'HOLD', summary: 'Qualidade excepcional. Aguardar pico de preços.' },
  { date: '10/07/2023', coffeeType: 'Liberica - Excelsa', decision: 'SELL', summary: 'Demanda forte em mercados asiáticos. Venda recomendada.' },
  { date: '15/08/2023', coffeeType: 'Arábica - Mundo Novo', decision: 'PARTIAL SELL', summary: 'Vender 50% e aguardar valorização do restante.' },
  { date: '20/09/2023', coffeeType: 'Arábica - Catuaí', decision: 'HOLD', summary: 'Aguardar melhores condições de mercado nas próximas semanas.' },
  { date: '28/09/2023', coffeeType: 'Robusta - Conillon', decision: 'SELL', summary: 'Mercado aquecido e boa safra. Recomenda-se venda imediata.' },
  { date: '05/10/2023', coffeeType: 'Arábica - Geisha', decision: 'HOLD', summary: 'Lote premium. Projeções indicam aumento de ~15% no mês seguinte; aguardar é recomendado.' },
  { date: '09/10/2023', coffeeType: 'Liberica - Barako', decision: 'SELL', summary: 'Alta demanda em mercados especiais. Momento ideal para venda.' },
  { date: '11/10/2023', coffeeType: 'Arábica - Bourbon', decision: 'PARTIAL SELL', summary: 'Qualidade mista. Recomenda-se vender 60% agora e manter o restante para nova avaliação.' },
  { date: '12/10/2023', coffeeType: 'Robusta - Nganda', decision: 'HOLD', summary: 'Preços baixos no momento; recomenda-se aguardar 2-3 semanas para possível recuperação.' },
  { date: '15/10/2023', coffeeType: 'Arábica - Caturra', decision: 'SELL', summary: 'Condições favoráveis no mercado e qualidade no pico; venda imediata para maximizar lucro.' },
  { date: '15/03/2024', coffeeType: 'Arábica - Catimor', decision: 'PARTIAL SELL', summary: 'Qualidade comercial. Vender 80% agora.' },
  { date: '25/08/2024', coffeeType: 'Arábica - Maragogipe', decision: 'HOLD', summary: 'Grãos grandes e qualidade superior. Aguardar valorização.' },
  { date: '05/09/2024', coffeeType: 'Liberica - Liberica', decision: 'SELL', summary: 'Rara oportunidade de mercado. Venda imediata recomendada.' },
  { date: '10/10/2024', coffeeType: 'Arábica - Pacamara', decision: 'PARTIAL SELL', summary: 'Lote especial. Vender 70% e manter o premium.' },
  { date: '20/11/2024', coffeeType: 'Robusta - Kouillou', decision: 'HOLD', summary: 'Mercado estável. Aguardar tendência de alta.' },
  { date: '28/10/2024', coffeeType: 'Robusta - Erecta', decision: 'HOLD', summary: 'Mercado em recuperação. Aguardar 2 semanas.' },
  { date: '15/12/2024', coffeeType: 'Arábica - Typica', decision: 'SELL', summary: 'Excelente momento de mercado. Preços em alta.' },
  { date: '12/01/2025', coffeeType: 'Arábica - SL28', decision: 'SELL', summary: 'Variedade queniana em alta demanda. Momento perfeito para venda.' },
  { date: '05/02/2025', coffeeType: 'Robusta - Conillon', decision: 'HOLD', summary: 'Mercado em leve queda; aguardar 1-2 semanas pode render melhor preço.' },
  { date: '18/02/2025', coffeeType: 'Arábica - Geisha', decision: 'SELL', summary: 'Alta procura internacional. Lucros acima da média esperados.' },
  { date: '03/03/2025', coffeeType: 'Liberica - Barako', decision: 'PARTIAL SELL', summary: 'Demanda crescente. Vender metade agora e monitorar mercado.' },
  { date: '22/03/2025', coffeeType: 'Arábica - Catuaí Vermelho', decision: 'HOLD', summary: 'Preços estáveis, mas tendência de alta a curto prazo.' },
  { date: '10/04/2025', coffeeType: 'Robusta - Nganda', decision: 'SELL', summary: 'Mercado aquecido após baixa produção no Vietnã.' },
  { date: '27/04/2025', coffeeType: 'Arábica - Mundo Novo', decision: 'HOLD', summary: 'Expectativa de aumento de 10% nas próximas semanas.' },
  { date: '15/05/2025', coffeeType: 'Arábica - Bourbon Amarelo', decision: 'SELL', summary: 'Pico de qualidade e alta demanda em cafés gourmet.' },
  { date: '30/06/2025', coffeeType: 'Robusta - Kouillou', decision: 'PARTIAL SELL', summary: 'Estoque elevado. Vender 60% e manter o restante.' },
  { date: '14/07/2025', coffeeType: 'Arábica - Typica', decision: 'HOLD', summary: 'Condições climáticas favoráveis sugerem valorização futura.' },
  { date: '02/08/2025', coffeeType: 'Liberica - Excelsa', decision: 'SELL', summary: 'Alta exportação para o leste asiático. Venda imediata recomendada.' },
  { date: '25/09/2025', coffeeType: 'Arábica - Pacamara', decision: 'HOLD', summary: 'Mercado estável, mas com potencial de alta no próximo trimestre.' },
  { date: '05/10/2025', coffeeType: 'Arábica - Catimor', decision: 'PARTIAL SELL', summary: 'Lote comercial de boa qualidade. Vender 70% agora.' },
  { date: '21/10/2025', coffeeType: 'Robusta - Erecta', decision: 'SELL', summary: 'Demanda repentina em torrefações europeias. Venda total sugerida.' },
  { date: '02/11/2025', coffeeType: 'Arábica - Caturra', decision: 'HOLD', summary: 'Tendência de alta sustentada. Aguardar mais uma semana.' }
];

const decisionLabel = (d: Analysis['decision']) => {
  if (d === 'SELL') return 'Vender Agora';
  if (d === 'HOLD') return 'Aguardar';
  return 'Vender Parcialmente';
};

const getDecisionClass = (decision: Analysis['decision']) => {
  switch (decision) {
    case 'SELL':
      return `${styles.decisionBadge} ${styles.decisionSell}`;
    case 'HOLD':
      return `${styles.decisionBadge} ${styles.decisionHold}`;
    case 'PARTIAL SELL':
      return `${styles.decisionBadge} ${styles.decisionPartial}`;
    default:
      return styles.decisionBadge;
  }
};

// Função para converter data dd/mm/yyyy para Date
const parseDate = (dateStr: string): Date => {
  const [day, month, year] = dateStr.split('/').map(Number);
  return new Date(year, month - 1, day);
};

// Função para filtrar por período
const filterByDateRange = (analysis: Analysis, dateFilter: string): boolean => {
  if (!dateFilter || dateFilter === 'Todos') return true;

  const analysisDate = parseDate(analysis.date);
  const now = new Date();

  if (dateFilter === 'Última Semana') {
    const weekAgo = new Date(now);
    weekAgo.setDate(now.getDate() - 7);
    return analysisDate >= weekAgo;
  }

  if (dateFilter === 'Últimos 3 Meses') {
    const threeMonthsAgo = new Date(now);
    threeMonthsAgo.setMonth(now.getMonth() - 3);
    return analysisDate >= threeMonthsAgo;
  }

  // Filtro por ano específico
  if (dateFilter.match(/^\d{4}$/)) {
    const year = parseInt(dateFilter);
    return analysisDate.getFullYear() === year;
  }

  return true;
};

type FilterDropdownProps = {
  label: string;
  options: string[];
  selected: string;
  onSelect: (value: string) => void;
};

const FilterDropdown: React.FC<FilterDropdownProps> = ({ label, options, selected, onSelect }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const [dropdownPosition, setDropdownPosition] = useState({ top: 0, left: 0, width: 0 });

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node) &&
          buttonRef.current && !buttonRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  useEffect(() => {
    if (isOpen && buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      setDropdownPosition({
        top: rect.bottom + window.scrollY + 8,
        left: rect.left + window.scrollX,
        width: rect.width
      });
    }
  }, [isOpen]);

  const displayLabel = selected || label;

  return (
    <>
      <button
        ref={buttonRef}
        className={`${styles.filterChip} ${isOpen ? styles.filterChipActive : ''}`}
        onClick={() => setIsOpen(!isOpen)}
      >
        <p className={styles.chipText}>{displayLabel}</p>
        <i className={`${styles.materialIcon} ${styles.icon} ${isOpen ? styles.iconRotated : ''}`}>
          expand_more
        </i>
      </button>

      {isOpen && (
        <div
          ref={dropdownRef}
          className={styles.dropdownMenu}
          style={{
            position: 'fixed',
            top: `${dropdownPosition.top}px`,
            left: `${dropdownPosition.left}px`,
            minWidth: `${dropdownPosition.width}px`
          }}
        >
          {options.map((option) => (
            <div
              key={option}
              className={`${styles.dropdownItem} ${selected === option ? styles.dropdownItemActive : ''}`}
              onClick={() => {
                onSelect(option === 'Todos' ? '' : option);
                setIsOpen(false);
              }}
            >
              {option}
            </div>
          ))}
        </div>
      )}
    </>
  );
};

const HistoricAnalyses: React.FC = () => {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [page, setPage] = useState(1);
  const [dateFilter, setDateFilter] = useState('');
  const [coffeeTypeFilter, setCoffeeTypeFilter] = useState('');
  const [decisionFilter, setDecisionFilter] = useState('');
  const perPage = 5;

  const userName = 'Gabriel';

  const [analyses] = useState<Analysis[]>(initialAnalyses);

  // Ordenar análises do mais recente para o mais antigo
  const sortedAnalyses = useMemo(() => {
    return [...analyses].sort((a, b) => {
      const dateA = parseDate(a.date);
      const dateB = parseDate(b.date);
      return dateB.getTime() - dateA.getTime();
    });
  }, [analyses]);

  const dateFilterOptions = ['Todos', 'Última Semana', 'Últimos 3 Meses', '2025', '2024', '2023'];

  const uniqueCoffeeTypes = useMemo(() => {
    return ['Todos', ...Array.from(new Set(sortedAnalyses.map(a => a.coffeeType))).sort()];
  }, [sortedAnalyses]);

  const uniqueDecisions = useMemo(() => {
    return ['Todos', ...Array.from(new Set(sortedAnalyses.map(a => decisionLabel(a.decision)))).sort()];
  }, [sortedAnalyses]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    
    return sortedAnalyses.filter(a => {
      const matchesQuery = !q || 
        a.coffeeType.toLowerCase().includes(q) ||
        a.summary.toLowerCase().includes(q) ||
        a.date.includes(q) ||
        decisionLabel(a.decision).toLowerCase().includes(q);

      const matchesDate = filterByDateRange(a, dateFilter);
      const matchesCoffeeType = !coffeeTypeFilter || a.coffeeType === coffeeTypeFilter;
      const matchesDecision = !decisionFilter || decisionLabel(a.decision) === decisionFilter;

      return matchesQuery && matchesDate && matchesCoffeeType && matchesDecision;
    });
  }, [sortedAnalyses, query, dateFilter, coffeeTypeFilter, decisionFilter]);

  const pageCount = Math.max(1, Math.ceil(filtered.length / perPage));
  const visible = filtered.slice((page - 1) * perPage, page * perPage);

  const handleNewAnalysis = () => {
    navigate('/nova-analise');
  };

  const handleFilterChange = () => {
    setPage(1);
  };

  useEffect(() => {
    handleFilterChange();
  }, [dateFilter, coffeeTypeFilter, decisionFilter]);

  return (
    <div className={styles.container}>
      <Sidebar userName={userName} />

      <main className={styles.mainContent}>
        <div className={styles.contentContainer}>
          <div className={styles.pageHeader}>
            <div className={styles.headerText}>
              <h1 className={styles.title}>Histórico de Análises</h1>
              <p className={styles.subtitle}>Visualize, filtre e gerencie todas as suas análises recentes.</p>
            </div>

            <button className={styles.newAnalysisButton} onClick={handleNewAnalysis}>
              <i className={`${styles.materialIcon} ${styles.icon}`}>add_circle</i>
              Nova Análise
            </button>
          </div>

          <div className={styles.filters}>
            <div className={styles.searchContainer}>
              <label className={styles.searchLabel}>
                <div className={styles.searchWrapper}>
                  <div className={styles.searchIcon}>
                    <i className={`${styles.materialIcon} ${styles.icon}`}>search</i>
                  </div>
                  <input
                    className={styles.searchInput}
                    placeholder="Pesquisar por palavra-chave no resumo da IA..."
                    type="text"
                    value={query}
                    onChange={(e) => { setQuery(e.target.value); setPage(1); }}
                  />
                </div>
              </label>
            </div>

            <div className={styles.filterChips}>
              <FilterDropdown
                label="Intervalo de Data"
                options={dateFilterOptions}
                selected={dateFilter}
                onSelect={setDateFilter}
              />
              <FilterDropdown
                label="Tipo de Café"
                options={uniqueCoffeeTypes}
                selected={coffeeTypeFilter}
                onSelect={setCoffeeTypeFilter}
              />
              <FilterDropdown
                label="Decisão"
                options={uniqueDecisions}
                selected={decisionFilter}
                onSelect={setDecisionFilter}
              />
            </div>
          </div>

          <div className={styles.tableContainer}>
            <div className={styles.tableWrapper}>
              <table className={styles.table}>
                <thead>
                  <tr className={styles.tableHeader}>
                    <th className={`${styles.tableCol} ${styles.tableColDate}`}>Data</th>
                    <th className={`${styles.tableCol} ${styles.tableColType}`}>Tipo de Café</th>
                    <th className={`${styles.tableCol} ${styles.tableColDecision}`}>Decisão</th>
                    <th className={`${styles.tableCol} ${styles.tableColSummary}`}>Resumo da IA</th>
                  </tr>
                </thead>
                <tbody className={styles.tableBody}>
                  {visible.map((analysis, index) => (
                    <tr key={index} className={styles.tableRow}>
                      <td className={`${styles.tableCol} ${styles.tableColDate}`}>{analysis.date}</td>
                      <td className={`${styles.tableCol} ${styles.tableColType}`}>{analysis.coffeeType}</td>
                      <td className={`${styles.tableCol} ${styles.tableColDecision}`}>
                        <div className={getDecisionClass(analysis.decision)}>
                          {decisionLabel(analysis.decision)}
                        </div>
                      </td>
                      <td className={`${styles.tableCol} ${styles.tableColSummary}`}>{analysis.summary}</td>
                    </tr>
                  ))}

                  {visible.length === 0 && (
                    <tr className={styles.tableRow}>
                      <td className={`${styles.tableCol} ${styles.tableColDate}`} colSpan={4} style={{ textAlign: 'center' }}>
                        Nenhum resultado encontrado.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className={styles.pagination}>
            <p className={styles.paginationText}>
              Mostrando <strong className={styles.paginationNumber}>{filtered.length === 0 ? 0 : ( (page - 1) * perPage + 1 )}</strong> a{' '}
              <strong className={styles.paginationNumber}>{Math.min(page * perPage, filtered.length)}</strong> de{' '}
              <strong className={styles.paginationNumber}>{filtered.length}</strong> resultados
            </p>

            <div className={styles.paginationControls}>
              <button
                className={styles.paginationButton}
                onClick={(e) => {
                  setPage(p => Math.max(1, p - 1));
                  e.currentTarget.blur();
                }}
                disabled={page === 1}
                aria-label="Página anterior"
              >
                <i className={`${styles.materialIcon} ${styles.icon}`}>chevron_left</i>
              </button>
              <button
                className={styles.paginationButton}
                onClick={(e) => {
                  setPage(p => Math.min(pageCount, p + 1));
                  e.currentTarget.blur();
                }}
                disabled={page === pageCount}
                aria-label="Próxima página"
              >
                <i className={`${styles.materialIcon} ${styles.icon}`}>chevron_right</i>
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default HistoricAnalyses;