from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class TransactionType(str, enum.Enum): #This is to ensure that the transaction type is either income or expense
    income = "income"
    expense = "expense"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) #It's .utcnow - The function reference not the function call
    transactions = relationship("Transaction", back_populates="owner") #This is a relationship that allows us to access the transactions of a user, back_populates means transactions will have a back reference to the user called "owner".

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(String, nullable=False)
    note = Column(String, nullable=True)
    date = Column(DateTime, nullable=False) # date is when transaction actually happened
    created_at = Column(DateTime, default=datetime.utcnow) # created_at is when transaction was created in db
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="transactions")


