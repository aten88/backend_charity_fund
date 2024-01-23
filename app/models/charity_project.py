from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, func

from app.constants import INVESTED_AMOUNT_START
from app.core.db import Base


class CharityProject(Base):
    """ Модель проектов. """
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)  # не менее одного символа проверить... можно реализовать через валидатор
    full_amount = Column(Integer, nullable=False)  # больше 0 проверить, можно реализовать через валидатор
    invested_amount = Column(Integer, nullable=False, default=INVESTED_AMOUNT_START)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=func.now())
    close_date = Column(DateTime, nullable=False)  # проставляется автоматически в момент набора нужной суммы нужно сделать
