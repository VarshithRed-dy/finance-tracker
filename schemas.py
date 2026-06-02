from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models import TransactionType

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


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
    amount: float
    type: TransactionType
    category: str
    note: Optional[str] = None
    date: datetime

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    category: Optional[str] = None
    note: Optional[str] = None
    date: Optional[datetime] = None


class TransactionResponse(TransactionCreate):
    id: int
    amount: float
    type: TransactionType
    category: str
    note: Optional[str] = None
    date: datetime
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


