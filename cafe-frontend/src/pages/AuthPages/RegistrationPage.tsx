import Form from '../../Components/Form/Form';
import type { FormField } from '../../Components/Form/Form';
import styles from './AuthPages.module.css';
import { useNavigate } from 'react-router-dom';

const RegistrationPage: React.FC = () => {
  const navigate = useNavigate();

  const fields: FormField[] = [
    { 
      name: 'fullName', 
      label: 'Nome Completo', 
      type: 'text', 
      placeholder: 'Seu nome completo', 
      icon: 'person' 
    },
    { 
      name: 'email', 
      label: 'E-mail', 
      type: 'email', 
      placeholder: 'seu@email.com', 
      icon: 'mail' 
    },
    { 
      name: 'password', 
      label: 'Senha', 
      type: 'password', 
      placeholder: '••••••••', 
      icon: 'lock', 
      showPasswordToggle: true,
      helperText: 'Use pelo menos 8 caracteres com letras e números'
    },
    { 
      name: 'confirmPassword', 
      label: 'Confirmar Senha', 
      type: 'password', 
      placeholder: '••••••••', 
      icon: 'lock', 
      showPasswordToggle: true 
    },
    { 
      name: 'accountType', 
      label: 'Tipo de Conta', 
      type: 'select', 
      placeholder: '', 
      icon: 'group',
      options: ['Produtor', 'Cooperativa'] 
    }
  ];

  const handleSubmit = async (data: Record<string, string>) => {
    console.log('Dados do cadastro:', data);
    // chama API de cadastro
    navigate('/login');
  };

  return (
    <div className={styles.authPage}>
      <div className={styles.registerContainer}>
        <div className={styles.registerHeader}>
          <svg className={styles.registerIcon} fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm3.32 12.35c-.17.38-.51.65-.92.65h-1.5c-.34 0-.65-.19-.8-.49l-.7-1.42c-.22-.43-.66-.7-1.13-.7-.47 0-.91.27-1.13.7l-.7 1.42c-.15.3-.46.49-.8.49H6.6c-.41 0-.75-.27-.92-.65-.17-.38-.07-.82.25-1.1l4.18-3.66c.32-.28.8-.28 1.12 0l4.18 3.66c.32.28.42.72.25 1.1zM11.5 8C10.67 8 10 7.33 10 6.5S10.67 5 11.5 5h1C13.33 5 14 5.67 14 6.5S13.33 8 12.5 8h-1z"></path>
          </svg>
          <h1 className={styles.registerTitle}>Criar sua conta</h1>
          <p className={styles.registerSubtitle}>
            Junte-se à nossa plataforma para começar com a análise agronômica.
          </p>
        </div>

        <Form
          title=""
          fields={fields}
          submitButtonText="Cadastrar"
          onSubmit={handleSubmit}
          footerText="Já tem uma conta?"
          footerLinkText="Fazer login"
          footerLinkHref="/login"
          showLogo={false}
        />
      </div>
    </div>
  );
};

export default RegistrationPage;