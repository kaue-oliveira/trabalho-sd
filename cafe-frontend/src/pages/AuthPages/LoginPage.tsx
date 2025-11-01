import React, { useState } from 'react';
import Form from '../../Components/Form/Form';
import type { FormField } from '../../Components/Form/Form';
import styles from './AuthPages.module.css';
import { useNavigate, Link } from 'react-router-dom';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const fields: FormField[] = [
    { 
      name: 'email', 
      label: 'E-mail', 
      type: 'email', 
      placeholder: 'seu@email.com', 
      icon: 'email' 
    },
    { 
      name: 'password', 
      label: 'Senha', 
      type: 'password', 
      placeholder: '••••••••', 
      icon: 'lock', 
      showPasswordToggle: true,
      helperText: (
        <div className={styles.forgotPasswordContainer}>
          <Link to="/esqueceu-senha" className={styles.forgotPasswordLink}>
            Esqueceu sua senha?
          </Link>
        </div>
      )
    }
  ];

  const handleSubmit = async (data: Record<string,string>) => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      console.log("Login realizado:", data);
      navigate('/dashboard');
    }, 1000);
  };

  return (
    <div className={styles.authPage}>
      <div style={{ width: '100%', maxWidth: 960, padding: 16 }}>
        <div style={{ display: 'flex', gap: 32, alignItems: 'flex-start', justifyContent: 'center' }}>
          <div className={styles.loginWrapper}>
            <Form
              title="Entre na sua conta"
              subtitle="Bem-vindo de volta! Insira seus dados."
              fields={fields}
              submitButtonText={loading ? 'Entrando...' : 'Entrar'}
              onSubmit={handleSubmit}
              footerText="Não tem conta?"
              footerLinkText="Criar conta"
              footerLinkHref="/cadastrar"
              showLogo
              logoText="AgroAnalytics"
              logoIcon="eco"
              showBackButton
              backButtonHref="/"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;