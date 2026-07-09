from sqlalchemy.orm import Session
from app.db import models

def create_category(db: Session, title: str) -> models.Category:
    category = models.Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def get_category_by_id(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def update_category(db: Session, category_id: int, new_title: str):
    category = get_category_by_id(db, category_id)
    if category:
        category.title = new_title
        db.commit()
        db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> bool:
    category = get_category_by_id(db, category_id)
    if category:
        db.delete(category)
        db.commit()
        return True
    return False


def create_book(
    db: Session,
    title: str,
    price: float,
    category_id: int,
    description: str = None,
    url: str = None,
) -> models.Book:
    book = models.Book(
        title=title,
        price=price,
        category_id=category_id,
        description=description,
        url=url,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, **kwargs):
    book = get_book_by_id(db, book_id)
    if book:
        for key, value in kwargs.items():
            if hasattr(book, key) and value is not None:
                setattr(book, key, value)
        db.commit()
        db.refresh(book)
    return book

def delete_book(db: Session, book_id: int) -> bool:
    book = get_book_by_id(db, book_id)
    if book:
        db.delete(book)
        db.commit()
        return True
    return False