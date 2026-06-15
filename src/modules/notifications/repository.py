from sqlalchemy.ext.asyncio import AsyncSession

from .model import NotificationModel
from .entity import NotificationEntity


class NotificationRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    def _to_entity(self, model: NotificationModel) -> NotificationEntity:

        return NotificationEntity(

            id=model.id,
            user_id=model.user_id,
            title=model.title,
            message=model.message,
            status=model.status,
            created_at=model.created_at
        )


    async def create(self, notif: NotificationEntity) -> NotificationEntity:

        model = NotificationModel(

            user_id=notif.user_id,
            title=notif.title,
            message=notif.message,
            status=notif.status
        )

        self.session.add(model)

        await self.session.commit()
        await self.session.refresh(model)

        return self._to_entity(model)


    async def get_by_user(self, user_id):

        rows = await self.session.execute(
            """
            SELECT * FROM notifications
            WHERE user_id = :user_id
            ORDER BY created_at DESC
            """,
            {"user_id": user_id}
        )

        return rows.fetchall()