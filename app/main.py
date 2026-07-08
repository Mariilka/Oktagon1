print("Hello, World!")
from app.db import crud
from app.db.db import SessionLocal


def display_data():
    db = SessionLocal()
    try:
        print(" СПИСОК КАТЕГОРИЙ ")
        categories = crud.get_categories(db)
        for cat in categories:
            print(f"ID: {cat.id} | Название: {cat.title}")

        print("\n СПИСОК КНИГ ")
        books = crud.get_books(db)
        for book in books:
            # Находим имя категории для наглядности вывода
            cat_name = "Неизвестно"
            for cat in categories:
                if cat.id == book.category_id:
                    cat_name = cat.title
                    break

            print(f"Книга: «{book.title}»")
            print(f"  - Цена: {book.price} руб.")
            print(f"  - Категория: {cat_name}")
            print(f"  - Описание: {book.description or 'Нет описания'}")
            print("-" * 30)

    finally:
        db.close()


if __name__ == "__main__":
    display_data()