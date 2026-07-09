from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

# Импортируем роутеры из папки api
from app.api import books, categories
# Импортируем генератор сессий для проверки соединения
from app.db.db import get_db

app = FastAPI(
    title="Book & Category API",
    description="Финальная сборка приложения: управление книгами и категориями с валидацией бизнес-логики",
    version="1.3.0"
)


@app.get("/", tags=["Service"])
def read_root():
    """Корневой эндпоинт приветствия."""
    return {"message": "Добро пожаловать в API каталога книг! Перейдите на /docs для работы с Swagger UI."}


@app.get("/health", tags=["Service"])
def health_check(db: Session = Depends(get_db)):
    """
    Эндпоинт для проверки жизнеспособности (Health Check).
    Проверяет не только работу самого FastAPI, но и делает тестовый запрос в PostgreSQL.
    """
    try:
        # Выполняем легковесный сырой запрос для проверки коннекта с базой данных
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Сервис и база данных работают в штатном режиме"
        }
    except Exception as e:
        # Если база данных лежит или не отвечает, возвращаем ошибку 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Сервис работает, но база данных недоступна: {str(e)}"
        )



app.include_router(categories.router)
app.include_router(books.router)
