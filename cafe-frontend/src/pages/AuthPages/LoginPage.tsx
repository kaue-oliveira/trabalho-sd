/**
 * Página de login de usuário
 * 
 * Autentica usuário no sistema via AuthContext
 * 
 * Integrações: AuthContext.login(), API /auth/login
 * Validações: email, senha
 */

import React, { useState } from 'react';
import Form from '../../Components/Form/Form';
import type { FormField } from '../../Components/Form/Form';
import Modal from '../../Components/Modal/Modal';
import styles from './AuthPages.module.css';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { loginValidations } from '../../utils/Validations';
import { useNotification } from '../../hooks/useNotification';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const { notification, showNotification, closeNotification } = useNotification();

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

  const handleSubmit = async (data: Record<string, string>) => {
    const validation = loginValidations.validateLogin(data.email, data.password);

    if (!validation.isValid) {
      showNotification('error', validation.message!);
      return;
    }

    setLoading(true);
    const result = await login(data.email, data.password);

    if (result.success) {
      showNotification('success', 'Login realizado com sucesso!');
      setTimeout(() => navigate('/painel-de-controle'), 1000);
    } else {
      showNotification('error', result.error || 'Erro ao fazer login');
    }
    setLoading(false);
  };

  return (
    <div className={styles.authPage}>
      <div className={styles.authContainer}>
        <div className={styles.authLayout}>
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

export default LoginPage;