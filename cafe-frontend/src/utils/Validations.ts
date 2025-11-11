export interface ValidationResult {
  isValid: boolean;
  message?: string;
}

export const FIELD_LIMITS = {
  // Tabela usuarios
  USUARIO: {
    NOME: { min: 2, max: 100 },
    EMAIL: { min: 5, max: 255 },
    SENHA: { min: 6, max: 255 },
  },
  // Tabela analises
  ANALISE: {
    TIPO_CAFE: { min: 2, max: 100 },
    CIDADE: { min: 2, max: 100 },
    ESTADO: { min: 2, max: 2 },
  }
};

export const validations = {
  // Validação de campo obrigatório
  required: (value: string, fieldName: string): ValidationResult => {
    if (!value || !value.trim()) {
      return {
        isValid: false,
        message: `${fieldName} é obrigatório.`
      };
    }
    return { isValid: true };
  },

  // Validação de email
  email: (email: string): ValidationResult => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return {
        isValid: false,
        message: 'Por favor, insira um email válido.'
      };
    }
    return { isValid: true };
  },

  // Validação de tamanho mínimo
  minLength: (value: string, min: number, fieldName: string): ValidationResult => {
    if (value && value.length < min) {
      return {
        isValid: false,
        message: `${fieldName} deve ter pelo menos ${min} caracteres.`
      };
    }
    return { isValid: true };
  },

  // Validação de tamanho máximo
  maxLength: (value: string, max: number, fieldName: string): ValidationResult => {
    if (value && value.length > max) {
      return {
        isValid: false,
        message: `${fieldName} não pode exceder ${max} caracteres.`
      };
    }
    return { isValid: true };
  },

  // Validação de senha forte
  strongPassword: (password: string): ValidationResult => {
    if (!password) return { isValid: true }; // Senha opcional
    
    const checks = [
      {
        test: password.length >= FIELD_LIMITS.USUARIO.SENHA.min,
        message: `A senha deve ter pelo menos ${FIELD_LIMITS.USUARIO.SENHA.min} caracteres.`
      },
      {
        test: password.length <= FIELD_LIMITS.USUARIO.SENHA.max,
        message: `A senha não pode exceder ${FIELD_LIMITS.USUARIO.SENHA.max} caracteres.`
      },
      {
        test: /(?=.*[A-Z])/.test(password),
        message: 'A senha deve conter pelo menos uma letra maiúscula.'
      },
      {
        test: /(?=.*[a-z])/.test(password),
        message: 'A senha deve conter pelo menos uma letra minúscula.'
      },
      {
        test: /(?=.*\d)/.test(password),
        message: 'A senha deve conter pelo menos um número.'
      }
    ];

    for (const check of checks) {
      if (!check.test) {
        return { isValid: false, message: check.message };
      }
    }

    return { isValid: true };
  },

  // Validação de confirmação de senha
  passwordMatch: (password: string, confirmPassword: string): ValidationResult => {
    if (password && password !== confirmPassword) {
      return {
        isValid: false,
        message: 'As senhas não coincidem.'
      };
    }
    return { isValid: true };
  },

  // Validação de nome de usuário
  userName: (name: string): ValidationResult => {
    const validators = [
      validations.required(name, 'Nome completo'),
      validations.minLength(name, FIELD_LIMITS.USUARIO.NOME.min, 'Nome completo'),
      validations.maxLength(name, FIELD_LIMITS.USUARIO.NOME.max, 'Nome completo'),
    ];

    return validators.find(validator => !validator.isValid) || { isValid: true };
  },

  // Validação de email com limites
  emailWithLimits: (email: string): ValidationResult => {
    const validators = [
      validations.required(email, 'Email'),
      validations.email(email),
      validations.minLength(email, 5, 'Email'),
      validations.maxLength(email, FIELD_LIMITS.USUARIO.EMAIL.max, 'Email'),
    ];

    return validators.find(validator => !validator.isValid) || { isValid: true };
  },

  // Validação para tipo de café
  coffeeType: (coffeeType: string): ValidationResult => {
    const validators = [
      validations.required(coffeeType, 'Tipo de café'),
      validations.minLength(coffeeType, FIELD_LIMITS.ANALISE.TIPO_CAFE.min, 'Tipo de café'),
      validations.maxLength(coffeeType, FIELD_LIMITS.ANALISE.TIPO_CAFE.max, 'Tipo de café'),
    ];

    return validators.find(validator => !validator.isValid) || { isValid: true };
  },

  // Validação para cidade
  city: (city: string): ValidationResult => {
    const validators = [
      validations.required(city, 'Cidade'),
      validations.minLength(city, FIELD_LIMITS.ANALISE.CIDADE.min, 'Cidade'),
      validations.maxLength(city, FIELD_LIMITS.ANALISE.CIDADE.max, 'Cidade'),
    ];

    return validators.find(validator => !validator.isValid) || { isValid: true };
  },

  // Validação para estado (UF)
  state: (state: string): ValidationResult => {
    const validators = [
      validations.required(state, 'Estado'),
      validations.minLength(state, FIELD_LIMITS.ANALISE.ESTADO.min, 'Estado'),
      validations.maxLength(state, FIELD_LIMITS.ANALISE.ESTADO.max, 'Estado'),
    ];

    return validators.find(validator => !validator.isValid) || { isValid: true };
  },

  decimalNumber: (value: string, fieldName: string, maxInteger: number = 6, maxDecimal: number = 2): ValidationResult => {
    if (!value || !value.trim()) {
      return {
        isValid: false,
        message: `${fieldName} é obrigatório.`
      };
    }

    // Verificar se contém apenas números e um ponto decimal
    if (!/^-?\d*\.?\d*$/.test(value)) {
      return {
        isValid: false,
        message: `${fieldName} deve conter apenas números e ponto decimal.`
      };
    }

    // Verificar formato específico (máximo de dígitos inteiros e decimais)
    const regex = new RegExp(`^\\d{1,${maxInteger}}(\\.\\d{1,${maxDecimal}})?$`);
    if (!regex.test(value)) {
      return {
        isValid: false,
        message: `${fieldName} deve ter no máximo ${maxInteger} dígitos inteiros e ${maxDecimal} decimais.`
      };
    }

    // Converter para número e verificar se é válido
    const numberValue = parseFloat(value);
    if (isNaN(numberValue)) {
      return {
        isValid: false,
        message: `${fieldName} deve ser um número válido.`
      };
    }

    if (numberValue <= 0) {
      return {
        isValid: false,
        message: `${fieldName} deve ser maior que zero.`
      };
    }

    return { isValid: true };
  },
  
};

