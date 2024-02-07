from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.crud.charity_project import project_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models import User
from app.services.investments_service import investment_process
from app.services.validators import (
    check_name, check_description, check_charity_project_exists,
    check_fully_invested, validate_full_amount, check_fully_and_invested_amounts,
)
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate
from app.schemas.donation import DonationCreate


class CharityProjectService:
    """ Сервисный класс для проектов. """

    @staticmethod
    async def create_charity_project(charity_project: CharityProjectCreate, session: AsyncSession):
        """ Метод создания проекта. """

        await check_name(charity_project.name, session)
        await check_description(charity_project.description, session)

        new_project = await project_crud.create(charity_project, session)
        await investment_process(new_project, Donation, session)
        return new_project

    @staticmethod
    async def update_charity_project(project_id: int, obj_in: CharityProjectUpdate, session: AsyncSession):
        """ Метод обновления проекта. """

        await check_charity_project_exists(project_id, session)
        charity_project = await check_fully_invested(project_id, session)

        if obj_in.name is not None:
            await check_name(obj_in.name, session)

        await validate_full_amount(obj_in.dict(exclude_unset=True), charity_project, session)

        return await project_crud.update(charity_project, obj_in, session)

    @staticmethod
    async def delete_charity_project(project_id: int, session: AsyncSession):
        """ Метод удаления проекта. """

        await check_fully_and_invested_amounts(project_id, session)
        charity_project = await check_charity_project_exists(project_id, session)

        return await project_crud.remove(charity_project, session)


class DonationService:
    """ Сервисный класс для донатов. """

    @staticmethod
    async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
    ):
        """ Метод создания доната. """
        new_donation = await donation_crud.create(
            donation, session, user
        )
        await investment_process(new_donation, CharityProject, session)

        return new_donation