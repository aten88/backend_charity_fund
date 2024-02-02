from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.services.close_service import closing_process
from app.core.constants import BOOLEAN_VARIABLE


def reinvestment_process(
    new_obj: Union[CharityProject, Donation],
    open_obj: Union[CharityProject, Donation],
):
    """ Метод перераспределения сумм между Донатами/Проектами."""
    to_close_new_obj = new_obj.full_amount - new_obj.invested_amount
    to_close_open_obj = open_obj.full_amount - open_obj.invested_amount
    if to_close_new_obj <= to_close_open_obj:
        open_obj.invested_amount += to_close_new_obj
        new_obj.invested_amount += to_close_new_obj
    else:
        open_obj.invested_amount += to_close_open_obj
        to_close_new_obj -= to_close_open_obj
        new_obj.invested_amount += to_close_open_obj
    return new_obj, open_obj


async def investment_process(
    new_obj: Union[CharityProject, Donation],
    model: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    """ Метод инвестирования Донатов/Проектов. """
    all_open_objs = await session.execute(
        select(model).where(model.fully_invested == BOOLEAN_VARIABLE)
    )
    all_open_objs = all_open_objs.scalars().all()
    for open_obj in all_open_objs:
        new_obj, open_obj = reinvestment_process(new_obj, open_obj)
        if open_obj.invested_amount == open_obj.full_amount:
            open_obj = closing_process(open_obj)
        session.add(open_obj)
        if new_obj.invested_amount == new_obj.full_amount:
            new_obj = closing_process(new_obj)
            break
    session.add(new_obj)
    await session.commit()
    await session.refresh(new_obj)