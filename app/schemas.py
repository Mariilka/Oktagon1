from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class CategoryBase(BaseModel):
    """Базовая схема категории с общими полями."""
    title: str = Field(..., max_length=255, description="Название категории")

class CategoryCreate(CategoryBase):
    """Схема для создания новой категории (совпадает с базовой)."""
    pass

class CategoryUpdate(CategoryBase):
    """Схема для обновления категории."""
    pass

class CategoryResponse(CategoryBase):
    """Схема ответа API для категории, включает сгенерированный ID."""
    id: int

    class Config:
        # Включаем поддержку объектов SQLAlchemy (ORM моделей)
        # from_attributes работает в Pydantic v2, orm_mode — в Pydantic v1
        from_attributes = True
        orm_mode = True  



class BookBase(BaseModel):
    """Базовая схема книги со всеми основными полями."""
    title: str = Field(..., max_length=255, description="Название книги")
    description: Optional[str] = Field(None, description="Описание книги")
    price: Decimal = Field(..., ge=0, description="Цена книги (не может быть отрицательной)")
    url: Optional[str] = Field(None, max_length=500, description="Ссылка на книгу")
    category_id: int = Field(..., description="ID категории, к которой относится книга")

class BookCreate(BookBase):
    """Схема для создания новой книги (требует передачи всех базовых полей)."""
    pass

class BookUpdate(BaseModel):
    """Схема для обновления книги (все поля опциональны, обновляем только то, что передано)."""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    url: Optional[str] = Field(None, max_length=500)
    category_id: Optional[int] = None

class BookResponse(BookBase):
    """Схема ответа API для книги, включает сгенерированный ID."""
    id: int

    class Config:
        
        from_attributes = True
        orm_mode = True  
