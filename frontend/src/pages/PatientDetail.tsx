import React from 'react';
import { useParams } from 'react-router-dom';

const PatientDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-5">
        <h1 className="text-2xl font-bold text-gray-900">
          Detalle del Paciente
        </h1>
        <p className="mt-2 text-sm text-gray-700">
          ID del paciente: {id}
        </p>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <p className="text-gray-500">
          Esta página estará disponible próximamente...
        </p>
      </div>
    </div>
  );
};

export default PatientDetail;