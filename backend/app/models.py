from datetime import datetime, date
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
import uuid


def generate_id():
    return str(uuid.uuid4())


# ===============================
# ENUMS
# ===============================

class UserRole(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    ASSISTANT = "assistant"
    RECEPTIONIST = "receptionist"


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PARTIAL = "partial"
    COMPLETED = "completed"
    OVERDUE = "overdue"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
   


class TreatmentType(str, Enum):
    CONSULTATION = "consultation"
    CLEANING = "cleaning"
    FILLING = "filling"
    EXTRACTION = "extraction"
    ROOT_CANAL = "root_canal"
    CROWN = "crown"
    BRIDGE = "bridge"
    IMPLANT = "implant"
    ORTHODONTICS = "orthodontics"
    OTHER = "other"


# ===============================
# BASE MODELS
# ===============================

class BaseDocument(BaseModel):
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)


# ===============================
# USER MODELS
# ===============================

class User(BaseDocument):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role: UserRole
    phone: Optional[str] = None
    hashed_password: str
    is_verified: bool = False
    last_login: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role: UserRole
    phone: Optional[str] = None
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    first_name: str
    last_name: str
    role: UserRole
    phone: Optional[str] = None
    is_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime


# ===============================
# PATIENT MODELS
# ===============================

class Patient(BaseDocument):
    # Información personal
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    dni: str
    email: Optional[EmailStr] = None
    phone: str
    
    # Dirección
    address: str
    city: str
    state: str
    postal_code: str
    country: str = "Argentina"
    
    # Información médica
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    
    # Información del seguro
    insurance_provider: Optional[str] = None
    insurance_number: Optional[str] = None
    
    # Estado financiero
    total_debt: float = 0.0
    notes: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    dni: str
    email: Optional[EmailStr] = None
    phone: str
    address: str
    city: str
    state: str
    postal_code: str
    country: str = "Argentina"
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_number: Optional[str] = None
    notes: Optional[str] = None


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_number: Optional[str] = None
    notes: Optional[str] = None

# ===============================
# APPOINTMENT MODELS
# ===============================

class Appointment(BaseDocument):
    patient_id: str
    doctor_id: str
    appointment_date: datetime
    duration_minutes: int = 60
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    treatment_type: TreatmentType
    notes: Optional[str] = None
    cost: Optional[float] = None
    reminder_sent: bool = False

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_date: datetime
    duration_minutes: int = 60
    treatment_type: TreatmentType
    notes: Optional[str] = None
    cost: Optional[float] = None


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: Optional[AppointmentStatus] = None
    treatment_type: Optional[TreatmentType] = None
    notes: Optional[str] = None
    cost: Optional[float] = None


# ===============================
# TREATMENT MODELS
# ===============================

class Treatment(BaseDocument):
    patient_id: str
    doctor_id: str
    appointment_id: Optional[str] = None
    treatment_type: TreatmentType
    description: str
    date_performed: datetime
    cost: float
    notes: Optional[str] = None
    teeth_involved: Optional[List[int]] = None  # Números de dientes involucrados

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TreatmentCreate(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_id: Optional[str] = None
    treatment_type: TreatmentType
    description: str
    date_performed: datetime
    cost: float
    notes: Optional[str] = None
    teeth_involved: Optional[List[int]] = None

# ===============================
# PAYMENT MODELS
# ===============================

class Payment(BaseDocument):
    patient_id: str
    appointment_id: Optional[str] = None
    treatment_id: Optional[str] = None
    amount: float
    payment_date: datetime
    payment_method: str  # "cash", "card", "transfer", etc.
    status: PaymentStatus = PaymentStatus.COMPLETED
    notes: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PaymentCreate(BaseModel):
    patient_id: str
    appointment_id: Optional[str] = None
    treatment_id: Optional[str] = None
    amount: float
    payment_date: datetime
    payment_method: str
    notes: Optional[str] = None


# ===============================
# TOKEN MODELS
# ===============================
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponse


class TokenData(BaseModel):
    username: Optional[str] = None