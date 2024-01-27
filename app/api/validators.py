from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.models.charity_project import CharityProject


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
