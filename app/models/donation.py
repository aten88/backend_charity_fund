from datetime import datetime, timezone

from sqlalchemy import (
    Column, Text, Integer,
    Boolean, DateTime,
    ForeignKey,
)

from app.core.db import Base


class Donation(Base):
    """ Модель пожертвований. """
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, default=datetime.now(timezone.utc))
    close_date = Column(DateTime)
