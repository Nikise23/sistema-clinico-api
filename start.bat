@echo off
echo 🏥 Iniciando Sistema Personal de Gestión Clínica...
echo ==================================================

REM Verificar si MongoDB está ejecutándose
echo ⚡ Verificando MongoDB...
tasklist /FI "IMAGENAME eq mongod.exe" 2>NUL | find /I /N "mongod.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo ⚠️  MongoDB no está ejecutándose. 
    echo    Por favor, inicia MongoDB primero desde MongoDB Compass
    echo    o ejecuta: net start MongoDB
    pause
    exit /b 1
)

echo ✅ MongoDB está ejecutándose

REM Iniciar Backend
echo 🚀 Iniciando Backend (FastAPI)...
cd backend

REM Verificar si el entorno virtual existe
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Instalar dependencias
echo 📦 Instalando dependencias...
pip install -r requirements.txt >nul 2>&1

REM Iniciar servidor backend en segundo plano
echo ✅ Iniciando servidor backend...
start /b uvicorn main:app --reload --host 0.0.0.0 --port 8000

echo ✅ Backend iniciado en http://localhost:8000
echo 📚 Documentación API: http://localhost:8000/docs

REM Volver al directorio raíz
cd ..

REM Iniciar Frontend
echo 🎨 Iniciando Frontend (React)...
cd frontend

REM Instalar dependencias si es necesario
if not exist "node_modules" (
    echo 📦 Instalando dependencias de Node.js...
    npm install
)

echo ✅ Iniciando servidor frontend...

REM Mostrar información del sistema
echo.
echo 🌐 URLs del Sistema:
echo    📱 Frontend:     http://localhost:3000
echo    🔧 Backend API:  http://localhost:8000
echo    📖 Docs API:     http://localhost:8000/docs
echo.
echo ⏹️  Para detener: Cierra esta ventana
echo.

REM Iniciar servidor frontend (esto mantendrá la ventana abierta)
npm start

pause