// Validações específicas para formulários
export const profileValidations = {
  validateProfile: (formData: {
    fullName: string;
    email: string;
    newPassword: string;
    confirmPassword: string;
  }) => {
    const validators = [
      validations.userName(formData.fullName),
      validations.emailWithLimits(formData.email),
    ];

    if (formData.newPassword) {
      validators.push(
        validations.strongPassword(formData.newPassword),
        validations.passwordMatch(formData.newPassword, formData.confirmPassword)
      );
    }

    return validators.find(validator => !validator.isValid) || { isValid: true };
  }
};

export const loginValidations = {
  validateLogin: (email: string, password: string) => {
    const validators = [
      validations.emailWithLimits(email),
      validations.required(password, 'Senha'),
    ];

    return validators.find(validator => !validator.isValid) || { isValid: true };
  }
};

export const registerValidations = {
  validateRegister: (formData: {
    fullName: string;
    email: string;
    password: string;
    confirmPassword: string;
  }) => {
    const validators = [
      validations.userName(formData.fullName),
      validations.emailWithLimits(formData.email),
      validations.required(formData.password, 'Senha'),
      validations.strongPassword(formData.password),
      validations.passwordMatch(formData.password, formData.confirmPassword),
    ];

    return validators.find(validator => !validator.isValid) || { isValid: true };
  }
};

// Validações para análises
export const analysisValidations = {
  validateAnalysis: (formData: {
    tipo_cafe: string;
    cidade: string;
    estado: string;
    quantidade: number | string;
  }) => {
    const validators = [
      validations.coffeeType(formData.tipo_cafe),
      validations.city(formData.cidade),
      validations.state(formData.estado),
    ];

    // Validação de quantidade
    const quantidadeValidation = validations.decimalNumber(
      formData.quantidade?.toString() || '', 
      'Quantidade'
    );
    validators.push(quantidadeValidation);

    return validators.find(validator => !validator.isValid) || { isValid: true };
  }
};

// Validação para formulário de esqueci senha
export const forgotPasswordValidations = {
  validateForgotPassword: (email: string) => {
    return validations.emailWithLimits(email);
  }
};

// Validação para formulário de trocar senha
export const changePasswordValidations = {
  validateChangePassword: (newPassword: string, confirmPassword: string) => {
    const validators = [
      validations.required(newPassword, 'Nova senha'),
      validations.required(confirmPassword, 'Confirmação de senha'),
      validations.strongPassword(newPassword),
      validations.passwordMatch(newPassword, confirmPassword)
    ];

    return validators.find(validator => !validator.isValid) || { isValid: true };
  }
};