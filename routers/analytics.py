from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from database import get_db
from models import User, Transaction
from auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"]) #This router will handle all analytics related endpoints.

@router.get("/summary")
def get_summary(
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    year: int = Query(..., ge=2000, description="Year (e.g., 2025)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).filter(
        extract("month", Transaction.date) == month,
        extract("year", Transaction.date) == year
    )

    total_income = transactions.filter(Transaction.type == "income").with_entities(func.sum(Transaction.amount)).scalar() or 0
    total_expense = transactions.filter(Transaction.type == "expense").with_entities(func.sum(Transaction.amount)).scalar() or 0


    return {
        "month": month,
        "year": year,
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": total_income - total_expense
    }



@router.get("/category-breakdown")
def get_category_breakdown(
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    year: int = Query(..., ge=2000, description="Year (e.g., 2025)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transactions = db.query(Transaction.category,
    Transaction.type,
    func.sum(Transaction.amount).label("total_amount")).filter(
        Transaction.user_id == current_user.id,
        extract("month", Transaction.date) == month,
        extract("year", Transaction.date) == year
    ).group_by(Transaction.category, Transaction.type).all()

    return {{"category": t.category, "type": t.type, "total_amount": t.total_amount} for t in transactions}


@router.get("/trends")
def get_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transactions = db.query(
        extract("year", Transaction.date).label("year"),
        extract("month", Transaction.date).label("month"),
        Transaction.type,
        func.sum(Transaction.amount).label("total_amount")
    ).filter(Transaction.user_id == current_user.id
    ).group_by("year", "month", Transaction.type
    ).order_by("year", "month").all()

    return {{"year" : t.year, "month": t.month, "type": t.type, "total": t.total_amount} for t in transactions}

    



