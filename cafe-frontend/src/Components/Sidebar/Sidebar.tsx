import React from 'react';
import styles from './Sidebar.module.css';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Sidebar: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  
  const userName = user?.nome || "Usuário";
  const userInitial = userName.charAt(0).toUpperCase();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <aside className={styles.sidebar}>
      <div className={styles.sidebarContent}>
        {/* ===== Logo ===== */}
        <div className={styles.logoSection}>
          <div className={styles.logoIcon}>
            <svg fill="currentColor" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <path d="M44 11.2727C44 14.0109 39.8386 16.3957 33.69 17.6364C39.8386 18.877 44 21.2618 44 24C44 26.7382 39.8386 29.123 33.69 30.3636C39.8386 31.6043 44 33.9891 44 36.7273C44 40.7439 35.0457 44 24 44C12.9543 44 4 40.7439 4 36.7273C4 33.9891 8.16144 31.6043 14.31 30.3636C8.16144 29.123 4 26.7382 4 24C4 21.2618 8.16144 18.877 14.31 17.6364C8.16144 16.3957 4 14.0109 4 11.2727C4 7.25611 12.9543 4 24 4C35.0457 4 44 7.25611 44 11.2727Z"></path>
            </svg>
          </div>
          <div className={styles.logoText}>
            <h1 className={styles.companyName}>AgroAnalytics</h1>
            <p className={styles.companyDescription}>Café System</p>
          </div>
        </div>

        {/* ===== Navegação ===== */}
        <nav className={styles.navigation}>
          <Link
            to="/painel-de-controle"
            className={`${styles.navLink} ${
              location.pathname.includes('/painel-de-controle') ? styles.active : ''
            }`}
          >
            <i className={`${styles.materialIcon} ${styles.icon}`}>dashboard</i>
            <p className={styles.navText}>Painel de Controle</p>
          </Link>

          <Link
            to="/nova-analise"
            className={`${styles.navLink} ${
              location.pathname.includes('/nova-analise') ? styles.active : ''
            }`}
          >
            <i className={`${styles.materialIcon} ${styles.icon}`}>science</i>
            <p className={styles.navText}>Nova Análise</p>
          </Link>

          <Link
            to="/historico-analises"
            className={`${styles.navLink} ${
              location.pathname.includes('/historico-analises') ? styles.active : ''
            }`}
          >
            <i className={`${styles.materialIcon} ${styles.icon}`}>history</i>
            <p className={styles.navText}>Histórico</p>
          </Link>
        </nav>
      </div>

      {/* ===== Rodapé (Perfil) ===== */}
      <div className={styles.sidebarFooter}>
        <Link
            to="/perfil"
            className={`${styles.profileContainer} ${
              location.pathname.includes('/perfil') ? styles.active : ''
            }`}
          >
          <div className={styles.avatarCircle}>{userInitial}</div>
          <p className={styles.profileName}>{userName}</p>
        </Link>

        <button onClick={handleLogout} className={styles.navLink} >
          <i className={`${styles.materialIcon} ${styles.icon}`}>logout</i>
          <p className={styles.navText}>Sair</p>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;