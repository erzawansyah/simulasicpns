from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from uuid import UUID


class UserStatus(str, Enum):
    NEW = "NEW"
    RETURNED = "RETURNED"
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"
    DELETED = "DELETED"


class User(BaseModel):
    created_at: Optional[str] = None
    id: Optional[UUID] = None
    username: str
    telegram_id: int
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    status: UserStatus = UserStatus.NEW
