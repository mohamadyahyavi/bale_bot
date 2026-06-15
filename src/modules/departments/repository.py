from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .entity import Department
from .model import DepartmentModel


class DepartmentRepository:


    def __init__(self, session: AsyncSession):
        self.session = session



    def _to_entity(self, model: DepartmentModel) -> Department:

        return Department(

            id=model.id,

            name=model.name,

            manager_user_id=model.manager_user_id
        )



    async def get_by_id(self, department_id: UUID):

        stmt = select(DepartmentModel).where(
            DepartmentModel.id == department_id
        )

        result = await self.session.execute(stmt)

        dept = result.scalar_one_or_none()

        if not dept:
            return None

        return self._to_entity(dept)




    async def get_all(self):

        stmt = select(DepartmentModel)

        result = await self.session.execute(stmt)

        departments = result.scalars().all()

        return [
            self._to_entity(d)
            for d in departments
        ]




    async def get_by_manager_id(self, manager_user_id: UUID):

        stmt = select(DepartmentModel).where(
            DepartmentModel.manager_user_id == manager_user_id
        )

        result = await self.session.execute(stmt)

        dept = result.scalar_one_or_none()

        if not dept:
            return None

        return self._to_entity(dept)