#!/usr/bin/env python3
"""
Script para crear un usuario de prueba en la base de datos
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_test_user():
    """Crear usuario de prueba"""
    # Conectar a MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["personal_clinic_db"]
    users_collection = db["users"]
    
    # Datos del usuario de prueba
    test_user = {
        "email": "nikise@test.com",
        "username": "nikise",
        "first_name": "Nikise",
        "last_name": "Test",
        "role": "admin",
        "phone": "123456789",
        "hashed_password": pwd_context.hash("admin123"),
        "is_verified": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    try:
        # Verificar si el usuario ya existe
        existing_user = await users_collection.find_one({"username": "nikise"})
        if existing_user:
            print("✅ Usuario 'nikise' ya existe en la base de datos")
            print(f"   Usuario: nikise")
            print(f"   Contraseña: admin123")
            return
        
        # Insertar usuario
        result = await users_collection.insert_one(test_user)
        print("✅ Usuario de prueba creado exitosamente!")
        print(f"   Usuario: nikise")
        print(f"   Contraseña: admin123")
        print(f"   ID: {result.inserted_id}")
        
    except Exception as e:
        print(f"❌ Error creando usuario: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_test_user())