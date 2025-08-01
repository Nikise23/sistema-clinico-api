import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { User, Lock, Stethoscope } from 'lucide-react';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import { authAPI } from '../services/api';
import { LoginRequest } from '../types';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginRequest>();

  const onSubmit = async (data: LoginRequest) => {
    setLoading(true);
    setError('');

    try {
      const response = await authAPI.login(data);
      
      // Store token and user data
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
      
      // Redirect to dashboard
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al iniciar sesión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="mx-auto h-16 w-16 bg-primary-600 rounded-full flex items-center justify-center">
            <Stethoscope className="h-8 w-8 text-white" />
          </div>
          <h2 className="mt-6 text-3xl font-bold text-gray-900">
            Sistema Clínico Personal
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Ingresa a tu cuenta para continuar
          </p>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-xl shadow-lg p-8 glass-effect">
          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            <Input
              label="Usuario"
              type="text"
              leftIcon={<User className="h-4 w-4" />}
              placeholder="Ingresa tu usuario"
              error={errors.username?.message}
              {...register('username', {
                required: 'El usuario es requerido',
              })}
            />
            <Input
              label="Contraseña"
              type="password"
              leftIcon={<Lock className="h-4 w-4" />}
              placeholder="Ingresa tu contraseña"
              error={errors.password?.message}
              {...register('password', {
                required: 'La contraseña es requerida',
              })}
            />

            <Button
              type="submit"
              size="lg"
              loading={loading}
              className="w-full"
            >
              {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              ¿No tienes una cuenta?{' '}
              <a href="#" className="font-medium text-primary-600 hover:text-primary-500">
                Contacta al administrador
              </a>
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center">
          <p className="text-xs text-gray-500">
            © 2024 Sistema Personal de Gestión Clínica. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;