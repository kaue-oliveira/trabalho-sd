import Form from '../../Components/Form/Form';
import type { FormField } from '../../Components/Form/Form';
import Modal from '../../Components/Modal/Modal';
import styles from './AuthPages.module.css';
import { useNavigate } from 'react-router-dom';
import { forgotPasswordValidations } from '../../utils/Validations';
import { useNotification } from '../../hooks/useNotification';

const ForgotPasswordPage: React.FC = () => {
  const navigate = useNavigate();
  const { notification, showNotification, closeNotification } = useNotification();

  const fields: FormField[] = [
    {
      name: 'email',
      label: 'E-mail',
      type: 'email',
      placeholder: 'seu@email.com',
      icon: 'email',
    },
  ];

  const handleSubmit = async (data: Record<string, string>) => {
    const validation = forgotPasswordValidations.validateForgotPassword(data.email);

    if (!validation.isValid) {
      showNotification('error', validation.message!);
      return;
    }

    try {
      console.log('Solicitação de redefinição enviada:', data);

      // =====================================================
      // **TROCAR AQUI QUANDO GATEWAY ESTIVER PRONTO**
      // =====================================================

      showNotification('success', 'Email de redefinição enviado com sucesso!');
      setTimeout(() => navigate('/login'), 2000);
    } catch (error) {
      showNotification('error', 'Erro ao enviar email. Tente novamente.');
    }
  };

  return (
    <div className={styles.authPage}>
      <div className={styles.authContainer}>
        <div className={styles.authLayout}>
          <div className={styles.loginWrapper}>
            <Form
              title="Esqueceu sua senha?"
              subtitle="Digite seu e-mail cadastrado e enviaremos um link para redefinir sua senha."
              fields={fields}
              submitButtonText="Enviar link de redefinição"
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
        duration={notification.type === 'success' ? 3000 : 4000}
      />
    </div>
  );
};

export default ForgotPasswordPage;
