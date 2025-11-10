import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import type { Usuario, AuthResponse } from '../types/auth.types';

// =====================================================
// **REMOVER QUANDO GATEWAY ESTIVER PRONTO**
// =====================================================
// Dados mockados - apenas para desenvolvimento
const MOCK_USUARIOS: Usuario[] = [
  {
    id: 1,
    nome: "João Silva",
    email: "joao.produtor@email.com",
    tipo_conta: "PRODUTOR"
  },
  {
    id: 2, 
    nome: "Cooperativa Café Mineiro", 
    email: "coop.mineira@email.com",
    tipo_conta: "COOPERATIVA"
  }
];
// =====================================================

const MOCK_ANALISES = [
  // Análises do João Silva (PRODUTOR) - 6 análises
  {
    id: 1,
    usuario_id: 1,
    tipo_cafe: "Arábica",
    data_colheita: "2024-05-15",
    quantidade: 1500.50,
    cidade: "Varginha", 
    estado: "MG",
    estado_cafe: "verde" as const,
    data_analise: "2024-06-01",
    decisao: "VENDER" as const,
    explicacao_decisao: "Preço atual favorável para café Arábica de alta qualidade. Clima úmido pode afetar estoque se aguardar. Recomenda-se venda total nos próximos 14 dias."
  },
  {
    id: 2,
    usuario_id: 1,
    tipo_cafe: "Bourbon", 
    data_colheita: "2024-04-20",
    quantidade: 800.75,
    cidade: "Varginha",
    estado: "MG",
    estado_cafe: "verde" as const,
    data_analise: "2024-05-10",
    decisao: "VENDER_PARCIALMENTE" as const,
    explicacao_decisao: "Café Bourbon com nota excelente (86), mas preço pode subir com chegada do inverno. Vender 60% agora e aguardar valorização do restante."
  },
  {
    id: 3,
    usuario_id: 1,
    tipo_cafe: "Catuaí",
    data_colheita: "2024-03-10",
    quantidade: 1200.00,
    cidade: "Varginha",
    estado: "MG",
    estado_cafe: "verde" as const,
    data_analise: "2024-04-05",
    decisao: "AGUARDAR" as const,
    explicacao_decisao: "Mercado saturado de Catuaí neste período. Preços abaixo da média. Condições climáticas estáveis permitem armazenamento por mais 30 dias."
  },
  {
    id: 4,
    usuario_id: 1,
    tipo_cafe: "Arábica",
    data_colheita: "2024-06-01",
    quantidade: 950.25,
    cidade: "Varginha",
    estado: "MG",
    estado_cafe: "torrado" as const,
    data_analise: "2024-06-20",
    decisao: "VENDER" as const,
    explicacao_decisao: "Café torrado tem prazo de validade reduzido. Preço atual compensa venda imediata. Alta demanda por torrados premium."
  },
  {
    id: 5,
    usuario_id: 1,
    tipo_cafe: "Mundo Novo",
    data_colheita: "2024-02-15",
    quantidade: 1800.00,
    cidade: "Varginha",
    estado: "MG",
    estado_cafe: "verde" as const,
    data_analise: "2024-03-10",
    decisao: "VENDER_PARCIALMENTE" as const,
    explicacao_decisao: "Grande volume disponível. Vender 40% para capital rápido e aguardar contratos de exportação que fecham em 3 semanas."
  },
  {
    id: 6,
    usuario_id: 1,
    tipo_cafe: "Bourbon",
    data_colheita: "2024-01-20",
    quantidade: 750.50,
    cidade: "Varginha",
    estado: "MG",
    estado_cafe: "moído" as const,
    data_analise: "2024-02-15",
    decisao: "VENDER" as const,
    explicacao_decisao: "Produto moído tem alta rotatividade. Preço está 15% acima da média sazonal. Vender todo estoque para evitar perda de aroma."
  },
  
  // Análises da Cooperativa Café Mineiro - 2 análises
  {
    id: 7,
    usuario_id: 2,
    tipo_cafe: "Conilon",
    data_colheita: "2024-03-10",
    quantidade: 3000.00,
    cidade: "Linhares",
    estado: "ES",
    estado_cafe: "verde" as const,
    data_analise: "2024-04-05",
    decisao: "AGUARDAR" as const,
    explicacao_decisao: "Mercado de Conilon em baixa. Previsão de geada no Paraná pode elevar preços nas próximas semanas. Condições de armazenamento adequadas."
  },
  {
    id: 8,
    usuario_id: 2,
    tipo_cafe: "Robusta",
    data_colheita: "2024-04-15",
    quantidade: 2500.75,
    cidade: "Linhares",
    estado: "ES",
    estado_cafe: "verde" as const,
    data_analise: "2024-05-20",
    decisao: "VENDER" as const,
    explicacao_decisao: "Alta demanda por Robusta para blends. Preço atingiu patamar ideal. Clima quente do ES pode comprometer qualidade se armazenado por muito tempo."
  }
];


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

  const login = async (email: string, password: string): Promise<AuthResponse> => {
    setLoading(true);
    try {
      // =====================================================
      //  **TROCAR AQUI QUANDO GATEWAY ESTIVER PRONTO**
      // =====================================================
      // const response = await fetch('http://localhost:3000/auth/login', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ email, password })
      // });
      // 
      // if (!response.ok) {
      //   const errorData = await response.json();
      //   return { success: false, error: errorData.detail || "Erro na autenticação" };
      // }
      // 
      // const data = await response.json();
      // const { access_token, user: userData } = data;
      // 
      // setUser(userData);
      // setToken(access_token);
      // localStorage.setItem('authToken', access_token);
      // localStorage.setItem('user', JSON.stringify(userData));
      // 
      // return { success: true, user: userData };
      // =====================================================

      // **CÓDIGO MOCKADO - MANTER POR ENQUANTO**
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const usuario = MOCK_USUARIOS.find(u => u.email === email);
      
      if (usuario && (password === "senha123" || email === "joao.produtor@email.com")) {
        const mockToken = "mock_jwt_token_12345";
        setUser(usuario);
        setToken(mockToken);

        const userAnalises = MOCK_ANALISES.filter(a => a.usuario_id === usuario.id);
        setAnalisesUsuario(userAnalises);

        localStorage.setItem('authToken', mockToken);
        localStorage.setItem('user', JSON.stringify(usuario));
        return { success: true, user: usuario };
      } else {
        return { success: false, error: "Credenciais inválidas" };
      }
    } catch (error) {
      return { success: false, error: "Erro ao conectar com o servidor" };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    // =====================================================
    // **ADICIONAR AQUI QUANDO GATEWAY ESTIVER PRONTO**
    // =====================================================
    // await fetch('http://localhost:3000/auth/logout', {
    //   method: 'POST',
    //   headers: { 'Authorization': `Bearer ${token}` }
    // });
    // =====================================================

    // **CÓDIGO MOCKADO - MANTER POR ENQUANTO**
    setUser(null);
    setToken(null);
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  };

  useEffect(() => {
    const savedToken = localStorage.getItem('authToken');
    const savedUser = localStorage.getItem('user');
    
    if (savedToken && savedUser) {
      // =====================================================
      // **TROCAR AQUI QUANDO GATEWAY ESTIVER PRONTO**
      // =====================================================
      // // Validar token com o gateway
      // const validateToken = async () => {
      //   try {
      //     const response = await fetch('http://localhost:3000/auth/validate', {
      //       headers: { 'Authorization': `Bearer ${savedToken}` }
      //     });
      //     
      //     if (response.ok) {
      //       const userData = JSON.parse(savedUser);
      //       setUser(userData);
      //       setToken(savedToken);
      //     } else {
      //       // Token inválido, limpar localStorage
      //       localStorage.removeItem('authToken');
      //       localStorage.removeItem('user');
      //     }
      //   } catch (error) {
      //     localStorage.removeItem('authToken');
      //     localStorage.removeItem('user');
      //   }
      // };
      // 
      // validateToken();
      // =====================================================

      // **CÓDIGO MOCKADO - MANTER POR ENQUANTO**
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const value: AuthContextType = {
    user,
    token,
    loading,
    login,
    logout,
    isAuthenticated: !!user && !!token,
    analisesUsuario
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