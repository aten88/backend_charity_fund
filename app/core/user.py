from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers,
    IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """ Асинхронный генератор. """
    yield SQLAlchemyUserDatabase(session, User)

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """ Стратегия хранения токена в виде JWT. """
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """ Класс управления юзером. """

    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User]
    ) -> None:
        """ Метод проверки пароля. """
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Пароль должен быть больше 3 символов.'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль не может содержать e-mail.'
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        """ Метод действий после регистрации. """
        print(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(user_db=Depends(get_user_db)):
    """ Метод возврата обьект UserManager. """
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
