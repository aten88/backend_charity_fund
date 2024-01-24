from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.core.constants import MIN_LEN_FIELD, MAX_LEN_FIELD


class CharityProjectBase(BaseModel):
    name: str = Field(
        None,
        min_length=MIN_LEN_FIELD,
        max_length=MAX_LEN_FIELD
    )
    description: str = Field(None, min_length=MIN_LEN_FIELD)
    full_amount: int

    @validator('full_amount')
    def check_full_amount(cls, value):
        if value <= 0:
            raise ValueError('Поле full_amount должно быть больше 0')
        return value


class CharityProjectCreate(CharityProjectBase):
    """ Схема для создания обьекта CharityProject. """
    name: str = Field(
        ...,
        min_length=MIN_LEN_FIELD,
        max_length=MAX_LEN_FIELD
    )
    description: str = Field(..., min_length=MIN_LEN_FIELD)


class CharityProjectDB(CharityProjectBase):
    """Схема получения данных из БД. """
    name: str = Field(
        ...,
        min_length=MIN_LEN_FIELD,
        max_length=MAX_LEN_FIELD
    )
    description: str = Field(..., min_length=MIN_LEN_FIELD)
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
