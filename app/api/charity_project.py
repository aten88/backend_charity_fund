from fastapi import APIRouter, HTTPException

from app.crud.charity_project import create_charity_project, get_project_id_by_name
from app.schemas.charity_project import CharityProjectCreate, CharityProjectDB

router = APIRouter()


@router.post(
    '/charity_project/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    response_model_exclude_defaults=True,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
):
    project_id = await get_project_id_by_name(charity_project.name)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )
    new_project = await create_charity_project(charity_project)
    return new_project
