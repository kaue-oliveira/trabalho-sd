import Form from '../../Components/Form/Form';
import type { FormField } from '../../Components/Form/Form';
import styles from './AuthPages.module.css';
import { useNavigate} from 'react-router-dom';

const ForgotPasswordPage: React.FC = () => {
  const navigate = useNavigate();

  const fields: FormField[] = [
    {
      name: 'email',
      label: 'E-mail',
      type: 'email',
      placeholder: 'seu@email.com',
      icon: 'email',
    },
  ];

  const handleSubmit = (data: Record<string, string>) => {
    console.log('Solicitação de redefinição enviada:', data);
    navigate('/login');
  };

  return (
    <div className={styles.authPage}>
      <div style={{ width: '100%', maxWidth: 960, padding: 16 }}>
        <div style={{ display: 'flex', gap: 32, alignItems: 'flex-start', justifyContent: 'center' }}>
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
    </div>
  );
};

export default ForgotPasswordPage;
