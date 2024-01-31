from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime

from app.core.constants import INVESTED_AMOUNT_START
from app.core.db import Base


class CharityProject(Base):
    """ Модель проектов. """
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=INVESTED_AMOUNT_START)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, default=datetime.now(timezone.utc))
    close_date = Column(DateTime)
