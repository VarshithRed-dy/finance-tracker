from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from models import TransactionType

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  #Allows Pydantic to read fields from SQLAlchemy objects.

class Token(BaseModel):
    access_token: str #The jwt string
    token_type: str #Always "bearer"

class TransactionCreate(BaseModel): # user_id is not included as it will be derived from the token
    amount: float = Field(gt=0, description="Amount must be positive")
    type: TransactionType
    category: str = Field(min_length=3, max_length=50)
    note: Optional[str] = Field(None, max_length=255)
    date: datetime

class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    category: Optional[str] = Field(None, min_length=3, max_length=50)
    note: Optional[str] = Field(None, max_length=255)
    date: Optional[datetime] = None


class TransactionResponse(TransactionCreate):
    id: int
    created_at: datetime
    user_id: int 

    class Config:
        from_attributes = True

class TransactionListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[TransactionResponse]


