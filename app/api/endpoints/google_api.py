from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends

from app.core.google_client import get_service
from app.core.user import current_superuser
from app.services.projects_donats_services import CharityProjectService

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    wrapper_services: Aiogoogle = Depends(get_service),
    get_projects: CharityProjectService = Depends(),
):
    """
    Только для суперюзеров.

    Создает отчет о скорости закрытия проектов.
    """
    projects = await get_projects.get_projects_by_completion_rate()
    return projects
