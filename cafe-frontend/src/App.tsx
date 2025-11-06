import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import PublicHome from './pages/PublicHome/PublicHome';
import LoginPage from './pages/AuthPages/LoginPage';
import RegistrationPage from './pages/AuthPages/RegistrationPage';
import ForgotPasswordPage from './pages/AuthPages/ForgotPasswordPage';
import ChangePasswordPage from './pages/AuthPages/ChangePasswordPage';
import Dashboard from './pages/Dashboard/Dashboard';
import NewAnalysis from './pages/NewAnalysis/NewAnalysis';
import HistoricAnalyses from './pages/HistoricAnalyses/HistoricAnalyses';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PublicHome />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/cadastrar" element={<RegistrationPage />} />
        <Route path='/esqueceu-senha' element={<ForgotPasswordPage />} />
        <Route path='/alterar-senha' element={<ChangePasswordPage />} />
        <Route path='/painel-de-controle' element={<Dashboard />} />
        <Route path='/nova-analise' element={<NewAnalysis />} />
        <Route path='/historico-analises' element={<HistoricAnalyses />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;