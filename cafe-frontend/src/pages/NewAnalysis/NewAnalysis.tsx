import React, { useState } from 'react';
import styles from './NewAnalysis.module.css';
import Sidebar from '../../Components/Sidebar/Sidebar';

const NewAnalysis: React.FC = () => {
  const [coffeeType, setCoffeeType] = useState('');
  const [variety, setVariety] = useState('');
  const [harvestDate, setHarvestDate] = useState('2024-10-05');
  const [location, setLocation] = useState('');
  const [stock, setStock] = useState('');
  const [quality, setQuality] = useState('');

  const handleAnalyze = () => {
    console.log('Analisando...', {
      coffeeType,
      variety,
      harvestDate,
      location,
      stock,
      quality
    });
    // lógica de análise
  };

  const handleSaveAnalysis = () => {
    console.log('Salvando análise...');
    // lógica de salvar
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
                  <div className={styles.row}>
                    <label className={styles.field}>
                      <p className={styles.label}>Tipo de Café</p>
                      <select 
                        className={styles.select}
                        value={coffeeType}
                        onChange={(e) => setCoffeeType(e.target.value)}
                      >
                        <option value="">Selecione o tipo de café</option>
                        <option value="Arabica">Arábica</option>
                        <option value="Robusta">Robusta</option>
                      </select>
                    </label>
                    
                    <label className={styles.field}>
                      <p className={styles.label}>Variedade</p>
                      <select 
                        className={styles.select}
                        value={variety}
                        onChange={(e) => setVariety(e.target.value)}
                      >
                        <option value="">Selecione a variedade</option>
                        <option value="Typica">Typica</option>
                        <option value="Bourbon">Bourbon</option>
                        <option value="Gesha">Gesha</option>
                      </select>
                    </label>
                  </div>

                  <label className={styles.field}>
                    <p className={styles.label}>Data da Colheita</p>
                    <div className={styles.inputWrapper}>
                      <input 
                        className={styles.input}
                        type="date" 
                        value={harvestDate}
                        onChange={(e) => setHarvestDate(e.target.value)}
                      />
                    </div>
                  </label>

                  <div className={styles.row}>
                    <label className={styles.field}>
                      <p className={styles.label}>Localização</p>
                      <input 
                        className={styles.input}
                        type="text"
                        placeholder="Ex: Minas Gerais, Brasil"
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                      />
                    </label>
                    
                    <label className={styles.stockField}>
                      <p className={styles.label}>Estoque (kg)</p>
                      <input 
                        className={styles.input}
                        type="number"
                        placeholder="Ex: 5000"
                        value={stock}
                        onChange={(e) => setStock(e.target.value)}
                      />
                    </label>
                  </div>

                  <label className={styles.field}>
                    <p className={styles.label}>Qualidade</p>
                    <select 
                      className={styles.select}
                      value={quality}
                      onChange={(e) => setQuality(e.target.value)}
                    >
                      <option value="">Selecione a qualidade</option>
                      <option value="Specialty Grade">Grau Especial</option>
                      <option value="Premium Grade">Grau Premium</option>
                      <option value="Commercial Grade">Grau Comercial</option>
                    </select>
                  </label>

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
                  <div className={styles.resultSection}>
                    <div className={styles.resultHeader}>
                      <span className={styles.resultBadge}>VENDER</span>
                    </div>
                    
                    <div className={styles.recommendation}>
                      <h3 className={styles.recommendationTitle}>Recomendação da IA</h3>
                      <p className={styles.recommendationText}>
                        Com base na alta dos preços de mercado para grãos Arábica e nas previsões
                        climáticas favoráveis que garantem estabilidade na oferta, vender agora é
                        recomendado para maximizar o lucro. É previsto um leve declínio no próximo
                        trimestre devido ao aumento de colheitas em regiões concorrentes.
                      </p>
                    </div>

                    <div className={styles.statsGrid}>
                      <div className={styles.statCard}>
                        <p className={styles.statLabel}>Preço de Mercado</p>
                        <p className={styles.statValue}>
                          R$ 4,50/kg <span className={styles.positiveChange}>(+2,3%)</span>
                        </p>
                      </div>
                      <div className={styles.statCard}>
                        <p className={styles.statLabel}>Previsão do Clima</p>
                        <p className={styles.statValue}>Favorável</p>
                      </div>
                    </div>

                    <div className={styles.chartSection}>
                      <h3 className={styles.chartTitle}>Tendência de Preços (30 dias)</h3>
                      <div className={styles.chartContainer}>
                        <img 
                          src="https://lh3.googleusercontent.com/aida-public/AB6AXuBFCjSEy5O5EXJAB99TcvRNqQ2QGgRy52OAJxPGhFgrJ7hUfZqkCRI_xcE7zWMsNfzotwiRqYnPplIDm1md1cyH7EPRl0AP6tdovAszkXt2WKbDfb4eW0h6GcopqO9jE_DjG5IVzMwxRKHUKzJhu5nRxbDNysOj1U1I9S7d11sWtuifajYj4bWUcnqCvEWEqwKJwLhvQ4tGmhEgS91KvxwSSP38OpMvhwSQL6AyzybZyY3b6s-LYjr5xw5KA71cE1R5KlOlWyTmiKI" 
                          alt="Gráfico de linha mostrando tendência de alta nos preços do café nos últimos 30 dias."
                          className={styles.chartImage}
                        />
                      </div>
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
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default NewAnalysis;
