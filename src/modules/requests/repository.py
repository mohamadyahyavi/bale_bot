from sqlalchemy import select,exists
from sqlalchemy.ext.asyncio import AsyncSession

from .model import RequestModel
from .entity import RequestEntity
from ..users import UserModel
from .enums import RequestStatus




class RequestRepository:


    def __init__(
        self,
        session: AsyncSession
    ):

        self.session = session



    def _to_entity(
        self,
        model: RequestModel
    ):

        return RequestEntity(

            id=model.id,

            user_id=model.user_id,

            manager_id=model.manager_id,

            type=model.type,

            status=model.status,

            data=model.data,

            created_at=model.created_at,

            processed_at=model.processed_at
        )



    async def create(
        self,
        request: RequestEntity
    ):


        model = RequestModel(

            user_id=request.user_id,

            manager_id=request.manager_id,

            type=request.type.value,

            status=request.status.value,

            data=request.data

        )


        self.session.add(model)


        await self.session.commit()


        await self.session.refresh(model)


        return self._to_entity(model)



    async def get_by_id(
    self,
    request_id
):

        stmt = (
        select(RequestModel)
        .where(
            RequestModel.id == request_id
        )
    )


        result = await self.session.execute(stmt)


        request = result.scalar_one_or_none()


        if not request:
           return None


        return self._to_entity(request)    




    async def get_by_manager(
        self,
        manager_id
    ):


        stmt = select(RequestModel).where(

            RequestModel.manager_id == manager_id

        )


        result = await self.session.execute(stmt)


        requests = result.scalars().all()


        return [

            self._to_entity(r)

            for r in requests

        ]




    async def get_by_user(
        self,
        user_id
    ):


        stmt = select(RequestModel).where(

            RequestModel.user_id == user_id

        )


        result = await self.session.execute(stmt)


        requests = result.scalars().all()


        return [

            self._to_entity(r)

            for r in requests

        ]
    

    async def get_by_department(
    self,
    department_id
):

        stmt = (
        select(RequestModel)
        .join(
            UserModel,
            RequestModel.user_id == UserModel.id
        )
        .where(
            UserModel.department_id == department_id
        )
    )


        result = await self.session.execute(stmt)
        requests = result.scalars().all()
        return [
        self._to_entity(r)
        for r in requests
        ]

    async def get_managers_with_pending_requests(self, manager_id):

          stmt = select(RequestModel.manager_id).where(
            RequestModel.status == RequestStatus.PENDING
            ).distinct()

          result = await self.session.execute(stmt)

          return result.scalars().all()