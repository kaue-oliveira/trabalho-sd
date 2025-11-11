export interface Usuario {
  id: number;
  nome: string;
  email: string;
  tipo_conta: 'PRODUTOR' | 'COOPERATIVA';
}

export interface LoginData {
  email: string;
  password: string;
}

export interface AuthResponse {
  success: boolean;
  user?: Usuario;
  error?: string;
}

// =====================================================
// **ADICIONAR AQUI QUANDO GATEWAY ESTIVER PRONTO**
// =====================================================
// export interface TokenResponse {
//   access_token: string;
//   token_type: string;
//   user: Usuario;
// }
// =====================================================