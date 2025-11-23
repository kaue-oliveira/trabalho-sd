/**
 * Página de histórico de análises
 * 
 * Lista filtrada e paginada das análises
 * 
 * Filtros: data, tipo de café, decisão
 * Paginação: 3 itens por página
 * Ordenação: mais recentes primeiro
 */

import React, { useMemo, useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../../Components/Sidebar/Sidebar';
import { useAuth } from '../../context/AuthContext';
import styles from './HistoricAnalyses.module.css';

const decisionLabel = (decisao: string) => {
  if (decisao === 'VENDER') return 'Vender Agora';
  return 'Aguardar';
};

const getDecisionClass = (decision: string) => {
  switch (decision) {
    case 'VENDER':
      return `${styles.decisionBadge} ${styles.decisionSell}`;
    case 'AGUARDAR':
      return `${styles.decisionBadge} ${styles.decisionHold}`;
    default:
      return styles.decisionBadge;
  }
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR');
};

const parseDateFromISO = (dateStr: string): Date => {
  return new Date(dateStr);
};

const filterByDateRange = (analysis: any, dateFilter: string): boolean => {
  if (!dateFilter || dateFilter === 'Todos') return true;

  const analysisDate = parseDateFromISO(analysis.data_analise);
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
  const perPage = 3;

  const { analisesUsuario } = useAuth();

  const sortedAnalyses = useMemo(() => {
    return [...analisesUsuario].sort((a, b) => {
      const dateA = new Date(a.data_analise);
      const dateB = new Date(b.data_analise);
      return dateB.getTime() - dateA.getTime();
    });
  }, [analisesUsuario]);

  const dateFilterOptions = useMemo(() => {
    const years = Array.from(new Set(sortedAnalyses.map(a => new Date(a.data_analise).getFullYear().toString())));
    return ['Todos', 'Última Semana', 'Últimos 3 Meses', ...years.sort((a, b) => parseInt(b) - parseInt(a))];
  }, [sortedAnalyses]);

  const uniqueCoffeeTypes = useMemo(() => {
    return ['Todos', ...Array.from(new Set(sortedAnalyses.map(a => a.tipo_cafe))).sort()];
  }, [sortedAnalyses]);

  const uniqueDecisions = useMemo(() => {
    return ['Todos', ...Array.from(new Set(sortedAnalyses.map(a => decisionLabel(a.decisao)))).sort()];
  }, [sortedAnalyses]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();

    return sortedAnalyses.filter(a => {
      const matchesQuery = !q ||
        a.tipo_cafe.toLowerCase().includes(q) ||
        a.explicacao_decisao.toLowerCase().includes(q) ||
        formatDate(a.data_analise).includes(q) ||
        decisionLabel(a.decisao).toLowerCase().includes(q);

      const matchesDate = filterByDateRange(a, dateFilter);
      const matchesCoffeeType = !coffeeTypeFilter || a.tipo_cafe === coffeeTypeFilter;
      const matchesDecision = !decisionFilter || decisionLabel(a.decisao) === decisionFilter;

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
      <Sidebar />
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
                    placeholder="Pesquisar por tipo de café, decisão ou explicação..."
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
                    <th className={`${styles.tableCol} ${styles.tableColDate}`}>Data da Análise</th>
                    <th className={`${styles.tableCol} ${styles.tableColType}`}>Tipo de Café</th>
                    <th className={`${styles.tableCol} ${styles.tableColDecision}`}>Decisão</th>
                    <th className={`${styles.tableCol} ${styles.tableColSummary}`}>Explicação da Decisão</th>
                  </tr>
                </thead>
                <tbody className={styles.tableBody}>
                  {visible.map((analysis) => (
                    <tr key={analysis.id} className={styles.tableRow}>
                      <td className={`${styles.tableCol} ${styles.tableColDate}`}>
                        {formatDate(analysis.data_analise)}
                      </td>
                      <td className={`${styles.tableCol} ${styles.tableColType}`}>
                        {analysis.tipo_cafe}
                      </td>
                      <td className={`${styles.tableCol} ${styles.tableColDecision}`}>
                        <div className={getDecisionClass(analysis.decisao)}>
                          {decisionLabel(analysis.decisao)}
                        </div>
                      </td>
                      <td className={`${styles.tableCol} ${styles.tableColSummary}`}>
                        {analysis.explicacao_decisao}
                      </td>
                    </tr>
                  ))}

                  {visible.length === 0 && (
                    <tr className={styles.tableRow}>
                      <td className={`${styles.tableCol} ${styles.tableColDate}`} colSpan={4} style={{ textAlign: 'center' }}>
                        {analisesUsuario.length === 0 ? 'Nenhuma análise encontrada.' : 'Nenhum resultado encontrado para os filtros aplicados.'}
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className={styles.pagination}>
            <p className={styles.paginationText}>
              Mostrando <strong className={styles.paginationNumber}>{filtered.length === 0 ? 0 : ((page - 1) * perPage + 1)}</strong> a{' '}
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