from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.api.validators import charity_project_validators
from app.services.investments_service import investment_process
from app.models.donation import Donation
from app.core.user import current_superuser


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    response_model_exclude_defaults=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """ Только для суперюзеров.

        Создает благотворительный проект.
    """
    await charity_project_validators.validate_create(charity_project, session)

    new_project = await project_crud.create(charity_project, session)
    await investment_process(new_project, Donation, session)

    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """ Получает список всех проектов. """
    all_projects = await project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """ Только для суперюзеров.

        Закрытый проект нельзя редактировать, также нельзя установить требуемую сумму меньше уже вложенной.
    """
    charity_project = await charity_project_validators.validate_update(project_id, obj_in, session)

    charity_project = await project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """ Только для суперюзеров.

        Удаляет проект. Нельзя удалить проект, в который уже были инвестированы средства, его можно только закрыть.
    """

    charity_project = await charity_project_validators.validate_delete(project_id, session)

    charity_project = await project_crud.remove(
        charity_project, session
    )
    return charity_project
