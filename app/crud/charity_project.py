from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):
    """ Класс CRUD для работы с CharityProject. """

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """ Метод для поиска id обьекта по имени. """
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        """ Переопределенный метод удаления объекта. """
        if db_obj.fully_invested or db_obj.invested_amount > 0:
            raise HTTPException(
                status_code=400,
                detail='В проект были внесены средства, не подлежит удалению!'
            )
        await session.delete(db_obj)
        await session.commit()
        return db_obj


project_crud = CRUDCharityProject(CharityProject)
