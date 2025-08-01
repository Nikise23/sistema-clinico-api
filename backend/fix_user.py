#!/usr/bin/env python3
"""
Script para verificar y corregir el usuario en la base de datos
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def check_and_fix_user():
    """Verificar y corregir el usuario"""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["personal_clinic_db"]
    users_collection = db["users"]
    
    try:
        # Buscar el usuario
        user = await users_collection.find_one({"username": "nikise"})
        if user:
            print("✅ Usuario encontrado:")
            print(f"   _id: {user['_id']}")
            print(f"   username: {user['username']}")
            print(f"   email: {user['email']}")
            
            # Verificar si tiene el campo id
            if 'id' not in user:
                print("⚠️  Usuario no tiene campo 'id', agregando...")
                await users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"id": str(user["_id"])}}
                )
                print("✅ Campo 'id' agregado")
            else:
                print("✅ Usuario ya tiene campo 'id'")
        else:
            print("❌ Usuario 'nikise' no encontrado")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_and_fix_user())