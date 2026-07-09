print("Hello, World!")
from app.db.db import init_db
from app.db import models  # <-- Именно эта строка говорит SQLAlchemy, какие таблицы нужно создать!

if __name__ == "__main__":
    init_db()
    print("Таблицы успешно созданы!")