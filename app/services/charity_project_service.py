from app.crud.charity_project import project_crud
from app.models.donation import Donation
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.validators import (
    check_name, check_description, check_charity_project_exists,
    check_fully_invested, validate_full_amount, check_fully_and_invested_amounts,
)


class CharityProjectService:
    """ Сервисный класс для проектов. """

    @staticmethod
    async def create_charity_project(charity_project: CharityProjectCreate, session: AsyncSession):
        """ Метод создания проекта. """

        await check_name(charity_project.name, session)
        await check_description(charity_project.description, session)

        return await project_crud.create(charity_project, Donation, session)

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
