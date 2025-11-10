import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext'; // 🚨 useAuth também
import PublicHome from './pages/PublicHome/PublicHome';
import LoginPage from './pages/AuthPages/LoginPage';
import RegistrationPage from './pages/AuthPages/RegistrationPage';
import ForgotPasswordPage from './pages/AuthPages/ForgotPasswordPage';
import ChangePasswordPage from './pages/AuthPages/ChangePasswordPage';
import Dashboard from './pages/Dashboard/Dashboard';
import NewAnalysis from './pages/NewAnalysis/NewAnalysis';
import HistoricAnalyses from './pages/HistoricAnalyses/HistoricAnalyses';
import Profile from './pages/Profile/Profile';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div>Carregando...</div>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/*Rota pública*/}
          <Route path="/" element={<PublicHome />} />
          
          {/*Rotas de auth*/}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/cadastrar" element={<RegistrationPage />} />
          <Route path='/esqueceu-senha' element={<ForgotPasswordPage />} />
          <Route path='/alterar-senha' element={<ChangePasswordPage />} />
          
          {/*Rotas protegidas - verificam autenticação */}
          <Route path='/painel-de-controle' element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
          <Route path='/nova-analise' element={
            <ProtectedRoute>
              <NewAnalysis />
            </ProtectedRoute>
          } />
          <Route path='/historico-analises' element={
            <ProtectedRoute>
              <HistoricAnalyses />
            </ProtectedRoute>
          } />
          <Route path='/perfil' element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          } />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;