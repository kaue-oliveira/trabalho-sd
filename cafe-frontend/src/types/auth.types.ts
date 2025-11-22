/**
 * Interfaces TypeScript para autenticação
 * 
 * Define tipos de usuário, dados de login e respostas da API
 * 
 * Estruturas: Usuario, LoginData, AuthResponse
 */

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