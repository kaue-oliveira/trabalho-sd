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
  { id: 1, usuario_id: 1, tipo_cafe: "Arábica", data_colheita: "2025-10-15", quantidade: 1500.50, cidade: "Varginha", estado: "MG", estado_cafe: "verde" as const, data_analise: "2025-11-01", decisao: "VENDER" as const, explicacao_decisao: "Preço do Arábica em alta de 8% no mercado futuro. Previsão de chuva intensa na região pode comprometer qualidade do grão armazenado. Relatórios indicam baixa oferta nos próximos 30 dias." },
  { id: 2, usuario_id: 1, tipo_cafe: "Arábica", data_colheita: "2025-09-20", quantidade: 800.75, cidade: "Varginha", estado: "MG", estado_cafe: "verde" as const, data_analise: "2025-10-10", decisao: "VENDER_PARCIALMENTE" as const, explicacao_decisao: "Preço atual favorável com tendência de alta moderada. Previsão de geada no Paraná pode valorizar estoques. Vender 50% agora e aguardar potencial valorização." },
  { id: 3, usuario_id: 1, tipo_cafe: "Robusta", data_colheita: "2025-08-10", quantidade: 1200.00, cidade: "Varginha", estado: "MG", estado_cafe: "verde" as const, data_analise: "2025-09-05", decisao: "AGUARDAR" as const, explicacao_decisao: "Mercado de Robusta saturado por exportações vietnamitas. Previsão de estiagem pode reduzir oferta nacional em 60 dias. Condições climáticas estáveis para armazenamento." },
  { id: 4, usuario_id: 1, tipo_cafe: "Arábica", data_colheita: "2025-07-01", quantidade: 950.25, cidade: "Varginha", estado: "MG", estado_cafe: "torrado" as const, data_analise: "2025-07-20", decisao: "VENDER" as const, explicacao_decisao: "Alta sazonalidade no consumo de torrados. Preço 12% acima da média. Umidade relativa alta pode comprometer qualidade do produto final." },
  { id: 5, usuario_id: 1, tipo_cafe: "Robusta", data_colheita: "2025-05-15", quantidade: 1800.00, cidade: "Varginha", estado: "MG", estado_cafe: "verde" as const, data_analise: "2025-06-10", decisao: "VENDER_PARCIALMENTE" as const, explicacao_decisao: "Demanda industrial por Robusta em crescimento. Previsão de El Niño pode afetar próxima safra. Vender 60% para capital imediato." },
  { id: 6, usuario_id: 1, tipo_cafe: "Arábica", data_colheita: "2024-12-20", quantidade: 750.50, cidade: "Varginha", estado: "MG", estado_cafe: "moído" as const, data_analise: "2025-01-15", decisao: "VENDER" as const, explicacao_decisao: "Produto moído com validade crítica. Preço de mercado 15% acima do esperado. Temperaturas elevadas aceleram perda de características organolépticas." },
  { id: 7, usuario_id: 2, tipo_cafe: "Robusta", data_colheita: "2024-11-10", quantidade: 3000.00, cidade: "Linhares", estado: "ES", estado_cafe: "verde" as const, data_analise: "2024-12-05", decisao: "AGUARDAR" as const, explicacao_decisao: "Excesso de oferta no mercado internacional. Previsão de chuva no Espírito Santo pode melhorar qualidade. Esperar abertura de novos contratos de exportação." },
  { id: 8, usuario_id: 2, tipo_cafe: "Robusta", data_colheita: "2024-09-15", quantidade: 2500.75, cidade: "Linhares", estado: "ES", estado_cafe: "verde" as const, data_analise: "2024-10-20", decisao: "VENDER" as const, explicacao_decisao: "Queda na produção brasileira de Robusta. Preço atingiu patamar ideal com alta de 18%. Clima quente pode acelerar processo de fermentação." },
  { id: 9, usuario_id: 1, tipo_cafe: "Arábica", data_colheita: "2024-07-10", quantidade: 2200.80, cidade: "Varginha", estado: "MG", estado_cafe: "verde" as const, data_analise: "2024-08-01", decisao: "AGUARDAR" as const, explicacao_decisao: "Preço abaixo do custo de produção. Previsão de geada em Minas Gerais pode causar valorização expressiva. Condições ideais de armazenamento por 90 dias." },
  { id: 10, usuario_id: 1, tipo_cafe: "Robusta", data_colheita: "2024-05-25", quantidade: 1350.25, cidade: "Varginha", estado: "MG", estado_cafe: "torrado" as const, data_analise: "2024-06-15", decisao: "VENDER" as const, explicacao_decisao: "Alta demanda por Robusta torrado no varejo. Preço 22% acima da média histórica. Umidade relativa em queda favorece conservação limitada." },
  { id: 11, usuario_id: 1, tipo_cafe: "Arábica", data_colheita: "2024-03-05", quantidade: 1850.60, cidade: "Varginha", estado: "MG", estado_cafe: "verde" as const, data_analise: "2024-04-10", decisao: "VENDER_PARCIALMENTE" as const, explicacao_decisao: "Mercado internacional em alta moderada. Previsão de chuva excessiva pode comprometer logística. Vender 70% e aguardar estabilização climática." },
  { id: 12, usuario_id: 1, tipo_cafe: "Robusta", data_colheita: "2024-01-18", quantidade: 920.45, cidade: "Varginha", estado: "MG", estado_cafe: "moído" as const, data_analise: "2024-02-20", decisao: "VENDER" as const, explicacao_decisao: "Prazo de validade crítico para produto moído. Preço atual compensa venda imediata. Temperaturas elevadas aceleram oxidação." },
  { id: 13, usuario_id: 1, tipo_cafe: "Arábica", data_colheita: "2023-11-12", quantidade: 3100.75, cidade: "Varginha", estado: "MG", estado_cafe: "verde" as const, data_analise: "2023-12-05", decisao: "AGUARDAR" as const, explicacao_decisao: "Excesso de oferta no mercado doméstico. Previsão de seca prolongada pode reduzir próxima safra. Armazenamento em silos climatizados recomendado." },
  { id: 14, usuario_id: 1, tipo_cafe: "Robusta", data_colheita: "2023-09-30", quantidade: 2750.90, cidade: "Varginha", estado: "MG", estado_cafe: "verde" as const, data_analise: "2023-10-25", decisao: "VENDER_PARCIALMENTE" as const, explicacao_decisao: "Queda na produção vietnamita cria oportunidade. Preço em tendência de alta. Vender 50% para contratos spot e aguardar maximização de ganhos." },
  { id: 15, usuario_id: 1, tipo_cafe: "Arábica", data_colheita: "2023-07-08", quantidade: 1420.30, cidade: "Varginha", estado: "MG", estado_cafe: "torrado" as const, data_analise: "2023-08-02", decisao: "VENDER" as const, explicacao_decisao: "Sazonalidade de fim de ano impulsiona preços. Demanda por torrados premium em alta de 25%. Escoamento recomendado em 21 dias." },
  { id: 16, usuario_id: 1, tipo_cafe: "Robusta", data_colheita: "2023-04-22", quantidade: 1680.15, cidade: "Varginha", estado: "MG", estado_cafe: "moído" as const, data_analise: "2023-05-18", decisao: "AGUARDAR" as const, explicacao_decisao: "Mercado industrial em recessão temporária. Previsão de recuperação em 45 dias. Embalagem a vácuo garante preservação por 4 meses." },
  { id: 17, usuario_id: 1, tipo_cafe: "Arábica", data_colheita: "2022-12-05", quantidade: 1150.40, cidade: "Varginha", estado: "MG", estado_cafe: "verde" as const, data_analise: "2023-01-01", decisao: "VENDER_PARCIALMENTE" as const, explicacao_decisao: "Preço estável com tendência de alta no curto prazo. Previsão de veranico pode afetar qualidade. Vender 80% e monitorar condições climáticas." },
  { id: 18, usuario_id: 1, tipo_cafe: "Robusta", data_colheita: "2022-08-15", quantidade: 1950.65, cidade: "Varginha", estado: "MG", estado_cafe: "verde" as const, data_analise: "2022-09-12", decisao: "VENDER" as const, explicacao_decisao: "Crise logística na Ásia cria janela de oportunidade. Preço internacional em alta de 30%. Vender todo estoque para contratos de exportação." }
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
        return { success: false, error: "Usuário e/ou senha incorretos" };
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