# 🔧 API Documentation - Sistema Personal de Gestión Clínica

## 📋 Overview

Esta API REST proporciona endpoints para la gestión completa de un consultorio médico/odontológico.

**Base URL**: `http://localhost:8000/api`

**Autenticación**: Bearer Token (JWT)

## 🔐 Autenticación

### POST `/auth/register`
Registra un nuevo usuario en el sistema.

```json
{
  "email": "doctor@clinica.com",
  "username": "doctor1",
  "first_name": "Juan",
  "last_name": "Pérez",
  "role": "doctor",
  "phone": "+5491123456789",
  "password": "password123"
}
```

**Respuesta:**
```json
{
  "id": "uuid",
  "email": "doctor@clinica.com",
  "username": "doctor1",
  "first_name": "Juan",
  "last_name": "Pérez",
  "role": "doctor",
  "phone": "+5491123456789",
  "is_verified": true,
  "created_at": "2024-01-01T00:00:00Z"
}

```

### POST `/auth/login`
Inicia sesión y obtiene un token de acceso.

```json
{
  "username": "doctor1",
  "password": "password123"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 2592000,
  "user": {
    "id": "uuid",
    "email": "doctor@clinica.com",
    "username": "doctor1",
    "first_name": "Juan",
    "last_name": "Pérez",
    "role": "doctor"
  }
}
```

### GET `/auth/me`
Obtiene información del usuario actual.

**Headers**: `Authorization: Bearer <token>`

## 👥 Gestión de Pacientes

### POST `/patients`
Crea un nuevo paciente.

```json

{
  "first_name": "María",
  "last_name": "González",
  "date_of_birth": "1990-05-15",
  "gender": "female",
  "dni": "12345678",
  "email": "maria@email.com",
  "phone": "+5491198765432",
  "address": "Av. Corrientes 1234",
  "city": "Buenos Aires",
  "state": "CABA",
  "postal_code": "1043",
  "country": "Argentina",
  "medical_history": "Sin antecedentes relevantes",
  "allergies": "Ninguna",
  "emergency_contact_name": "Juan González",
  "emergency_contact_phone": "+5491187654321",
  "insurance_provider": "OSDE",
  "insurance_number": "12345678901"
}
```

### GET `/patients`
Lista todos los pacientes con paginación y búsqueda.

**Query Parameters:**
- `skip`: Número de registros a omitir (default: 0)
- `limit`: Número máximo de registros (default: 50, max: 100)
- `search`: Texto para buscar en nombre, apellido, DNI, teléfono

**Ejemplo:**
`GET /patients?skip=0&limit=20&search=María`

### GET `/patients/{patient_id}`
Obtiene un paciente específico por ID.

### PUT `/patients/{patient_id}`
Actualiza un paciente existente.

### DELETE `/patients/{patient_id}`
Elimina (soft delete) un paciente.

### GET `/patients/{patient_id}/summary`
Obtiene un resumen completo del paciente con citas y tratamientos.

**Respuesta:**
```json
{
  "patient": { /* datos del paciente */ },
  "summary": {
    "total_appointments": 15,
    "upcoming_appointments": 2,
    "total_treatments": 8,
    "total_spent": 45000.00,
    "current_debt": 5000.00
  },
  "recent_treatments": [ /* últimos 5 tratamientos */ ],
  "upcoming_appointments": [ /* próximas 3 citas */ ]
}
```

## 📅 Gestión de Citas

### POST `/appointments`
Crea una nueva cita.

```json
{
  "patient_id": "uuid",
  "doctor_id": "uuid",
  "appointment_date": "2024-02-15T14:30:00Z",
  "duration_minutes": 60,
  "treatment_type": "consultation",
  "notes": "Control de rutina",
  "cost": 5000.00
}
```

### GET `/appointments`
Lista todas las citas con filtros.

**Query Parameters:**
- `skip`, `limit`: Paginación
`patient_id`: Filtrar por paciente
- `doctor_id`: Filtrar por doctor
- `status`: Filtrar por estado
- `date_from`, `date_to`: Rango de fechas

### GET `/appointments/{appointment_id}`
Obtiene una cita específica.

### PUT `/appointments/{appointment_id}`
Actualiza una cita.

