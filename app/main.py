from fastapi import FastAPI
from app.routers import auth, admin, user, payment

def create_app() -> FastAPI:
    app = FastAPI(title="Payment Service")

    # Подключаем роутеры
    app.include_router(auth.router)
    app.include_router(admin.router)
    app.include_router(user.router)
    app.include_router(payment.router)

    return app

app = create_app()