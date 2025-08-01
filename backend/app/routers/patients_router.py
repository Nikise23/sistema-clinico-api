from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from ..models import Patient, PatientCreate, PatientUpdate
from ..auth import get_current_user
from ..database import get_collection


router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", response_model=Patient)
async def create_patient(
    patient_data: PatientCreate,
    current_user = Depends(get_current_user)
):
    """Create a new patient"""
    patients_collection = await get_collection("patients")
    
    # Check if patient with same DNI exists
    existing_patient = await patients_collection.find_one({"dni": patient_data.dni})
    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient with this DNI already exists"
        )
    
    # Create patient
    patient = Patient(**patient_data.dict())
    patient_dict = patient.dict()
    
    # Insert into database
    await patients_collection.insert_one(patient_dict)
    
    return patient


@router.get("/", response_model=List[Patient])
async def get_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    current_user = Depends(get_current_user)
):
    """Get all patients with pagination and search"""
    patients_collection = await get_collection("patients")
    
    # Build query
    query = {"is_active": True}
    if search:
        query["$or"] = [
            {"first_name": {"$regex": search, "$options": "i"}},
            {"last_name": {"$regex": search, "$options": "i"}},
            {"dni": {"$regex": search, "$options": "i"}},
            {"phone": {"$regex": search, "$options": "i"}}
        ]
    
    # Get patients
    cursor = patients_collection.find(query).skip(skip).limit(limit)
    patients = await cursor.to_list(length=limit)
    
    return [Patient(**patient) for patient in patients]


@router.get("/{patient_id}", response_model=Patient)
async def get_patient(
    patient_id: str,
    current_user = Depends(get_current_user)
):
    """Get a specific patient by ID"""
    patients_collection = await get_collection("patients")
    
    patient = await patients_collection.find_one({"id": patient_id, "is_active": True})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    return Patient(**patient)

@router.put("/{patient_id}", response_model=Patient)
async def update_patient(
    patient_id: str,
    patient_data: PatientUpdate,
    current_user = Depends(get_current_user)
):
    """Update a patient"""
    patients_collection = await get_collection("patients")
    
    # Check if patient exists
    existing_patient = await patients_collection.find_one({"id": patient_id, "is_active": True})
    if not existing_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Prepare update data
    update_data = {k: v for k, v in patient_data.dict().items() if v is not None}
    update_data["updated_at"] = datetime.now()
    
    # Update patient
    await patients_collection.update_one(
        {"id": patient_id},
        {"$set": update_data}
    )
    
    # Get updated patient
    updated_patient = await patients_collection.find_one({"id": patient_id})
    return Patient(**updated_patient)


@router.delete("/{patient_id}")
async def delete_patient(
    patient_id: str,
    current_user = Depends(get_current_user)
):
    """Soft delete a patient"""
    patients_collection = await get_collection("patients")
    
    # Check if patient exists
    existing_patient = await patients_collection.find_one({"id": patient_id, "is_active": True})
    if not existing_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Soft delete
    await patients_collection.update_one(
        {"id": patient_id},
        {"$set": {"is_active": False, "updated_at": datetime.now()}}
    )
    
    return {"message": "Patient deleted successfully"}


@router.get("/{patient_id}/summary")
async def get_patient_summary(
    patient_id: str,
    current_user = Depends(get_current_user)
):
    """Get patient summary with appointments and treatments"""
    patients_collection = await get_collection("patients")
    appointments_collection = await get_collection("appointments")
    treatments_collection = await get_collection("treatments")
    payments_collection = await get_collection("payments")
    
    # Get patient
    patient = await patients_collection.find_one({"id": patient_id, "is_active": True})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Get related data
    appointments = await appointments_collection.find({"patient_id": patient_id}).to_list(length=None)
    treatments = await treatments_collection.find({"patient_id": patient_id}).to_list(length=None)
    payments = await payments_collection.find({"patient_id": patient_id}).to_list(length=None)
    
    # Calculate totals
    total_treatments = len(treatments)
    total_spent = sum(payment["amount"] for payment in payments)
    upcoming_appointments = len([apt for apt in appointments if apt["appointment_date"] > datetime.now()])
    
    return {
        "patient": Patient(**patient),
        "summary": {
            "total_appointments": len(appointments),
            "upcoming_appointments": upcoming_appointments,
            "total_treatments": total_treatments,
            "total_spent": total_spent,
            "current_debt": patient.get("total_debt", 0)
        },
        "recent_treatments": treatments[-5:] if treatments else [],
        "upcoming_appointments": [apt for apt in appointments if apt["appointment_date"] > datetime.now()][:3]
    }