### DELETE `/appointments/{appointment_id}`
Cancela una cita.

## 💉 Gestión de Tratamientos

### POST `/treatments`
Registra un nuevo tratamiento.

```json
{
  "patient_id": "uuid",
  "doctor_id": "uuid",
  "appointment_id": "uuid",
  "treatment_type": "filling",
  "description": "Obturación dental en molar superior derecho",
  "date_performed": "2024-01-15T10:00:00Z",
  "cost": 15000.00,
  "notes": "Tratamiento sin complicaciones",
  "teeth_involved": [16, 17]
}
```

### GET `/treatments`
Lista todos los tratamientos.

### GET `/treatments/{treatment_id}`
Obtiene un tratamiento específico.

## 💰 Gestión de Pagos

### POST `/payments`
Registra un nuevo pago.

```json
{
  "patient_id": "uuid",
  "appointment_id": "uuid",
  "treatment_id": "uuid",
  "amount": 10000.00,
  "payment_date": "2024-01-15T14:00:00Z",
  "payment_method": "card",
  "notes": "Pago parcial del tratamiento"
}
```

### GET `/payments`
Lista todos los pagos.

## 📊 Reportes y Estadísticas

### GET `/reports/dashboard`
Obtiene estadísticas para el dashboard.

```json
{
  "total_patients": 150,
  "appointments_today": 8,
  "appointments_week": 45,
  "revenue_month": 180000.00,
  "pending_payments": 25000.00,
  "recent_patients": [ /* últimos 5 pacientes */ ],
  "upcoming_appointments": [ /* próximas citas */ ]
}
```

### GET `/reports/revenue`
Reporte de ingresos por período.

**Query Parameters:**
- `period`: "day", "week", "month", "year"
- `start_date`, `end_date`: Rango personalizado

### GET `/reports/patients-stats`
Estadísticas de pacientes.

```json
{
  "total_patients": 150,
  "new_patients_month": 12,
  "patients_by_age_group": {
    "0-18": 25,
    "19-35": 45,
    "36-50": 50,
    "51+": 30
  },
  "patients_by_gender": {
    "male": 70,
    "female": 75,
    "other": 5
  }
}
```

## 🔍 Búsqueda Global

### GET `/search`
Búsqueda global en el sistema.

**Query Parameters:**
- `q`: Término de búsqueda
- `type`: "patients", "appointments", "treatments" (opcional)

```json
{
  "patients": [ /* pacientes encontrados */ ],
  "appointments": [ /* citas encontradas */ ],
  "treatments": [ /* tratamientos encontrados */ ]
}
```

## 📋 Códigos de Estado HTTP

- `200`: OK - Solicitud exitosa
- `201`: Created - Recurso creado exitosamente
- `400`: Bad Request - Error en los datos enviados
- `401`: Unauthorized - Token inválido o expirado
- `403`: Forbidden - Sin permisos para la operación
- `404`: Not Found - Recurso no encontrado
- `422`: Unprocessable Entity - Error de validación
- `500`: Internal Server Error - Error del servidor

## 🔒 Permisos por Rol

### Admin
- Acceso completo a todos los endpoints
- Gestión de usuarios
- Configuración del sistema

### Doctor
- Gestión de pacientes
- Gestión de citas propias
- Registrar tratamientos
- Ver reportes básicos

### Assistant
- Gestión de pacientes
- Ver citas
- Registrar pagos
- Reportes básicos

### Receptionist
- Gestión de citas
- Ver información de pacientes
- Registrar pagos

## 📝 Ejemplos de Uso

### Flujo típico - Nueva cita

1. **Buscar paciente**: `GET /patients?search=María`
2. **Crear cita**: `POST /appointments`
3. **Confirmar cita**: `PUT /appointments/{id}` (status: "confirmed")
4. **Completar cita**: `PUT /appointments/{id}` (status: "completed")
5. **Registrar tratamiento**: `POST /treatments`
6. **Registrar pago**: `POST /payments`

### Flujo típico - Nuevo paciente

1. **Crear paciente**: `POST /patients`
2. **Crear primera cita**: `POST /appointments`
3. **Ver resumen**: `GET /patients/{id}/summary`

---

💡 **Tip**: Usa la documentación interactiva en `/docs` para probar los endpoints directamente.