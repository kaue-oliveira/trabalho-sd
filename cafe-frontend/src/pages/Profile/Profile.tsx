import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../../Components/Sidebar/Sidebar';
import { useAuth } from '../../context/AuthContext';
import styles from './Profile.module.css';

const Profile: React.FC = () => {
    const navigate = useNavigate();
    const { user, logout } = useAuth();
    
    const userName = user?.nome || "Usuário";
    const userEmail = user?.email || "email@exemplo.com";
    const userInitial = userName.charAt(0).toUpperCase();
    const accountType = user?.tipo_conta === "PRODUTOR" ? "Produtor" : "Cooperativa";

    const [showSuccess, setShowSuccess] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const [formData, setFormData] = useState({
        fullName: userName,
        email: userEmail,
        newPassword: '',
        confirmPassword: '',
        accountType: accountType
    });

    const handleChange = (field: string, value: string) => {
        setFormData({ ...formData, [field]: value });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        
        if (formData.newPassword && formData.newPassword !== formData.confirmPassword) {
            alert("As senhas não coincidem!");
            return;
        }
        
        console.log('Dados do perfil salvos:', formData);
        
        // =====================================================
        // **TROCAR AQUI QUANDO GATEWAY ESTIVER PRONTO**
        // =====================================================
        // const updateData = {
        //   nome: formData.fullName,
        //   email: formData.email,
        //   senha: formData.newPassword || undefined,
        //   tipo_conta: formData.accountType.toUpperCase() // ✅ **ENVIAR TIPO DE CONTA**
        // };
        // 
        // const response = await fetch('http://localhost:3000/usuarios/me', {
        //   method: 'PUT',
        //   headers: {
        //     'Authorization': `Bearer ${token}`,
        //     'Content-Type': 'application/json'
        //   },
        //   body: JSON.stringify(updateData)
        // });
        // =====================================================
        
        // **CÓDIGO MOCKADO - MANTER POR ENQUANTO**
        setShowSuccess(true);
        setTimeout(() => setShowSuccess(false), 3000);
    };

    const handleDeleteAccount = () => {
        if (window.confirm('Tem certeza que deseja excluir sua conta? Esta ação não pode ser desfeita.')) {
            // =====================================================
            // **TROCAR AQUI QUANDO GATEWAY ESTIVER PRONTO**
            // =====================================================
            // const response = await fetch('http://localhost:3000/usuarios/me', {
            //   method: 'DELETE',
            //   headers: {
            //     'Authorization': `Bearer ${token}`
            //   }
            // });
            // =====================================================
            
            console.log('Conta excluída');
            logout();
            navigate('/');
        }
    };

    const handleCancel = () => {
        console.log('Alterações canceladas');
        navigate(-1);
    };

    return (
        <div className={styles.container}>
            <Sidebar />

            <main className={styles.mainContent}>
                <div className={styles.contentContainer}>
                    <div className={styles.pageHeader}>
                        <h1 className={styles.title}>Meu Perfil</h1>
                    </div>

                    <div className={styles.profileCard}>
                        <div className={styles.profileHeader}>
                            <div className={styles.avatarSection}>
                                <div className={styles.avatarCircle}>
                                    {userInitial}
                                </div>
                                <div className={styles.profileInfo}>
                                    <h2 className={styles.userName}>{userName}</h2>
                                    <p className={styles.userEmail}>{userEmail}</p>
                                    <div className={styles.userBadge}>
                                        {accountType}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className={styles.formSection}>
                            <form onSubmit={handleSubmit}>

                                <label className={styles.inputLabel}>
                                    <p className={styles.labelText}>Nome Completo</p>
                                    <div className={styles.inputWrapper}>
                                        <i className={`${styles.materialIcon} ${styles.iconLeft}`}>person</i>
                                        <input
                                            className={styles.input}
                                            type="text"
                                            placeholder="Digite seu nome completo"
                                            value={formData.fullName}
                                            onChange={(e) => handleChange('fullName', e.target.value)}
                                        />
                                    </div>
                                </label>

                                <label className={styles.inputLabel}>
                                    <p className={styles.labelText}>Endereço de Email</p>
                                    <div className={styles.inputWrapper}>
                                        <i className={`${styles.materialIcon} ${styles.iconLeft}`}>email</i>
                                        <input
                                            className={styles.input}
                                            type="email"
                                            placeholder="Digite seu email"
                                            value={formData.email}
                                            onChange={(e) => handleChange('email', e.target.value)}
                                        />
                                    </div>
                                </label>

                                <div className={styles.formGrid}>
                                    <label className={styles.inputLabel}>
                                        <p className={styles.labelText}>Nova Senha</p>
                                        <div className={styles.inputWrapper}>
                                            <i className={`${styles.materialIcon} ${styles.iconLeft}`}>lock</i>
                                            <input
                                                className={styles.input}
                                                type={showPassword ? 'text' : 'password'}
                                                placeholder="Digite sua nova senha"
                                                value={formData.newPassword}
                                                onChange={(e) => handleChange('newPassword', e.target.value)}
                                            />
                                            <button
                                                type="button"
                                                className={styles.togglePassword}
                                                onClick={() => setShowPassword(!showPassword)}
                                                aria-label="Alternar visibilidade da senha"
                                            >
                                                <i className={styles.materialIcon}>
                                                    {showPassword ? 'visibility' : 'visibility_off'}
                                                </i>
                                            </button>
                                        </div>
                                        {formData.newPassword && (
                                            <p className={styles.passwordHint}>
                                                Deixe em branco para manter a senha atual
                                            </p>
                                        )}
                                    </label>

                                    <label className={styles.inputLabel}>
                                        <p className={styles.labelText}>Confirme sua Nova Senha</p>
                                        <div className={styles.inputWrapper}>
                                            <i className={`${styles.materialIcon} ${styles.iconLeft}`}>lock</i>
                                            <input
                                                className={styles.input}
                                                type={showConfirmPassword ? 'text' : 'password'}
                                                placeholder="Confirme sua nova senha"
                                                value={formData.confirmPassword}
                                                onChange={(e) => handleChange('confirmPassword', e.target.value)}
                                            />
                                            <button
                                                type="button"
                                                className={styles.togglePassword}
                                                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                                aria-label="Alternar visibilidade da senha de confirmação"
                                            >
                                                <i className={styles.materialIcon}>
                                                    {showConfirmPassword ? 'visibility' : 'visibility_off'}
                                                </i>
                                            </button>
                                        </div>
                                        {formData.newPassword !== formData.confirmPassword && formData.confirmPassword && (
                                            <p className={styles.passwordError}>As senhas não coincidem</p>
                                        )}
                                    </label>
                                </div>

                                <label className={styles.inputLabel}>
                                    <p className={styles.labelText}>Tipo de Conta</p>
                                    <div className={styles.inputWrapper}>
                                        <i className={`${styles.materialIcon} ${styles.iconLeft}`}>badge</i>
                                        <select
                                            className={styles.select}
                                            value={formData.accountType}
                                            onChange={(e) => handleChange('accountType', e.target.value)}
                                        >
                                            <option value="Produtor">Produtor</option>
                                            <option value="Cooperativa">Cooperativa</option>
                                        </select>
                                        <i className={`${styles.materialIcon} ${styles.iconRight}`}>expand_more</i>
                                    </div>
                                </label>

                                <div className={styles.actionButtons}>
                                    <button
                                        className={styles.deleteButton}
                                        onClick={handleDeleteAccount}
                                        type="button"
                                    >
                                        <i className={styles.materialIcon}>delete</i>
                                        Excluir Conta
                                    </button>

                                    <div className={styles.formActions}>
                                        <button
                                            className={styles.cancelButton}
                                            onClick={handleCancel}
                                            type="button"
                                        >
                                            Cancelar
                                        </button>
                                        <button
                                            className={styles.saveButton}
                                            type="submit"
                                        >
                                            Salvar Alterações
                                        </button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>

                    {showSuccess && (
                        <div className={styles.successNotification}>
                            <i className={`${styles.materialIcon} ${styles.successIcon}`}>check_circle</i>
                            <p className={styles.successText}>Perfil atualizado com sucesso!</p>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
};

export default Profile;