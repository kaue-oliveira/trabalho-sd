import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import type { Usuario, AuthResponse } from '../types/auth.types';

// Adicionar: usar variável de ambiente VITE_API_URL com fallback
const API_BASE = (import.meta as any).env?.VITE_API_URL || 'http://localhost:3000';

interface AuthContextType {
  user: Usuario | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<AuthResponse>;
  logout: () => void;
  isAuthenticated: boolean;
  analisesUsuario: Array<{
    id: number;
    usuario_id: number;
    tipo_cafe: string;
    data_colheita: string;
    quantidade: number;
    cidade: string;
    estado: string;
    estado_cafe: 'verde' | 'torrado' | 'moído';
    data_analise: string;
    decisao: 'VENDER' | 'VENDER_PARCIALMENTE' | 'AGUARDAR';
    explicacao_decisao: string;
  }>;
  //função para adicionar uma análise ao estado global
  addAnalise: (analise: any) => void;
  updateUser: (user: Usuario) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<Usuario | null>(null);
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [analisesUsuario, setAnalisesUsuario] = useState<any[]>([]);

  // função para adicionar análise (coloca no topo da lista)
  const addAnalise = (analise: any) => {
    setAnalisesUsuario(prev => [analise, ...prev]);
  };

  // função para atualizar usuário (atualiza state e localStorage)
  const updateUser = (updated: Usuario) => {
    setUser(updated);
    localStorage.setItem('user', JSON.stringify(updated));
  };

  const login = async (email: string, password: string): Promise<AuthResponse> => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const errorData = await response.json();
        return { success: false, error: errorData.detail || "Erro na autenticação" };
      }

      const data = await response.json();
      const { access_token, user: userData } = data;

      setUser(userData);
      setToken(access_token);
      localStorage.setItem('authToken', access_token);
      localStorage.setItem('user', JSON.stringify(userData));

      // Buscar análises do usuário após login
      const analisesResponse = await fetch(`${API_BASE}/analises`, {
        headers: { 'Authorization': `Bearer ${access_token}` }
      });

      if (analisesResponse.ok) {
        const analisesData = await analisesResponse.json();
        setAnalisesUsuario(analisesData);
      }

      return { success: true, user: userData };
    } catch (error) {
      return { success: false, error: "Erro ao conectar com o servidor" };
    } finally {
      setLoading(false);
    }
  };


  const logout = async () => {
    try {
      if (token) {
        await fetch(`${API_BASE}/auth/logout`, {
          method: 'POST'
        });
      }
    } catch (error) {
      console.error('Erro no logout:', error);
    } finally {
      setAnalisesUsuario([]);
      setUser(null);
      setToken(null);
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
    }
  };

  useEffect(() => {
    const savedToken = localStorage.getItem('authToken');
    const savedUser = localStorage.getItem('user');

    if (savedToken && savedUser) {
      const validateToken = async () => {
        try {
          const response = await fetch(`${API_BASE}/auth/me`, {
            headers: { 'Authorization': `Bearer ${savedToken}` }
          });

          if (response.ok) {
            const userData = JSON.parse(savedUser);
            setUser(userData);
            setToken(savedToken);

            const analisesResponse = await fetch(`${API_BASE}/analises`, {
              headers: { 'Authorization': `Bearer ${savedToken}` }
            });

            if (analisesResponse.ok) {
              const analisesData = await analisesResponse.json();
              setAnalisesUsuario(analisesData);
            }
          } else {
            localStorage.removeItem('authToken');
            localStorage.removeItem('user');
          }
        } catch (error) {
          localStorage.removeItem('authToken');
          localStorage.removeItem('user');
        }
      };

      validateToken();
    }
  }, []);

  const value: AuthContextType = {
    user,
    token,
    loading,
    login,
    logout,
    isAuthenticated: !!user && !!token,
    analisesUsuario,
    addAnalise, // exposto para uso em componentes (ex: NewAnalysis)
    updateUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};