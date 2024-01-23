from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CharityProjectCreate(BaseModel):
    """ Схема для создания обьекта CharityProject. """
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
