from fastapi import APIRouter

from app.crud.charity_project import create_charity_project
from app.schemas.charity_project import CharityProjectCreate

router = APIRouter()


@router.post('/charity_project/')
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
):
    new_project = await create_charity_project(charity_project)
    return new_project
