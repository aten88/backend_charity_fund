from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate


class CharityProjectValidators:
    """ Класс-валидатор. """
    @classmethod
    async def validate_create(cls, charity_project: CharityProjectCreate, session: AsyncSession):
<<<<<<< HEAD
=======
        """ Набор валидаторов для create. """
>>>>>>> 8aec13e86ea63d76eed1bb1c1f9204645d631f2b
        await cls.check_name(charity_project.name, session)
        await cls.check_description(charity_project.description, session)

    @classmethod
    async def validate_update(
        cls, project_id: int, obj_in: CharityProjectUpdate, session: AsyncSession
    ):
<<<<<<< HEAD
=======
        """ Набор валидаторов для update. """
>>>>>>> 8aec13e86ea63d76eed1bb1c1f9204645d631f2b
        await cls.check_charity_project_exists(project_id, session)
        charity_project = await cls.check_fully_invested(project_id, session)

        if obj_in.name is not None:
            await cls.check_name(obj_in.name, session)

        await cls.validate_full_amount(obj_in.dict(exclude_unset=True), charity_project, session)
        return charity_project

    @classmethod
    async def validate_delete(cls, project_id: int, session: AsyncSession):
<<<<<<< HEAD
=======
        """ Набор валидаторов для delete. """
>>>>>>> 8aec13e86ea63d76eed1bb1c1f9204645d631f2b
        await cls.check_fully_and_invested_amounts(project_id, session)
        charity_project = await cls.check_charity_project_exists(project_id, session)
        return charity_project

    @staticmethod
    async def check_name(project_name: str, session: AsyncSession):
<<<<<<< HEAD
=======
        """ Валидатор проверки имени. """
>>>>>>> 8aec13e86ea63d76eed1bb1c1f9204645d631f2b
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

    @staticmethod
    async def check_description(project_description: str, session: AsyncSession):
<<<<<<< HEAD
=======
        """ Валидатор для проверки описания. """
>>>>>>> 8aec13e86ea63d76eed1bb1c1f9204645d631f2b
        if not project_description:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Описание проекта не может быть пустым!'
            )

    @staticmethod
    async def check_charity_project_exists(project_id: int, session: AsyncSession):
<<<<<<< HEAD
=======
        """ Проверяет наличие проекта. """
>>>>>>> 8aec13e86ea63d76eed1bb1c1f9204645d631f2b
        charity_project = await project_crud.get(project_id, session)
        if charity_project is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Проект с таким id не найден!'
            )
        return charity_project

    @staticmethod
    async def check_fully_invested(project_id: int, session: AsyncSession):
<<<<<<< HEAD
=======
        """ Проверяет поле full_invested. """
>>>>>>> 8aec13e86ea63d76eed1bb1c1f9204645d631f2b
        charity_project = await project_crud.get(project_id, session)
        if charity_project.fully_invested:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Закрытый проект нельзя редактировать!'
            )
        return charity_project

    @staticmethod
    async def validate_full_amount(update_data, db_obj, session: AsyncSession):
<<<<<<< HEAD
=======
        """ Проверяет поле full_amount. """
>>>>>>> 8aec13e86ea63d76eed1bb1c1f9204645d631f2b
        if 'full_amount' in update_data and update_data['full_amount'] < db_obj.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Сумма проекта не может быть меньше инвестированной суммы!'
            )

    @staticmethod
    async def check_fully_and_invested_amounts(project_id: int, session: AsyncSession):
<<<<<<< HEAD
=======
        """ Проверяет наличие инвестированных средств. """
>>>>>>> 8aec13e86ea63d76eed1bb1c1f9204645d631f2b
        charity_project = await project_crud.get(project_id, session)
        if charity_project.fully_invested or charity_project.invested_amount > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='В проект были внесены средства, не подлежит удалению!'
            )


charity_project_validators = CharityProjectValidators()
<<<<<<< HEAD
=======

### Эта версия работает
>>>>>>> 8aec13e86ea63d76eed1bb1c1f9204645d631f2b
