import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import auth_router, patients_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


# Create FastAPI app
app = FastAPI(
    title="🏥 Sistema Personal de Gestión Clínica",
    description="Sistema moderno y personalizado para la gestión de consultorios médicos y odontológicos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth_router.router, prefix="/api")
app.include_router(patients_router.router, prefix="/api")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🏥 Sistema Personal de Gestión Clínica",
        "version": "1.0.0",
        "status": "🟢 Online",
        "docs": "/docs"
    }


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }

# API info
@app.get("/api")
async def api_info():
    """API information"""
    return {
        "message": "🔥 API Personal de Gestión Clínica",
        "endpoints": {
            "authentication": "/api/auth",
            "patients": "/api/patients",
            "documentation": "/docs"
        },
        "features": [
            "👥 Gestión de Pacientes",
            "🔐 Autenticación JWT",
            "📅 Sistema de Citas",
            "💰 Control de Pagos",
            "📊 Reportes y Estadísticas"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )