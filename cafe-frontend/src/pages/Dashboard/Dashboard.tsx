import React, { useState, useRef } from 'react';
import styles from './Dashboard.module.css';
import { Link, useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const profileMenuRef = useRef<HTMLDivElement>(null);
  const userName = "Gabriel";
  const userInitial = userName.charAt(0).toUpperCase();
  const navigate = useNavigate();

  const toggleProfileMenu = () => {
    setIsProfileMenuOpen(!isProfileMenuOpen);
  };

  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target as Node)) {
        setIsProfileMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // ====== AÇÕES ======
  const handleLogout = () => {
    console.log("Logout realizado");
    navigate('/');
  };

  const handleProfile = () => {
    console.log("Acessar perfil");
    navigate('/perfil');
  };

  const handleAnalyses = () => {
    console.log("Acessar minhas análises");
    navigate('/historico-analises');
  };

  const handleNewAnalysis = () => {
    console.log("Nova análise iniciada");
    navigate('/nova-analise');
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
      <div className={styles.layoutContainer}>
        <header className={styles.header}>
          <div className={styles.logoSection}>
            <div className={styles.logoIcon}>
              <svg fill="currentColor" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <path d="M44 11.2727C44 14.0109 39.8386 16.3957 33.69 17.6364C39.8386 18.877 44 21.2618 44 24C44 26.7382 39.8386 29.123 33.69 30.3636C39.8386 31.6043 44 33.9891 44 36.7273C44 40.7439 35.0457 44 24 44C12.9543 44 4 40.7439 4 36.7273C4 33.9891 8.16144 31.6043 14.31 30.3636C8.16144 29.123 4 26.7382 4 24C4 21.2618 8.16144 18.877 14.31 17.6364C8.16144 16.3957 4 14.0109 4 11.2727C4 7.25611 12.9543 4 24 4C35.0457 4 44 7.25611 44 11.2727Z"></path>
              </svg>
            </div>
            <h2 className={styles.logoText}>AgroAnalytics Café</h2>
          </div>

          <nav className={styles.nav}>
            <div className={styles.navLinkActive}>Painel de Controle</div>
            <Link className={styles.navLink} to="/historico-analises">Análises</Link>
          </nav>

          <div className={styles.userSection} ref={profileMenuRef}>
            <div className={styles.profileContainer}>
              <button
                className={styles.avatarButton}
                onClick={toggleProfileMenu}
              >
                <i className={styles.avatarInitial}>{userInitial}</i>
              </button>

              {isProfileMenuOpen && (
                <div className={styles.profileMenu}>
                  <button className={styles.menuItem} onClick={handleProfile}>
                    <i className={styles.materialIcon}>person</i>
                    Meu Perfil
                  </button>
                  <button className={styles.menuItem} onClick={handleAnalyses}>
                    <i className={styles.materialIcon}>analytics</i>
                    Minhas Análises
                  </button>
                  <div className={styles.menuDivider}></div>
                  <button className={styles.menuItem} onClick={handleLogout}  >
                    <i className={styles.materialIcon}>logout</i>
                    Sair
                  </button>
                </div>
              )}
            </div>
          </div>
        </header>

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
              <Link className={styles.viewAllLink} to="historico-analises">Ver Todas</Link>
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