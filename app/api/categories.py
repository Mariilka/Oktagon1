from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.db import get_db
from app import schemas
from app.db import crud

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[schemas.CategoryResponse])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех категорий."""
    return crud.get_categories(db, skip=skip, limit=limit)


@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def read_category_by_id(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по её ID. Возвращает 404, если она не найдена."""
    category = crud.get_category_by_id(db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail=f"Категория с ID {category_id} не найдена")
    return category


@router.post("/", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию (возвращает статус 201 Created)."""
    return crud.create_category(db, title=category.title)


@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(category_id: int, category_data: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    """Обновить существующую категорию по ID. Возвращает 404, если она не найдена."""
    updated_category = crud.update_category(db, category_id=category_id, new_title=category_data.title)
    if not updated_category:
        raise HTTPException(status_code=404, detail=f"Категория с ID {category_id} не найдена для обновления")
    return updated_category


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию по ID. Возвращает 404, если объект отсутствует."""
    success = crud.delete_category(db, category_id=category_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Категория с ID {category_id} не найдена для удаления")
    return {"message": f"Категория {category_id} успешно удалена"}
