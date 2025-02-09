from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models, schemas, security

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.LoginSchema, db: Session = Depends(get_db)):
    # Ищем пользователя по email
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Проверяем пароль
    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Создаём JWT
    token_data = {
        "user_id": user.id,
        "is_admin": user.is_admin
    }
    access_token = security.create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}