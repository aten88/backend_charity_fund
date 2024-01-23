from app.core.db import AsyncSessionLocal
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectCreate


async def create_charity_project(
        new_project: CharityProjectCreate
) -> CharityProject:
    """ Метод-корутина для создания обьекта CharityProject. """
    new_project_data = new_project.dict()

    db_project = CharityProject(**new_project_data)

    async with AsyncSessionLocal() as session:
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
    return db_project
