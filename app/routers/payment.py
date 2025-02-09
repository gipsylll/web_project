from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models, schemas
from app.utils import check_signature

router = APIRouter(prefix="/payments", tags=["Payments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/webhook")
def process_webhook(data: schemas.PaymentWebhook, db: Session = Depends(get_db)):
    """
    При обработке вебхука:
    - Проверить подпись
    - Проверить, есть ли у user такой account
      - Если нет - создать
    - Сохранить транзакцию
    - Начислить сумму на счёт
    """
    # Проверка подписи
    if not check_signature(
        transaction_id=data.transaction_id,
        account_id=data.account_id,
        user_id=data.user_id,
        amount=data.amount,
        given_signature=data.signature
    ):
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Ищем пользователя
    user = db.query(models.User).filter(models.User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    # Проверяем, есть ли у пользователя такой счёт
    account = db.query(models.Account).filter(
        models.Account.id == data.account_id,
        models.Account.user_id == data.user_id
    ).first()

    # Если счёта нет - создаём
    if not account:
        account = models.Account(user_id=user.id, balance=0)
        db.add(account)
        db.commit()
        db.refresh(account)

    # Проверяем уникальность transaction_id
    existing_payment = db.query(models.Payment).filter(models.Payment.transaction_id == data.transaction_id).first()
    if existing_payment:
        # Транзакция с таким ID уже была проведена
        return {"detail": "Transaction already processed"}

    # Сохраняем транзакцию
    new_payment = models.Payment(
        transaction_id=data.transaction_id,
        user_id=user.id,
        account_id=account.id,
        amount=data.amount
    )
    db.add(new_payment)

    # Начисляем сумму на баланс
    account.balance = account.balance + data.amount

    db.commit()
    db.refresh(account)
    db.refresh(new_payment)

    return {"detail": "Payment processed successfully", "payment_id": new_payment.id}