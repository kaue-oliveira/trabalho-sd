import React, { useState } from 'react';
import styles from './NewAnalysis.module.css';
import Sidebar from '../../Components/Sidebar/Sidebar';
import Modal from '../../Components/Modal/Modal';
import { useNotification } from '../../hooks/useNotification';
import { analysisValidations, requireAuthToken } from '../../utils/Validations';
import { useAuth } from '../../context/AuthContext';

const NewAnalysis: React.FC = () => {
  const { notification, showNotification, closeNotification } = useNotification();
  const { token, addAnalise } = useAuth();

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


    try {
      const tokenCheck = requireAuthToken(token);
      if (!tokenCheck.isValid) {
        showNotification('error', tokenCheck.message!);
        return;
      }

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
        const errorText = await response.text();
        throw new Error(errorText || 'Erro na análise agronômica');
      }

      const analysisResult = await response.json();

      setAnalysisResult(analysisResult);
      showNotification('success', 'Análise agronômica concluída com sucesso!');

    } catch (error) {
      console.error('Erro na análise agronômica:', error);
      showNotification('error', 'Erro ao realizar análise. Tente novamente.');
    }
  };

  const handleSaveAnalysis = async () => {
    if (!analysisResult) {
      showNotification('error', 'Realize uma análise antes de salvar.');
      return;
    }

    try {
      const analysisToSave = {
        ...formData,
        quantidade: parseFloat(formData.quantidade),
        data_analise: new Date().toISOString().split('T')[0],
        ...analysisResult
      };

      const tokenCheck = requireAuthToken(token);
      if (!tokenCheck.isValid) {
        showNotification('error', tokenCheck.message!);
        return;
      }

      const API_BASE = (import.meta as any).env?.VITE_API_URL || 'http://localhost:3000';
      const response = await fetch(`${API_BASE}/analises`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(analysisToSave)
      });

      if (!response.ok) {
        const errorText = await response.text();
        showNotification('error', `Erro ao salvar análise: ${errorText}`);
        return;
      }

      const saved = await response.json();

      try {
        addAnalise(saved);
      } catch (err) {
        console.warn('addAnalise falhou:', err);
      }

      showNotification('success', 'Análise salva com sucesso!');

      // Limpar formulário após salvar
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
      showNotification('error', 'Erro ao salvar análise. Tente novamente.');
    }
  };

  const getDecisionBadgeClass = (decisao: string) => {
    switch (decisao) {
      case 'VENDER':
        return styles.sellBadge;
      case 'AGUARDAR':
        return styles.waitBadge;
      default:
        return styles.sellBadge;
    }
  };

  const getDecisionText = (decisao: string) => {
    switch (decisao) {
      case 'VENDER':
        return 'VENDER';
      case 'AGUARDAR':
        return 'AGUARDAR';
      default:
        return 'VENDER';
    }
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
                      required
                    >
                      <option value="">Selecione o tipo de café</option>
                      <option value="Arábica">Arábica</option>
                      <option value="Robusta">Robusta</option>
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
                        required
                      />
                    </label>

                    <label className={styles.field}>
                      <p className={styles.label}>Estado do Café *</p>
                      <select
                        className={styles.select}
                        value={formData.estado_cafe}
                        onChange={(e) => handleInputChange('estado_cafe', e.target.value)}
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
                        required
                      />
                    </label>

                    <label className={styles.field}>
                      <p className={styles.label}>Estado (UF) *</p>
                      <select
                        className={styles.select}
                        value={formData.estado}
                        onChange={(e) => handleInputChange('estado', e.target.value)}
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
                  >
                    ANALISAR
                  </button>
                </form>
              </div>

              <div className={styles.resultsPanel}>
                <div className={styles.resultsContent}>
                  {analysisResult ? (
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
                        >
                          Salvar Análise
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