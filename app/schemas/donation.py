from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.core.constants import MIN_LEN_FIELD


class DonationBase(BaseModel):
    """ Основа для схем пожертвования. """
    full_amount: int
    comment: str = Optional[Field(None, min_length=MIN_LEN_FIELD)]

    @validator('full_amount')
    def check_full_amount(cls, value):
        if value <= 0:
            raise ValueError('Поле full_amount должно быть больше 0')
        return value


class DonationCreate(DonationBase):
    """ Схема для создания пожертвования. """
    pass


class DonationDB(DonationBase):
    """ Схема для получения пожертвования из БД. """
    comment: str = Field(..., min_length=MIN_LEN_FIELD)
    id: int
    create_date: datetime
    user_id: str
    invested_amount: int
    fully_invested: bool
    close_date: datetime

    class Config:
        orm_mode = True


class DonationUserDB(DonationBase):
    """ Схема для получения пожертвования юзера из БД. """
    comment: str = Field(..., min_length=MIN_LEN_FIELD)
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
