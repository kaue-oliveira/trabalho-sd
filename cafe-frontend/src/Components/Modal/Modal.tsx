import React from 'react';
import styles from './Modal.module.css';

interface ModalProps {
    isOpen: boolean;
    onClose: () => void;
    type: 'success' | 'error' | 'info';
    message: string;
    duration?: number;
}

const Modal: React.FC<ModalProps> = ({
    isOpen,
    onClose,
    type,
    message,
    duration = 3000
}) => {
    React.useEffect(() => {
        if (isOpen && duration > 0) {
            const timer = setTimeout(onClose, duration);
            return () => clearTimeout(timer);
        }
    }, [isOpen, duration, onClose]);

    if (!isOpen) return null;

    return (
        <div className={`${styles.notification} ${styles[type]}`}>
            <div className={styles.notificationContent}>
                <i className={`${styles.materialIcon} ${styles.icon}`}>
                    {type === 'success' ? 'check_circle' :
                        type === 'error' ? 'error' :
                            'info'}
                </i>
                <span className={styles.message}>{message}</span>
            </div>
            <button
                className={styles.closeButton}
                onClick={onClose}
                aria-label="Fechar notificação"
            >
                <i className={styles.materialIcon}>close</i>
            </button>
        </div>
    );
};

export default Modal;