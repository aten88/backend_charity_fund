from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate


async def create_charity_project(
        new_project: CharityProjectCreate,
        session: AsyncSession,
) -> CharityProject:
    """ Метод-корутина для создания обьекта CharityProject. """
    new_project_data = new_project.dict()
    db_project = CharityProject(**new_project_data)
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


async def get_project_id_by_name(
        project_name: str,
        session: AsyncSession,
) -> Optional[int]:
    """ Метод-корутина для поиска id обьекта по имени. """
    db_project_id = await session.execute(
        select(CharityProject.id).where(
            CharityProject.name == project_name
        )
    )
    db_project_id = db_project_id.scalars().first()
    return db_project_id


async def read_all_projects_from_db(
        session: AsyncSession,
) -> list[CharityProject]:
    """ Метод-корутина для получения списка проектов. """
    db_projects = await session.execute(select(CharityProject))
    return db_projects.scalars().all()


async def get_project_by_id(
        project_id: int,
        session: AsyncSession,
) -> Optional[CharityProject]:
    """ Метод-корутина для получения проектов по id. """
    db_project = await session.execute(
        select(CharityProject).where(
            CharityProject.id == project_id
        )
    )
    db_project = db_project.scalars().first()
    return db_project


async def update_charity_project(
        db_project: CharityProject,
        project_in: CharityProjectUpdate,
        session: AsyncSession,
) -> CharityProject:
    """ Метод-корутина для обновления объектов CharityProject. """
    obj_data = jsonable_encoder(db_project)
    update_data = project_in.dict(exclude_unset=True)

    for field in obj_data:
        if field in update_data:
            setattr(db_project, field, update_data[field])
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project
