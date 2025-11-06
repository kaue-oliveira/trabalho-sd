import Form from '../../Components/Form/Form';
import type { FormField } from '../../Components/Form/Form';
import styles from './AuthPages.module.css';
import { useNavigate } from 'react-router-dom';

const ChangePasswordPage: React.FC = () => {
  const navigate = useNavigate();

  const fields: FormField[] = [
    {
      name: 'newPassword',
      label: 'Nova senha',
      type: 'password',
      placeholder: '••••••••',
      icon: 'lock',
      showPasswordToggle: true,
    },
    {
      name: 'confirmPassword',
      label: 'Confirmar nova senha',
      type: 'password',
      placeholder: '••••••••',
      icon: 'lock_reset',
      showPasswordToggle: true,
    },
  ];

  const handleSubmit = (data: Record<string, string>) => {
    console.log('Senha alterada:', data);
    navigate('/login');
  };

  return (
    <div className={styles.authPage}>
      <div style={{ width: '100%', maxWidth: 960, padding: 16 }}>
        <div style={{ display: 'flex', gap: 32, alignItems: 'flex-start', justifyContent: 'center' }}>
          <div className={styles.loginWrapper}>
            <Form
              title="Alterar senha"
              subtitle="Digite sua nova senha abaixo."
              fields={fields}
              submitButtonText="Atualizar senha"
              onSubmit={handleSubmit}
              showLogo
              logoText="AgroAnalytics"
              logoIcon="eco"
              showBackButton
              backButtonHref="/login"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChangePasswordPage;
