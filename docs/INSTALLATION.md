# 📦 Guía de Instalación - Sistema Personal de Gestión Clínica

## 📋 Requisitos Previos

### Sistema Operativo
- **Linux/macOS/Windows** con WSL2
- **Python 3.8+**
- **Node.js 16+** y **npm/yarn**
- **MongoDB 4.4+**

### Herramientas Necesarias
```bash
# Verificar versiones
python --version  # >= 3.8
node --version    # >= 16
npm --version     # >= 8
mongod --version  # >= 4.4
```

## 🚀 Instalación Rápida

### 1. Clonar/Descargar el Proyecto
```bash
# Si tienes el proyecto en Git
git clone https://github.com/tu-usuario/personal-clinic-system.git
cd personal-clinic-system

# O si descargaste el ZIP
cd personal-clinic-system
```

### 2. Configurar MongoDB
```bash
# Ubuntu/Debian
sudo systemctl start mongod
sudo systemctl enable mongod

# macOS con Homebrew
brew services start mongodb/brew/mongodb-community

# Windows
# Instalar MongoDB desde: https://www.mongodb.com/try/download/community

### 3. Ejecutar Script de Inicio Automático
```bash
./start.sh
```

¡Eso es todo! El script se encarga de:
- ✅ Crear entornos virtuales
- ✅ Instalar dependencias
- ✅ Iniciar ambos servidores
- ✅ Mostrar URLs del sistema

## 🔧 Instalación Manual

### Backend (FastAPI)
```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Ejecutar servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (React)
```bash
cd frontend

# Instalar dependencias
npm install
# Configurar variables de entorno
cp .env.example .env
# Editar .env si es necesario

# Ejecutar servidor de desarrollo
npm start
```

## 🌐 URLs del Sistema

Una vez instalado:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Redoc API**: http://localhost:8000/redoc

## 👤 Primer Usuario

Para crear tu primer usuario administrador:

```bash
# Opción 1: Usar la API directamente
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@clinica.com",
    "username": "admin",
    "first_name": "Admin",
    "last_name": "Sistema",
    "role": "admin",
    "password": "admin123"
  }'

# Opción 2: Usar la interfaz web
# Ve a http://localhost:3000 y haz clic en "Registrarse"
```

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

## 🔧 Configuración Avanzada

### Variables de Entorno - Backend
```bash
# backend/.env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=personal_clinic_db
SECRET_KEY=tu-clave-secreta-super-segura
ACCESS_TOKEN_EXPIRE_MINUTES=43200
DEBUG=true
```

### Variables de Entorno - Frontend
```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_APP_NAME=Sistema Personal de Gestión Clínica
```

## 🐳 Docker (Opcional)

```bash
# Construcción y ejecución con Docker Compose
docker-compose up -d

# URLs con Docker
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# MongoDB: localhost:27017
```

## 🔍 Solución de Problemas

### Error: MongoDB no conecta
```bash
# Verificar estado de MongoDB
sudo systemctl status mongod

# Reiniciar MongoDB
sudo systemctl restart mongod
```

## Error: Puerto ya en uso
```bash
# Buscar proceso usando el puerto
sudo lsof -i :8000  # Backend
sudo lsof -i :3000  # Frontend

# Matar proceso
sudo kill -9 PID
```

### Error: Dependencias de Python
```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: Dependencias de Node.js
```bash
# Limpiar cache
npm cache clean --force

# Eliminar node_modules y reinstalar
rm -rf node_modules package-lock.json
npm install
```

## 📚 Próximos Pasos

1. **Configurar tu clínica**: Agrega información de tu consultorio
2. **Crear usuarios**: Doctores, asistentes, recepcionistas
3. **Importar pacientes**: Si tienes datos existentes
4. **Personalizar**: Modifica colores, logos, etc.

## 🆘 Soporte
Si tienes problemas:

1. Revisa los logs en la consola
2. Verifica que todos los servicios estén ejecutándose
3. Consulta la documentación de la API en `/docs`
4. Revisa este archivo de instalación nuevamente

---

💡 **Tip**: Usa el script `start.sh` para un inicio rápido y automático del sistema.