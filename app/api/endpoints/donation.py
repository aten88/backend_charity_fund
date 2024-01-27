from fastapi import APIRouter, Depends  # HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationUserDB,
)
# from app.models.donation import Donation

router = APIRouter(
    prefix='/donation',
    tags=['Donation'])


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude_defaults=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """ Метод создания доната. """

    new_donation = await donation_crud.create(donation, session)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """ Метод получения списка донатов. """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationUserDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """ Метод получения списка донатов. """
    all_donations = await donation_crud.get_donations_by_user(session)
    return all_donations