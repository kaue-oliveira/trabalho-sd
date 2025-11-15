import Form from '../../Components/Form/Form';
import type { FormField } from '../../Components/Form/Form';
import Modal from '../../Components/Modal/Modal';
import styles from './AuthPages.module.css';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { changePasswordValidations } from '../../utils/Validations';
import { useNotification } from '../../hooks/useNotification';

const ChangePasswordPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { notification, showNotification, closeNotification } = useNotification();

  const token = searchParams.get('token');

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

  const handleSubmit = async (data: Record<string, string>) => {
    if (!token) {
      showNotification('error', 'Link de redefinição inválido ou expirado. Solicite um novo link na página "Esqueci minha senha"');
      return;
    }

    const validation = changePasswordValidations.validateChangePassword(
      data.newPassword,
      data.confirmPassword
    );

    if (!validation.isValid) {
      showNotification('error', validation.message!);
      return;
    }

    try {
      const API_BASE = (import.meta as any).env?.VITE_API_URL || 'http://localhost:3000';
      const response = await fetch(`${API_BASE}/auth/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token: token,
          new_password: data.newPassword
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Erro ao redefinir senha' }));
        showNotification('error', errorData.detail || 'Erro ao alterar senha');
        return;
      }

      showNotification('success', 'Senha alterada com sucesso!');
      setTimeout(() => navigate('/login'), 1500);
    } catch (error) {
      showNotification('error', 'Erro ao alterar senha. Tente novamente.');
    }
  };

  return (
    <div className={styles.authPage}>
      <div className={styles.authContainer}>
        <div className={styles.authLayout}>
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
      <Modal
        isOpen={notification.isOpen}
        onClose={closeNotification}
        type={notification.type}
        message={notification.message}
        duration={notification.type === 'success' ? 3000 : 5000}
      />
    </div>
  );
};

export default ChangePasswordPage;