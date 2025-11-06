import styles from './Dashboard.module.css';
import { Link, useNavigate } from 'react-router-dom';
import Sidebar from '../../Components/Sidebar/Sidebar';

const Dashboard: React.FC = () => {
  const userName = "Gabriel";
  const navigate = useNavigate();

  const handleNewAnalysis = () => {
    console.log("Nova análise iniciada");
    navigate('/nova-analise');
  };

  const handleAnalyses = () => {
    console.log("Acessar minhas análises");
    navigate('/historico-analises');
  };

  const recentAnalyses = [
    { id: "AN-004", date: "28/10/2024", coffeeType: "Arábica", quantity: "120 sacas", decision: "Vender Agora" },
    { id: "AN-003", date: "26/10/2024", coffeeType: "Arábica", quantity: "200 sacas", decision: "Aguardar" },
    { id: "AN-002", date: "24/10/2024", coffeeType: "Robusta", quantity: "80 sacas", decision: "Vender Parcialmente" },
    { id: "AN-001", date: "22/10/2024", coffeeType: "Arábica", quantity: "150 sacas", decision: "Vender Agora" }
  ];

  const sortedAnalyses = [...recentAnalyses].sort((a, b) => {
    const idA = parseInt(a.id.split('-')[1]);
    const idB = parseInt(b.id.split('-')[1]);
    return idB - idA;
  });

  const sellNowCount = recentAnalyses.filter(a => a.decision === "Vender Agora").length;
  const sellPartiallyCount = recentAnalyses.filter(a => a.decision === "Vender Parcialmente").length;
  const waitCount = recentAnalyses.filter(a => a.decision === "Aguardar").length;

  return (
    <div className={styles.dashboard}>
      <Sidebar userName={userName} />
  
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
                <p className={styles.statValue}>{recentAnalyses.length}</p>
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
                  {sortedAnalyses.map((analysis) => (
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