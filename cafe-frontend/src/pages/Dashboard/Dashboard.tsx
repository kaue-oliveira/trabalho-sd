import styles from './Dashboard.module.css';
import { Link, useNavigate } from 'react-router-dom';
import Sidebar from '../../Components/Sidebar/Sidebar';
import { useAuth } from '../../context/AuthContext';

const Dashboard: React.FC = () => {
  const { user, analisesUsuario } = useAuth();
  const navigate = useNavigate();

  const userName = user?.nome || "Usuário";
  
  const handleNewAnalysis = () => {
    console.log("Nova análise iniciada");
    navigate('/nova-analise');
  };

  const handleAnalyses = () => {
    console.log("Acessar minhas análises");
    navigate('/historico-analises');
  };

  const recentAnalyses = analisesUsuario
    .sort((a, b) => b.id - a.id) // Ordenar por ID decrescente (mais recentes primeiro)
    .slice(0, 4); // Pegar apenas as 4 mais recentes

  // **CALCULAR ESTATÍSTICAS COM DADOS REAIS**
  const sellNowCount = analisesUsuario.filter(a => a.decisao === "VENDER").length;
  const sellPartiallyCount = analisesUsuario.filter(a => a.decisao === "VENDER_PARCIALMENTE").length;
  const waitCount = analisesUsuario.filter(a => a.decisao === "AGUARDAR").length;
  const totalAnalises = analisesUsuario.length;

  // **FORMATAR DADOS PARA A TABELA**
  const formatAnalysisForTable = (analise: any) => ({
    id: `AN-${analise.id.toString().padStart(3, '0')}`,
    date: new Date(analise.data_colheita).toLocaleDateString('pt-BR'),
    coffeeType: analise.tipo_cafe,
    quantity: `${analise.quantidade} kg`,
    decision: analise.decisao === "VENDER" ? "Vender Agora" : 
              analise.decisao === "VENDER_PARCIALMENTE" ? "Vender Parcialmente" : 
              "Aguardar"
  });

  const tableAnalyses = recentAnalyses.map(formatAnalysisForTable);

  return (
    <div className={styles.dashboard}>
      <Sidebar />
  
      <div className={styles.mainContent}>
        <main className={styles.main}>
          <section className={styles.heroSection}>
            <div className={styles.heroContent}>
              <div className={styles.heroText}>
                <h1 className={styles.heroTitle}>Bem-vindo de volta, {userName}!</h1>
                <p className={styles.heroSubtitle}>
                  Sua plataforma para análise inteligente de decisões de venda do café.
                </p>
              </div>
              <div className={styles.heroActions}>
                <button className={styles.primaryButton} onClick={handleNewAnalysis}>
                  <i className={styles.materialIcon}>add_circle</i>
                  <div>Nova Análise</div>
                </button>
                <button className={styles.secondaryButton} onClick={handleAnalyses}>
                  <i className={styles.materialIcon}>history</i>
                  <div>Análises Recentes</div>
                </button>
              </div>
            </div>
          </section>

          <section className={styles.statsSection}>
            <h2 className={styles.sectionTitle}>Visão Geral das Decisões</h2>
            <div className={styles.statsGrid}>
              <div className={styles.statCard}>
                <p className={styles.statLabel}>Vender Agora</p>
                <p className={styles.statValue}>{sellNowCount}</p>
              </div>
              <div className={styles.statCard}>
                <p className={styles.statLabel}>Vender Parcialmente</p>
                <p className={styles.statValue}>{sellPartiallyCount}</p>
              </div>
              <div className={styles.statCard}>
                <p className={styles.statLabel}>Aguardar</p>
                <p className={styles.statValue}>{waitCount}</p>
              </div>
              <div className={styles.statCard}>
                <p className={styles.statLabel}>Total de Análises</p>
                <p className={styles.statValue}>{totalAnalises}</p>
              </div>
            </div>
          </section>

          <section className={styles.analysesSection}>
            <div className={styles.sectionHeader}>
              <h2 className={styles.sectionTitle}>Análises Recentes</h2>
              <Link className={styles.viewAllLink} to="/historico-analises">Ver Todas</Link>
            </div>
            <div className={styles.tableContainer}>
              <table className={styles.analysesTable}>
                <thead>
                  <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Data da Colheita</th>
                    <th scope="col">Tipo de Café</th>
                    <th scope="col">Quantidade</th>
                    <th scope="col">Decisão</th>
                  </tr>
                </thead>
                <tbody>
                  {tableAnalyses.map((analysis) => (
                    <tr key={analysis.id}>
                      <td className={styles.analysisName}>{analysis.id}</td>
                      <td>{analysis.date}</td>
                      <td>{analysis.coffeeType}</td>
                      <td>{analysis.quantity}</td>
                      <td>
                        <div className={
                          analysis.decision === "Vender Agora" ? styles.decisionSellNow :
                            analysis.decision === "Vender Parcialmente" ? styles.decisionSellPartially :
                              styles.decisionWait
                        }>
                          {analysis.decision}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;