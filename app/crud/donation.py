from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonations(CRUDBase):

    async def get_donations_by_user(
            self,
            user_id,
            session: AsyncSession,
    ):
        return "Пока работает как заглушка."


donation_crud = CRUDDonations(Donation)
