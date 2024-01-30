from datetime import datetime
from typing import Union

from app.models import CharityProject, Donation


def closing_process(obj: Union[CharityProject, Donation]) -> Union[CharityProject, Donation]:
    """ Закрывает проект/донат публикует дату закрытия. """
    if obj.full_amount == obj.invested_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()
    return obj