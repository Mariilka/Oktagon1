from app.db import crud
from app.db.db import SessionLocal, init_db


def seed_data():
    
    init_db()

    db = SessionLocal()
    try:
        
        python_category = crud.create_category(db, title="Программирование на Python")
        db_category = crud.create_category(db, title="Базы данных и SQL")

        print("Категории успешно добавлены!")

        
        crud.create_book(
            db,
            title="Изучаем Python",
            price=1200.50,
            category_id=python_category.id,
            description="Легендарное руководство Марка Лутца.",
            url="https://example.com/lutsubook",
        )
        crud.create_book(
            db,
            title="Чистый Python",
            price=850.00,
            category_id=python_category.id,
            description="Трюки для эффективного программирования от Дэна Бейдера.",
        )

        
        crud.create_book(
            db,
            title="Понимая SQL",
            price=950.00,
            category_id=db_category.id,
            description="Отличное практическое руководство для новичков.",
        )
        crud.create_book(
            db,
            title="PostgreSQL. Основы",
            price=1500.00,
            category_id=db_category.id,
            description="Подробный разбор архитектуры и возможностей СУБД.",
        )

        print("Тестовые книги успешно добавлены!")

    except Exception as e:
        print(f"Произошла ошибка при заполнении: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()