from typing import Optional

from fastapi.encoders import jsonable_encoder
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

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        """ Базовый метод обновления объекта. """
        if db_obj.fully_invested:
            raise HTTPException(
                status_code=400,
                detail='Закрытый проект нельзя редактировать!'
            )
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        # if 'full_amount' in update_data and update_data['full_amount'] < db_obj.full_amount:
        #     raise HTTPException(
        #         status_code=400,
        #         detail='Предложенная сумма проекта меньше предыдущей!'
        #     )

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

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
