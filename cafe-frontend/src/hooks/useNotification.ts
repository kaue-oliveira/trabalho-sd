import { useState } from 'react';

export const useNotification = () => {
  const [notification, setNotification] = useState<{
    isOpen: boolean;
    type: 'success' | 'error' | 'info';
    message: string;
  }>({
    isOpen: false,
    type: 'success',
    message: ''
  });

  const showNotification = (type: 'success' | 'error' | 'info', message: string) => {
    setNotification({
      isOpen: true,
      type,
      message
    });
  };

  const closeNotification = () => {
    setNotification(prev => ({ ...prev, isOpen: false }));
  };

  return {
    notification,
    showNotification,
    closeNotification
  };
};