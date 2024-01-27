from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.models.charity_project import CharityProject

router = APIRouter(
    prefix='/charity_project',
    tags=['сharity projects'])


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    response_model_exclude_defaults=True,
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """ Метод создания проекта. """
    await check_name_duplicate(charity_project.name, session)

    new_project = await project_crud.create(charity_project, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """ Метод получения списка проектов. """
    all_projects = await project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """ Метод обновления проекта. """
    charity_project = await check_charity_project_exists(project_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    charity_project = await project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """ Метод удаления проекта. """
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    charity_project = await project_crud.remove(
        charity_project, session
    )
    return charity_project


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """ Метод для проверки имени проекта на дубликаты. """
    project_id = await project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """ Метод проверки на наличие объекта в БД. """
    charity_project = await project_crud.get(
        project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект с таким id не найден!'
        )
    return charity_project
