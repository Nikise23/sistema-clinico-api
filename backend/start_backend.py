#!/usr/bin/env python3
"""
Script simplificado para iniciar el backend
"""
import uvicorn
import os

if __name__ == "__main__":
    print("🚀 Iniciando backend...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )