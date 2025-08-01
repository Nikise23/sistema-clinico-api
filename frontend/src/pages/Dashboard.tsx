import React from 'react';
import { Users, Calendar, DollarSign, TrendingUp } from 'lucide-react';

const Dashboard: React.FC = () => {
  const stats = [
    {
      name: 'Total Pacientes',
      value: '1,234',
      change: '+12%',
      changeType: 'increase',
      icon: Users,
    },
    {
      name: 'Citas Hoy',
      value: '12',
      change: '+5',
      changeType: 'increase',
      icon: Calendar,
    },
    {
      name: 'Ingresos del Mes',
      value: '$24,500',
      change: '+8%',
      changeType: 'increase',
      icon: DollarSign,
    },
    {
      name: 'Crecimiento',
      value: '18%',
      change: '+2%',
      changeType: 'increase',
      icon: TrendingUp,
    },
  ];
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-5">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-sm text-gray-700">
          Bienvenido a tu sistema de gestión clínica personal
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((item) => {
          const Icon = item.icon;
          return (
            <div
              key={item.name}
              className="relative bg-white pt-5 px-4 pb-12 sm:pt-6 sm:px-6 shadow rounded-lg overflow-hidden"
            >
              <dt>
                <div className="absolute bg-primary-500 rounded-md p-3">
                  <Icon className="h-6 w-6 text-white" aria-hidden="true" />
                </div>
                <p className="ml-16 text-sm font-medium text-gray-500 truncate">
                  {item.name}
                </p>
              </dt>
              <dd className="ml-16 pb-6 flex items-baseline sm:pb-7">
                <p className="text-2xl font-semibold text-gray-900">
                  {item.value}
                </p>
                <p
                  className={`ml-2 flex items-baseline text-sm font-semibold ${
                    item.changeType === 'increase'
                      ? 'text-green-600'
                      : 'text-red-600'
                  }`}
                >
                  {item.change}
                </p>
                <div className="absolute bottom-0 inset-x-0 bg-gray-50 px-4 py-4 sm:px-6">
                  <div className="text-sm">
                    <a
                      href="#"
                      className="font-medium text-primary-600 hover:text-primary-500"
                    >
                      Ver detalles
                    </a>
                  </div>
                </div>
              </dd>
            </div>
          );
        })}
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Próximas Citas */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Próximas Citas
            </h3>
            <div className="mt-4 space-y-4">
              {[1, 2, 3].map((item) => (
                <div key={item} className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      María González
                    </p>
                    <p className="text-sm text-gray-500">Consulta general</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-900">14:30</p>
                    <p className="text-sm text-gray-500">Hoy</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Pacientes Recientes */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Pacientes Recientes
            </h3>
            <div className="mt-4 space-y-4">
              {[1, 2, 3].map((item) => (
                <div key={item} className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center">
                      <span className="text-sm font-medium text-gray-700">
                        MG
                      </span>
                    </div>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-900">
                      María González
                    </p>
                    <p className="text-sm text-gray-500">
                      Registrado hace 2 días
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;