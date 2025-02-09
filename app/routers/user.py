from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from fastapi.security import OAuth2PasswordBearer

from app.database import SessionLocal
from app import models, schemas, security
from app.schemas import UserOut, AccountOut, PaymentOut

router = APIRouter(prefix="/user", tags=["User"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    token_data = security.decode_access_token(token)
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@router.get("/me", response_model=UserOut)
def get_user_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.get("/accounts", response_model=List[AccountOut])
def get_my_accounts(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Получаем все счета текущего пользователя
    accounts = db.query(models.Account).filter(models.Account.user_id == current_user.id).all()
    return accounts

@router.get("/payments", response_model=List[PaymentOut])
def get_my_payments(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    payments = db.query(models.Payment).filter(models.Payment.user_id == current_user.id).all()
    return payments