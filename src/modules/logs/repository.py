from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

from .model import OperationLog



class LogRepository:


    def __init__(
        self,
        session: AsyncSession
    ):
        self.session = session



    async def create(
        self,
        log: OperationLog
    ):

        self.session.add(log)

        await self.session.commit()

        await self.session.refresh(log)

        return log



    async def get_by_user_id(
        self,
        user_id
    ):

        result = await self.session.execute(
            select(OperationLog)
            .where(
                OperationLog.user_id == user_id
            )
            .order_by(
                OperationLog.created_at.desc()
            )
        )


        return result.scalars().all()



    async def get_all(
        self,
        limit: int = 100
    ):

        result = await self.session.execute(
            select(OperationLog)
            .order_by(
                OperationLog.created_at.desc()
            )
            .limit(limit)
        )


        return result.scalars().all()

    async def get_last_30_days_logs(self):

        from_date = datetime.now() - timedelta(days=30)

        stmt = (
        select(OperationLog)
        .where(
            OperationLog.created_at >= from_date
        )
        .order_by(
            OperationLog.created_at.desc()
        )
    )

        result = await self.session.execute(stmt)

        return result.scalars().all()