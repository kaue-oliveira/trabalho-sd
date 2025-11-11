import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../../Components/Sidebar/Sidebar';
import Modal from '../../Components/Modal/Modal';
import { useAuth } from '../../context/AuthContext';
import { profileValidations } from '../../utils/Validations';
import { useNotification } from '../../hooks/useNotification';
import styles from './Profile.module.css';

const Profile: React.FC = () => {
    const navigate = useNavigate();
    const { user, logout } = useAuth();
    const { notification, showNotification, closeNotification } = useNotification();
    const [showDeleteModal, setShowDeleteModal] = useState(false);

    const userName = user?.nome || "Usuário";
    const userEmail = user?.email || "email@exemplo.com";
    const userInitial = userName.charAt(0).toUpperCase();
    const accountType = user?.tipo_conta === "PRODUTOR" ? "Produtor" : "Cooperativa";

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
        const validation = profileValidations.validateProfile(formData);
        
        if (!validation.isValid) {
            showNotification('error', validation.message!);
            return;
        }

        // Verificar se houve mudanças reais
        const hasChanges =
            formData.fullName !== userName ||
            formData.email !== userEmail ||
            formData.accountType !== accountType ||
            formData.newPassword !== '';

        if (!hasChanges) {
            showNotification('info', 'Nenhuma alteração foi feita.');
            return;
        }

        console.log('Dados do perfil salvos:', formData);
        showNotification('success', 'Perfil atualizado com sucesso!');

        // =====================================================
        // **TROCAR AQUI QUANDO GATEWAY ESTIVER PRONTO**
        // =====================================================
        // const updateData = {
        //   nome: formData.fullName,
        //   email: formData.email,
        //   senha: formData.newPassword || undefined,
        //   tipo_conta: formData.accountType.toUpperCase()
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
    };

    const handleDeleteAccount = () => {
        setShowDeleteModal(true);
    };

    const confirmDeleteAccount = () => {
        setShowDeleteModal(false);
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
    };

    const cancelDeleteAccount = () => {
        setShowDeleteModal(false);
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

                    {showDeleteModal && (
                        <div className={styles.modalOverlay}>
                            <div className={styles.deleteModal}>
                                <div className={styles.modalHeader}>
                                    <i className={`${styles.materialIcon} ${styles.warningIcon}`}>warning</i>
                                    <h3 className={styles.modalTitle}>Excluir Conta</h3>
                                </div>
                                
                                <div className={styles.modalContent}>
                                    <p className={styles.modalText}>
                                        Tem certeza que deseja excluir sua conta? 
                                        <strong> Todos os seus dados e análises serão perdidos permanentemente.</strong>
                                    </p>
                                    <p className={styles.modalWarning}>
                                        Esta ação não pode ser desfeita.
                                    </p>
                                </div>

                                <div className={styles.modalActions}>
                                    <button
                                        className={styles.modalCancel}
                                        onClick={cancelDeleteAccount}
                                    >
                                        Cancelar
                                    </button>
                                    <button
                                        className={styles.modalConfirm}
                                        onClick={confirmDeleteAccount}
                                    >
                                        Sim, Excluir Conta
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}

                    <Modal
                        isOpen={notification.isOpen}
                        onClose={closeNotification}
                        type={notification.type}
                        message={notification.message}
                        duration={notification.type === 'success' ? 3000 : 4000}
                    />
                </div>
            </main>
        </div>
    );
};

export default Profile;