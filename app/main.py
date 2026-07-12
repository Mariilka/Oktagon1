from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

# Импорты для работы с БД
from app.api import books, categories
from app.db import crud
from app.db.db import SessionLocal, get_db

app = FastAPI(
    title="Book & Category API",
    description="Финальная сборка приложения: управление книгами и категориями с валидацией бизнес-логики",
    version="1.3.0",
)


@app.get("/", tags=["Service"])
def read_root():
    """Корневой эндпоинт приветствия."""
    return {
        "message": "Добро пожаловать в API каталога книг! Перейдите на /docs для работы с Swagger UI."
    }


@app.get("/health", tags=["Service"])
def health_check(db: Session = Depends(get_db)):
    """Эндпоинт для проверки жизнеспособности (Health Check)."""
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Сервис и база данных работают в штатном режиме",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Сервис работает, но база данных недоступна: {str(e)}",
        )


app.include_router(categories.router)
app.include_router(books.router)


# =====================================================================
# Консольный вывод для выполнения Шага 6 и создания скриншота наставнику
# =====================================================================
def display_data():
    db = SessionLocal()
    try:
        categories_list = crud.get_categories(db)
        books_list = crud.get_books(db)

        print("\n" + "=" * 45)
        print("         === СПИСОК КАТЕГОРИЙ ===")
        print("=" * 45)
        for cat in categories_list:
            print(f"  [ID: {cat.id}] {cat.title}")

        print("\n" + "=" * 45)
        print("         === СПИСОК КНИГ ===")
        print("=" * 45)
        for book in books_list:
            cat_name = "Без категории"
            for cat in categories_list:
                if cat.id == book.category_id:
                    cat_name = cat.title
                    break

            print(f"Книга #{book.id}: «{book.title}»")
            print(f"  • Цена: {book.price} руб.")
            print(f"  • Категория: {cat_name}")
            print(f"  • Описание: {book.description or 'Нет описания'}")
            print("-" * 45)

        print("=" * 45 + "\n")
    finally:
        db.close()


if __name__ == "__main__":
    display_data()