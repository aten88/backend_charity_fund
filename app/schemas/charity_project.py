from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator

from app.core.constants import MAX_LEN_FIELD


class CharityProjectBase(BaseModel):
    """ Основа для схем проекта. """
    name: str = Field(
        None,
        max_length=MAX_LEN_FIELD
    )
    description: str = Field(
        None,
        max_length=MAX_LEN_FIELD
    )
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    """ Схема для создания обьекта CharityProject. """
    name: str = Field(..., max_length=MAX_LEN_FIELD)
    description: str = Field(...,)


class CharityProjectDB(CharityProjectBase):
    """ Схема получения данных из БД. """
    name: str = Field(..., max_length=MAX_LEN_FIELD)
    description: str = Field(...,)
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    """ Схема для обновления обьекта CharityProject. """
    full_amount: Optional[PositiveInt]
    description: str = Field(None,)

    @validator('name')
    def name_cannot_be_null(cls, value):
        """ Валидатор поля name. """
        if value is None:
            raise ValueError('Имя проекта не может быть пустым.')
        return value
