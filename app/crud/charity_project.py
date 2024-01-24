from typing import Optional
from datetime import datetime, timezone

from sqlalchemy import select
from app.core.db import AsyncSessionLocal
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectCreate


async def create_charity_project(
        new_project: CharityProjectCreate
) -> CharityProject:
    """ Метод-корутина для создания обьекта CharityProject. """
    new_project_data = new_project.dict()
    new_project_data['create_date'] = datetime.now(timezone.utc)
    db_project = CharityProject(**new_project_data)
    async with AsyncSessionLocal() as session:
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
    return db_project


async def get_project_id_by_name(project_name: str) -> Optional[int]:
    """ Метод-корутина для поиска id обьекта по имени. """
    async with AsyncSessionLocal() as session:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
    return db_project_id