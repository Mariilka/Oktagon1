from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.db import get_db
from app import schemas
from app.db import crud, models

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[schemas.BookResponse])
def read_books(
    category_id: Optional[int] = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Получить список книг.
    Поддерживает фильтрацию по query-параметру: ?category_id=значение
    """
    if category_id is not None:
        # Проверяем, существует ли сама категория перед фильтрацией (бизнес-логика)
        category = crud.get_category_by_id(db, category_id=category_id)
        if not category:
            raise HTTPException(status_code=404, detail=f"Категория с ID {category_id} не существует")
        
        return db.query(models.Book).filter(models.Book.category_id == category_id).offset(skip).limit(limit).all()
        
    return crud.get_books(db, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=schemas.BookResponse)
def read_book_by_id(book_id: int, db: Session = Depends(get_db)):
    """Получить информацию о конкретной книге по её ID."""
    book = crud.get_book_by_id(db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Книга с ID {book_id} не найдена")
    return book


@router.post("/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Создать новую книгу. Валидирует существование категории."""
    # Проверка бизнес-логики: нельзя привязать книгу к несуществующей категории
    category = crud.get_category_by_id(db, category_id=book.category_id)
    if not category:
        raise HTTPException(status_code=400, detail=f"Ошибка бизнес-логики: Категория с ID {book.category_id} не существует")
    
    return crud.create_book(
        db=db,
        title=book.title,
        price=float(book.price),
        category_id=book.category_id,
        description=book.description,
        url=str(book.url) if book.url else None
    )


@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book_data: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Редактировать существующую книгу. Проверяет существование категории при её изменении."""
    update_dict = book_data.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(status_code=400, detail="Не передано ни одного поля для обновления")
    
    # Проверка бизнес-логики: если пользователь меняет категорию книги, проверяем её валидность
    if "category_id" in update_dict:
        category = crud.get_category_by_id(db, category_id=update_dict["category_id"])
        if not category:
            raise HTTPException(status_code=400, detail=f"Ошибка бизнес-логики: Категория с ID {update_dict['category_id']} не существует")

    updated_book = crud.update_book(db, book_id=book_id, **update_dict)
    if not updated_book:
        raise HTTPException(status_code=404, detail=f"Книга с ID {book_id} не найдена для обновления")
    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу по ID."""
    success = crud.delete_book(db, book_id=book_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Книга с ID {book_id} не найдена для удаления")
    return {"message": f"Книга {book_id} успешно удалена"}
