import hashlib

from app.config import settings

def generate_signature(transaction_id: str, account_id: int, user_id: int, amount, secret_key: str) -> str:
    """
    Формируем sha256-хеш из конкатенации (account_id, amount, transaction_id, user_id, secret_key) 
    в алфавитном порядке ключей: account_id, amount, transaction_id, user_id, secret_key.
    """
    data_str = f"{account_id}{amount}{transaction_id}{user_id}{secret_key}"
    return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

def check_signature(transaction_id: str, account_id: int, user_id: int, amount, given_signature: str) -> bool:
    secret_key = settings.SIGNATURE_SECRET_KEY
    expected_signature = generate_signature(
        transaction_id=transaction_id,
        account_id=account_id,
        user_id=user_id,
        amount=amount,
        secret_key=secret_key
    )
    return expected_signature == given_signature