/**
 * Componente de formulário reutilizável
 * 
 * Campos: texto, email, senha, select
 * Features: toggle de senha, ícones, validações
 * 
 * Props: campos, título, ações, footer
 * Estados: dados do form, visibilidade de senha
 */

import React, { useState } from 'react';
import styles from './Form.module.css';

export type FieldType = 'text' | 'email' | 'password' | 'select';

export interface FormField {
  name: string;
  label: string;
  type: FieldType;
  placeholder: string;
  icon: string;
  showPasswordToggle?: boolean;
  options?: string[]; // Para campos select
  helperText?: string | React.ReactNode;
}

export interface FormProps {
  title: string;
  subtitle?: string;
  fields: FormField[];
  submitButtonText: string;
  onSubmit: (data: Record<string, string>) => void;
  footerText?: string;
  footerLinkText?: string;
  footerLinkHref?: string;
  showLogo?: boolean;
  logoText?: string;
  logoIcon?: string;
  showBackButton?: boolean;
  backButtonHref?: string;
  backButtonOnClick?: () => void;
}

interface InputFieldProps {
  field: FormField;
  value: string;
  onChange: (value: string) => void;
}

const InputField: React.FC<InputFieldProps> = ({ field, value, onChange }) => {
  const [showPassword, setShowPassword] = useState(false);
  const inputType = field.showPasswordToggle
    ? (showPassword ? 'text' : 'password')
    : field.type;

  return (
    <label className={styles.inputLabel}>
      <p className={styles.labelText}>{field.label}</p>
      <div className={styles.inputWrapper}>
        <i className={`${styles.materialIcon} ${styles.iconLeft}`}>
          {field.icon}
        </i>
        <input
          className={styles.input}
          type={inputType}
          placeholder={field.placeholder}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          name={field.name}
        />
        {field.showPasswordToggle && (
          <button
            type="button"
            className={styles.togglePassword}
            onClick={() => setShowPassword(!showPassword)}
            aria-label="Alternar visibilidade da senha"
          >
            <i className={styles.materialIcon}>
              {showPassword ? 'visibility' : 'visibility_off'}
            </i>
          </button>
        )}
      </div>
      {field.helperText && (
        <p className={styles.helperText}>{field.helperText}</p>
      )}
    </label>
  );
};

interface SelectFieldProps {
  field: FormField;
  value: string;
  onChange: (value: string) => void;
}

const SelectField: React.FC<SelectFieldProps> = ({ field, value, onChange }) => {
  return (
    <label className={styles.inputLabel}>
      <p className={styles.labelText}>{field.label}</p>
      <div className={styles.inputWrapper}>
        <i className={`${styles.materialIcon} ${styles.iconLeft}`}>
          {field.icon}
        </i>
        <select
          className={styles.select}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          name={field.name}
        >
          {field.options?.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
        <i className={`${styles.materialIcon} ${styles.iconRight}`}>
          expand_more
        </i>
      </div>
    </label>
  );
};

const Form: React.FC<FormProps> = ({
  title,
  subtitle,
  fields,
  submitButtonText,
  onSubmit,
  footerText,
  footerLinkText,
  footerLinkHref,
  showLogo = false,
  logoText = 'AgroAnalytics',
  logoIcon = 'eco',
  showBackButton = false,
  backButtonHref,
  backButtonOnClick
}) => {
  const [formData, setFormData] = useState<Record<string, string>>(
    fields.reduce((acc, field) => {
      acc[field.name] = field.type === 'select' && field.options ? field.options[0] : '';
      return acc;
    }, {} as Record<string, string>)
  );

  const handleChange = (name: string, value: string) => {
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = () => {
    onSubmit(formData);
  };

  return (
    <div className={styles.formContainer}>
      <div className={styles.card}>
        <div className={styles.cardContent}>
          {showBackButton && (
            <div className={styles.backButtonContainer}>
              {backButtonHref ? (
                <a 
                  href={backButtonHref} 
                  className={styles.backButton}
                  aria-label="Voltar"
                >
                  <i className={styles.materialIcon}>arrow_back</i>
                </a>
              ) : (
                <button 
                  onClick={backButtonOnClick}
                  className={styles.backButton}
                  type="button"
                  aria-label="Voltar"
                >
                  <i className={styles.materialIcon}>arrow_back</i>
                </button>
              )}
            </div>
          )}

          {showLogo && (
            <div className={styles.logoContainer}>
              <div className={styles.logo}>
                <i className={`${styles.materialIcon} ${styles.logoIcon}`}>
                  {logoIcon}
                </i>
                <h1 className={styles.logoText}>{logoText}</h1>
              </div>
            </div>
          )}

          <h2 className={styles.title}>{title}</h2>
          {subtitle && <p className={styles.subtitle}>{subtitle}</p>}

          <div className={styles.formFields}>
            {fields.map((field) => (
              <div key={field.name}>
                {field.type === 'select' ? (
                  <SelectField
                    field={field}
                    value={formData[field.name]}
                    onChange={(value) => handleChange(field.name, value)}
                  />
                ) : (
                  <InputField
                    field={field}
                    value={formData[field.name]}
                    onChange={(value) => handleChange(field.name, value)}
                  />
                )}
              </div>
            ))}
          </div>

          <button
            type="button"
            onClick={handleSubmit}
            className={styles.submitButton}
          >
            {submitButtonText}
          </button>

          {footerText && (
            <p className={styles.footerText}>
              {footerText}{' '}
              {footerLinkText && footerLinkHref && (
                <a href={footerLinkHref} className={styles.link}>
                  {footerLinkText}
                </a>
              )}
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Form;