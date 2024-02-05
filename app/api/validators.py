from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """ Метод для проверки имени проекта на дубликаты. """
    if not project_name:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Имя проекта не может быть пустым'
        )
    project_id = await project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_description(
        project_descrition: str,
        session: AsyncSession,
) -> None:
    """ Метод проверки описания проекта. """
    if not project_descrition:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Описание проекта не может быть пустым!'
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
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект с таким id не найден!'
        )
    return charity_project


async def check_fully_invested(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await project_crud.get(
        project_id, session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    return charity_project


async def validate_full_amount(update_data, db_obj, session: AsyncSession):
    """ Метод-валидатор для проверки full_amount. """
    if 'full_amount' in update_data and update_data['full_amount'] < db_obj.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Сумма проекта не может быть меньше инвестированной суммы!'
        )


async def check_fully_and_invested_amounts(project_id: int, session) -> CharityProject:
    charity_project = await project_crud.get(project_id, session)
    if charity_project.fully_invested or charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
