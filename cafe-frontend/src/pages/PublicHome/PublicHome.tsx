/**
 * Página pública inicial
 * 
 * Landing page com features e call-to-action
 * 
 * Navegação: login, cadastro
 * Conteúdo: hero section, features, footer
 */

import React from 'react';
import styles from './PublicHome.module.css';
import { Link, useNavigate } from 'react-router-dom';

const PublicHome: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.root}>
      <div className={styles.layoutContainer}>
        <div className={styles.contentWrapper}>
          <div className={styles.layoutContent}>
       
            <header className={styles.header}>
              <div className={styles.logo}>
                <div className={styles.logoIcon}>
                  <svg fill="currentColor" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                    <path d="M44 11.2727C44 14.0109 39.8386 16.3957 33.69 17.6364C39.8386 18.877 44 21.2618 44 24C44 26.7382 39.8386 29.123 33.69 30.3636C39.8386 31.6043 44 33.9891 44 36.7273C44 40.7439 35.0457 44 24 44C12.9543 44 4 40.7439 4 36.7273C4 33.9891 8.16144 31.6043 14.31 30.3636C8.16144 29.123 4 26.7382 4 24C4 21.2618 8.16144 18.877 14.31 17.6364C8.16144 16.3957 4 14.0109 4 11.2727C4 7.25611 12.9543 4 24 4C35.0457 4 44 7.25611 44 11.2727Z"></path>
                  </svg>
                </div>
                <h2 className={styles.logoText}>AgroAnalytics</h2>
              </div>
              <div className={styles.headerActions}>
                <button className={styles.btnPrimary} onClick={() => navigate('/cadastrar')}>
                  Cadastrar
                </button>
                <button className={styles.btnSecondary} onClick={() => navigate('/login')}>
                  Entrar
                </button>
              </div>
            </header>

            <main>
              <div className={styles.heroContainer}>
                <div className={styles.heroPadding}>
                  <div className={styles.hero}>
                    <div className={styles.heroContent}>
                      <h1 className={styles.heroTitle}>
                        Decida o Melhor Momento para Vender Sua Safra
                      </h1>
                      <p className={styles.heroDescription}>
                        Sistema inteligente que integra dados climáticos, de mercado e agronômicos para apoiar sua decisão de venda de café.
                      </p>
                    </div>
                    <div className={styles.heroActions}>
                      <button className={styles.btnHeroPrimary} onClick={() => navigate('/cadastrar')}>
                        Começar Agora
                      </button>
                      <button className={styles.btnHeroSecondary} onClick={() => navigate('/login')}>
                        Entrar
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <section className={styles.featuresSection}>
                <h2 className={styles.sectionTitle}>Como Funciona</h2>
                <div className={styles.featuresGrid}>
                  <div className={styles.featureCard}>
                    <div className={styles.featureIcon}>
                      <i className={styles.materialIcon}>cloud</i>
                    </div>
                    <div className={styles.featureContent}>
                      <h3 className={styles.featureTitle}>Dados Climáticos</h3>
                      <p className={styles.featureDescription}>
                        Coletamos e analisamos dados meteorológicos em tempo real para avaliar o impacto no seu café.
                      </p>
                    </div>
                  </div>

                  <div className={styles.featureCard}>
                    <div className={styles.featureIcon}>
                      <i className={styles.materialIcon}>show_chart</i>
                    </div>
                    <div className={styles.featureContent}>
                      <h3 className={styles.featureTitle}>Análise de Mercado</h3>
                      <p className={styles.featureDescription}>
                        Monitoramos preços e tendências do mercado de café para identificar as melhores oportunidades de venda.
                      </p>
                    </div>
                  </div>

                  <div className={styles.featureCard}>
                    <div className={styles.featureIcon}>
                      <i className={styles.materialIcon}>insights</i>
                    </div>
                    <div className={styles.featureContent}>
                      <h3 className={styles.featureTitle}>Decisão Inteligente</h3>
                      <p className={styles.featureDescription}>
                        Agentes inteligentes processam múltiplas variáveis e fornecem recomendações explicáveis sobre o timing ideal de venda.
                      </p>
                    </div>
                  </div>
                </div>
              </section>
            </main>

            <footer className={styles.footer}>
              <nav className={styles.footerLinks}>
                <Link to="/nova-analise" className={styles.footerLink}>Nova Análise</Link>
                <Link to="/historico-analises" className={styles.footerLink}>Histório de Análises</Link>
                <Link to="/perfil" className={styles.footerLink}>Perfil</Link>
                <Link to="/login" className={styles.footerLink}>Login</Link>
                <Link to="/cadastrar" className={styles.footerLink}>Cadastrar</Link>
              </nav>
              <p className={styles.copyright}>© 2025 AgroAnalytics. Sistema de Apoio à Decisão para Cafeicultura.</p>
            </footer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PublicHome;