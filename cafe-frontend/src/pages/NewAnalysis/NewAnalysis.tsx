/**
 * Página de nova análise de café
 * 
 * Formulário para análise com IA + resultados
 * 
 * APIs: /agro/recommend (POST), /analises (POST)
 * Validações: campos obrigatórios, formato
 * Estados: análise em andamento, salvamento
 */

import React, { useState } from 'react';
import styles from './NewAnalysis.module.css';
import Sidebar from '../../Components/Sidebar/Sidebar';
import Modal from '../../Components/Modal/Modal';
import { useNotification } from '../../hooks/useNotification';
import { analysisValidations, requireAuthToken } from '../../utils/Validations';
import { useAuth } from '../../context/AuthContext';

const NewAnalysis: React.FC = () => {
  const { notification, showNotification, closeNotification } = useNotification();
  const { token, addAnalise, logout } = useAuth();

  const [formData, setFormData] = useState({
    tipo_cafe: '',
    data_colheita: '',
    quantidade: '',
    cidade: '',
    estado: '',
    estado_cafe: ''
  });

  const [analysisResult, setAnalysisResult] = useState<{
    decisao: string;
    explicacao_decisao: string;
  } | null>(null);

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleAnalyze = async () => {
    if (!formData.tipo_cafe || !formData.data_colheita || !formData.quantidade ||
      !formData.cidade || !formData.estado || !formData.estado_cafe) {
      showNotification('error', 'Todos os campos são obrigatórios.');
      return;
    }

    const validation = analysisValidations.validateAnalysis({
      tipo_cafe: formData.tipo_cafe,
      cidade: formData.cidade,
      estado: formData.estado,
      quantidade: formData.quantidade
    });

    if (!validation.isValid) {
      showNotification('error', validation.message!);
      return;
    }

    const tokenCheck = requireAuthToken(token);
    if (!tokenCheck.isValid) {
      showNotification('error', tokenCheck.message!);
      return;
    }

    setIsAnalyzing(true);
    setAnalysisResult(null);

    try {
      const API_BASE = (import.meta as any).env?.VITE_API_URL || 'http://localhost:3000';

      const analysisPayload = {
        tipo_cafe: formData.tipo_cafe,
        data_colheita: formData.data_colheita,
        quantidade: parseFloat(formData.quantidade),
        cidade: formData.cidade,
        estado: formData.estado,
        estado_cafe: formData.estado_cafe
      };

      const response = await fetch(`${API_BASE}/agro/recommend`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(analysisPayload)
      });

      if (!response.ok) {
        const contentType = response.headers.get("content-type");

        if (response.status === 401) {
          showNotification("error", "Sua sessão expirou. Faça login novamente.");
          setTimeout(() => {
            logout();
          }, 4000);
          return;
        }

        if (contentType && contentType.includes("application/json")) {
          const data = await response.json();
          throw new Error(data.detail || JSON.stringify(data));
        } else {
          const text = await response.text();
          throw new Error(text);
        }
      }

      const analysisResult = await response.json();
      setAnalysisResult(analysisResult);
      showNotification('success', 'Análise agronômica concluída com sucesso!');

    } catch (error) {
      showNotification('error', 'Erro ao realizar análise. Tente novamente.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const displayCoffeeTypes: Record<string, string> = {
    arabica: "Arábica",
    robusta: "Robusta"
  };

  const handleSaveAnalysis = async () => {
    if (!analysisResult) {
      showNotification('error', 'Realize uma análise antes de salvar.');
      return;
    }

    const tokenCheck = requireAuthToken(token);
    if (!tokenCheck.isValid) {
      showNotification('error', tokenCheck.message!);
      return;
    }

    setIsSaving(true);

    try {
      const analysisToSave = {
        tipo_cafe: displayCoffeeTypes[formData.tipo_cafe] || formData.tipo_cafe,
        data_colheita: formData.data_colheita,
        quantidade: parseFloat(formData.quantidade),
        cidade: formData.cidade,
        estado: formData.estado,
        estado_cafe: formData.estado_cafe,
        data_analise: new Date().toISOString().split('T')[0],
        decisao: analysisResult.decisao.toUpperCase(),
        explicacao_decisao: analysisResult.explicacao_decisao
      };

      const API_BASE = (import.meta as any).env?.VITE_API_URL || 'http://localhost:3000';
      const url = `${API_BASE}/analises`;

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(analysisToSave)
      });

      if (!response.ok) {
        if (response.status === 401) {
          showNotification("error", "Sua sessão expirou. Faça login novamente.");
          setTimeout(() => {
            logout();
          }, 4000);
          setIsSaving(false);
          return;
        }

        let errorMessage = 'Erro desconhecido';
        const contentType = response.headers.get('content-type');

        try {
          if (contentType && contentType.includes('application/json')) {
            const errorData = await response.json();
            errorMessage = errorData.detail || errorData.message || JSON.stringify(errorData);
          } else {
            const errorText = await response.text();
            errorMessage = errorText || `Status ${response.status}`;
          }
        } catch (e) {
          errorMessage = `Status ${response.status} - Não foi possível ler a resposta`;
        }

        showNotification('error', `Erro ao salvar análise: ${errorMessage}`);
        setIsSaving(false);
        return;
      }

      const saved = await response.json();

      try {
        addAnalise(saved);
      } catch (err) {
        console.warn('addAnalise falhou:', err);
      }

      showNotification('success', 'Análise salva com sucesso!');

      setFormData({
        tipo_cafe: '',
        data_colheita: '',
        quantidade: '',
        cidade: '',
        estado: '',
        estado_cafe: ''
      });
      setAnalysisResult(null);

    } catch (error) {
      showNotification('error', `Erro ao salvar análise: ${error instanceof Error ? error.message : 'Erro desconhecido'}`);
    } finally {
      setIsSaving(false);
    }
  };

  const getDecisionBadgeClass = (decisao: string) => {
    const d = decisao.toUpperCase();
    return d === 'AGUARDAR' ? styles.waitBadge : styles.sellBadge;
  };

  const getDecisionText = (decisao: string) => {
    const d = decisao.toUpperCase();
    return d === 'AGUARDAR' ? 'AGUARDAR' : 'VENDER';
  };


  return (
    <div className={styles.page}>
      <div className={styles.layout}>
        <Sidebar />

        <main className={styles.main}>
          <div className={styles.container}>
            <div className={styles.header}>
              <h1 className={styles.title}>Nova Análise</h1>
              <p className={styles.subtitle}>
                Preencha os detalhes abaixo para receber uma recomendação de venda com IA.
              </p>
            </div>

            <div className={styles.grid}>
              <div className={styles.formPanel}>
                <form className={styles.form}>
                  <label className={styles.field}>
                    <p className={styles.label}>Tipo de Café *</p>
                    <select
                      className={styles.select}
                      value={formData.tipo_cafe}
                      onChange={(e) => handleInputChange('tipo_cafe', e.target.value)}
                      disabled={isAnalyzing}
                      required
                    >
                      <option value="">Selecione o tipo de café</option>
                      <option value="arabica">Arábica</option>
                      <option value="robusta">Robusta</option>
                    </select>
                  </label>

                  <label className={styles.field}>
                    <p className={styles.label}>Data da Colheita *</p>
                    <div className={styles.inputWrapper}>
                      <input
                        className={styles.input}
                        type="date"
                        value={formData.data_colheita}
                        onChange={(e) => handleInputChange('data_colheita', e.target.value)}
                        disabled={isAnalyzing}
                        required
                      />
                    </div>
                  </label>

                  <div className={styles.row}>
                    <label className={styles.field}>
                      <p className={styles.label}>Quantidade (kg) *</p>
                      <input
                        className={styles.input}
                        type="text"
                        placeholder="Ex: 5000"
                        value={formData.quantidade}
                        onChange={(e) => handleInputChange('quantidade', e.target.value)}
                        disabled={isAnalyzing}
                        required
                      />
                    </label>

                    <label className={styles.field}>
                      <p className={styles.label}>Estado do Café *</p>
                      <select
                        className={styles.select}
                        value={formData.estado_cafe}
                        onChange={(e) => handleInputChange('estado_cafe', e.target.value)}
                        disabled={isAnalyzing}
                        required
                      >
                        <option value="">Selecione o estado</option>
                        <option value="verde">Verde</option>
                        <option value="torrado">Torrado</option>
                        <option value="moído">Moído</option>
                      </select>
                    </label>
                  </div>

                  <div className={styles.row}>
                    <label className={styles.field}>
                      <p className={styles.label}>Cidade *</p>
                      <input
                        className={styles.input}
                        type="text"
                        placeholder="Ex: Varginha"
                        value={formData.cidade}
                        onChange={(e) => handleInputChange('cidade', e.target.value)}
                        disabled={isAnalyzing}
                        required
                      />
                    </label>

                    <label className={styles.field}>
                      <p className={styles.label}>Estado (UF) *</p>
                      <select
                        className={styles.select}
                        value={formData.estado}
                        onChange={(e) => handleInputChange('estado', e.target.value)}
                        disabled={isAnalyzing}
                        required
                      >
                        <option value="">Selecione o estado</option>
                        <option value="AC">AC</option>
                        <option value="AL">AL</option>
                        <option value="AP">AP</option>
                        <option value="AM">AM</option>
                        <option value="BA">BA</option>
                        <option value="CE">CE</option>
                        <option value="DF">DF</option>
                        <option value="ES">ES</option>
                        <option value="GO">GO</option>
                        <option value="MA">MA</option>
                        <option value="MT">MT</option>
                        <option value="MS">MS</option>
                        <option value="MG">MG</option>
                        <option value="PA">PA</option>
                        <option value="PB">PB</option>
                        <option value="PR">PR</option>
                        <option value="PE">PE</option>
                        <option value="PI">PI</option>
                        <option value="RJ">RJ</option>
                        <option value="RN">RN</option>
                        <option value="RS">RS</option>
                        <option value="RO">RO</option>
                        <option value="RR">RR</option>
                        <option value="SC">SC</option>
                        <option value="SP">SP</option>
                        <option value="SE">SE</option>
                        <option value="TO">TO</option>
                      </select>
                    </label>
                  </div>

                  <button
                    className={styles.analyzeButton}
                    type="button"
                    onClick={handleAnalyze}
                    disabled={isAnalyzing}
                  >
                    {isAnalyzing ? (
                      <>
                        <span className={styles.spinner}></span>
                        ANALISANDO...
                      </>
                    ) : (
                      'ANALISAR'
                    )}
                  </button>
                </form>
              </div>

              <div className={styles.resultsPanel}>
                <div className={styles.resultsContent}>
                  {isAnalyzing ? (
                    <div className={styles.loadingState}>
                      <div className={styles.loadingSpinner}></div>
                      <h3 className={styles.loadingTitle}>Analisando dados...</h3>
                      <p className={styles.loadingText}>
                        Nossa IA está processando as informações do seu café para fornecer a melhor recomendação.
                      </p>
                    </div>
                  ) : analysisResult ? (
                    <div className={styles.resultSection}>
                      <div className={styles.resultHeader}>
                        <div className={`${styles.resultBadge} ${getDecisionBadgeClass(analysisResult.decisao)}`}>
                          {getDecisionText(analysisResult.decisao)}
                        </div>
                      </div>

                      <div className={styles.recommendation}>
                        <h3 className={styles.recommendationTitle}>Recomendação da IA</h3>
                        <p className={styles.recommendationText}>
                          {analysisResult.explicacao_decisao}
                        </p>
                      </div>

                      <div className={styles.saveSection}>
                        <button
                          className={styles.saveButton}
                          type="button"
                          onClick={handleSaveAnalysis}
                          disabled={isSaving}
                        >
                          {isSaving ? (
                            <>
                              <span className={styles.smallSpinner}></span>
                              Salvando...
                            </>
                          ) : (
                            'Salvar Análise'
                          )}
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className={styles.emptyState}>
                      <i className={`${styles.materialIcon} ${styles.emptyStateIcon}`}>analytics</i>
                      <h3 className={styles.emptyStateTitle}>Análise Pendente</h3>
                      <p className={styles.emptyStateText}>
                        Preencha o formulário ao lado e clique em "ANALISAR" para receber uma recomendação de venda baseada em IA.
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
      <Modal
        isOpen={notification.isOpen}
        onClose={closeNotification}
        type={notification.type}
        message={notification.message}
        duration={notification.type === 'success' ? 3000 : 4000}
      />
    </div>
  );
};

export default NewAnalysis;