#!/bin/bash

# 🏥 Sistema Personal de Gestión Clínica - Script de Inicio
# Este script inicia tanto el backend como el frontend

echo "🏥 Iniciando Sistema Personal de Gestión Clínica..."
echo "=================================================="

# Verificar si MongoDB está ejecutándose
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB no está ejecutándose. Por favor, inicia MongoDB primero:"
    echo "   sudo systemctl start mongod"
    echo "   o"
    echo "   brew services start mongodb/brew/mongodb-community"
    exit 1
fi

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servidores..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ Servidores detenidos"
    exit 0
}

# Capturar señales para limpieza
trap cleanup SIGINT SIGTERM

# Iniciar Backend
echo "🚀 Iniciando Backend (FastAPI)..."
cd backend

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias si es necesario
pip install -r requirements.txt > /dev/null 2>&1

# Iniciar servidor backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "✅ Backend iniciado en http://localhost:8000"
echo "📚 Documentación API: http://localhost:8000/docs"

# Volver al directorio raíz
cd ..

# Iniciar Frontend
echo "🎨 Iniciando Frontend (React)..."
cd frontend

# Instalar dependencias si es necesario
if [ ! -d "node_modules" ]; then
echo "📦 Instalando dependencias de Node.js..."
    npm install
fi

# Iniciar servidor frontend
npm start &
FRONTEND_PID=$!

echo "✅ Frontend iniciado en http://localhost:3000"

# Mostrar información del sistema
echo ""
echo "🌐 URLs del Sistema:"
echo "   📱 Frontend:     http://localhost:3000"
echo "   🔧 Backend API:  http://localhost:8000"
echo "   📖 Docs API:     http://localhost:8000/docs"
echo ""
echo "⏹️  Para detener: Presiona Ctrl+C"
echo ""

# Esperar a que los procesos terminen
wait $BACKEND_PID $FRONTEND_PID