from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc

from app.models.donation import Donation


async def get_free_donations(session: AsyncSession):
    """ Метод поиска нераспределенных пожертвований. """
    free_donations = await session.execute(
        select(Donation)
        .where(Donation.fully_invested == 0)
        .order_by(asc(Donation.create_date))
    )
    free_donations = free_donations.scalars().all()
    return free_donations


async def investing_process(new_project, donations, session: AsyncSession):
    remaining_difference = 0
    for donation in donations:
        if new_project.fully_invested == 1:
            break

        remaining_amount = new_project.full_amount - (new_project.invested_amount + remaining_difference)

        if donation.full_amount == new_project.full_amount:
            new_project.invested_amount = donation.full_amount
            new_project.fully_invested = 1
            new_project.close_date = datetime.now(timezone.utc)

            donation.invested_amount = donation.full_amount
            donation.fully_invested = 1
            donation.close_date = datetime.now(timezone.utc)

        elif donation.full_amount > remaining_amount:
            difference = donation.full_amount - remaining_amount
            new_project.invested_amount = donation.full_amount - difference
            new_project.fully_invested = 1
            new_project.close_date = datetime.now(timezone.utc)
            donation.invested_amount = donation.full_amount - difference

        else:
            new_project.invested_amount += donation.full_amount
            donation.invested_amount = donation.full_amount

        if new_project.invested_amount >= new_project.full_amount:
            new_project.fully_invested = 1
            new_project.close_date = datetime.now(timezone.utc)

        session.add(new_project)
        session.add(donation)

    await session.commit()
    await session.refresh(new_project)
    return new_project