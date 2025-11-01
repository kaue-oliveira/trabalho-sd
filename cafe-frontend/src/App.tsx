import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import PublicHome from './pages/PublicHome/PublicHome';
import LoginPage from './pages/AuthPages/LoginPage';
import RegistrationPage from './pages/AuthPages/RegistrationPage';
import ForgotPasswordPage from './pages/AuthPages/ForgotPasswordPage';
import ChangePasswordPage from './pages/AuthPages/ChangePasswordPage';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PublicHome />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/cadastrar" element={<RegistrationPage />} />
        <Route path='/esqueceu-senha' element={<ForgotPasswordPage />} />
        <Route path='/alterar-senha' element={<ChangePasswordPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;