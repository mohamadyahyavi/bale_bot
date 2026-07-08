from sqlalchemy import select,exists
from sqlalchemy.ext.asyncio import AsyncSession

from .model import RequestModel
from .entity import RequestEntity
from ..users import UserModel
from .enums import RequestStatus,RequestType
from datetime import datetime,timedelta,time

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

            type=RequestType(model.type),

            status=RequestStatus(model.status),

            data=model.data,

            created_at=model.created_at,

            processed_at=model.processed_at,
            reject_reason=model.reject_reason
        )


    async def create(
        self,
        request: RequestEntity
    ):


        model = RequestModel(

            user_id=request.user_id,

            manager_id=request.manager_id,

            type=request.type.value
                if hasattr(request.type, "value")
                else request.type,

            status=request.status.value
                if hasattr(request.status, "value")
                else request.status,

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


        thirty_days_ago = datetime.now() - timedelta(days=30)


        stmt = (
        select(RequestModel)
        .where(
            RequestModel.manager_id == manager_id,
            RequestModel.created_at >= thirty_days_ago
        ).order_by(RequestModel.created_at.desc())
        
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

    async def get_managers_with_pending_requests(self):

          stmt = (
          select(UserModel.bale_user_id)
          .join(
            RequestModel,
            RequestModel.manager_id == UserModel.id
          )
         .where(
            RequestModel.status == RequestStatus.PENDING
          )
         .distinct()
    )

          result = await self.session.execute(stmt)

          return result.scalars().all()


    async def get_month_approved_leaves(self):
        
        now = datetime.now()

        begin = datetime(
        year=now.year,
        month=now.month,
        day=1,
        hour=0,
        minute=0,
        second=0,
        )

        stmt = (
        select(RequestModel)
        .where(
            
            RequestModel.type == RequestType.LEAVE,
            RequestModel.status == RequestStatus.ACCEPTED,
            RequestModel.created_at >= begin,
        )
        .order_by(RequestModel.created_at.desc())
        )

        result = await self.session.execute(stmt)
        requests = result.scalars().all()

        return [self._to_entity(r) for r in requests]       
    

    async def update(
          self,
          request: RequestEntity
          ):

        stmt = (
        select(RequestModel)
        .where(
            RequestModel.id == request.id
        )
        )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()


        if not model:
           raise Exception("Request not found")


        model.status = (
        request.status.value
        if hasattr(request.status, "value")
        else request.status
        )

        model.processed_at = request.processed_at
        model.reject_reason = request.reject_reason


        await self.session.commit()


        await self.session.refresh(model)


        return self._to_entity(model)
    

    async def get_all_leave_requests(self):

        thirty_days_ago = datetime.now() - timedelta(days=30)

        stmt = (
        select(RequestModel)
        .where(
            RequestModel.created_at >= thirty_days_ago,
            RequestModel.type == RequestType.LEAVE,
        )
        .order_by(RequestModel.created_at.desc())
        )

        result = await self.session.execute(stmt)

        requests = result.scalars().all()

        return [
        self._to_entity(r)
        for r in requests
        ]
    
    async def get_today_overtime_by_user_id(self,user_id):

        now = datetime.now()

        begin = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=0,
        minute=0,
        second=0,
        )

        stmt = (
        select(RequestModel)
        .where(
            RequestModel.created_at >= begin,
            RequestModel.type == RequestType.OVERTIME,
            RequestModel.status == RequestStatus.ACCEPTED,
            RequestModel.user_id == user_id,
            )
        )

        result = await self.session.execute(stmt)

        requests = result.scalars().all()

        total_hours = 0.0

        for request in requests:
            data = request.data or {}
            total_hours += float(data.get("hours", 0))

        total_minutes = int(total_hours * 60)

        hours = total_minutes // 60
        minutes = total_minutes % 60

        return f"{hours}:{minutes:02d}"
    
    async def get_week_overtime_by_user_id(
      self,
      user_id,
    ) -> str:

      now = datetime.now()

      days_since_saturday = (now.weekday() + 2) % 7

      week_start = now - timedelta(days=days_since_saturday)

      begin = datetime(
        year=week_start.year,
        month=week_start.month,
        day=week_start.day,
        hour=0,
        minute=0,
        second=0,
      )

      stmt = (
        select(RequestModel)
        .where(
            RequestModel.user_id == user_id,
            RequestModel.type == RequestType.OVERTIME,
            RequestModel.status == RequestStatus.ACCEPTED,
            RequestModel.created_at >= begin,
           )
        )

      result = await self.session.execute(stmt)

      requests = result.scalars().all()

      total_hours = 0

      for request in requests:

        data = request.data or {}

        total_hours += int(data.get("hours", 0))

      hours = total_hours
      minutes = 0

      return f"{hours}:{minutes:02d}"
    

    async def get_month_overtime_by_user_id(
    self,
    user_id,
    ) -> str:

       now = datetime.now()

       begin = datetime(
        year=now.year,
        month=now.month,
        day=1,
        hour=0,
        minute=0,
        second=0,
       )

       stmt = (
        select(RequestModel)
        .where(
            RequestModel.user_id == user_id,
            RequestModel.type == RequestType.OVERTIME,
            RequestModel.status == RequestStatus.ACCEPTED,
            RequestModel.created_at >= begin,
          )
       )

       result = await self.session.execute(stmt)

       requests = result.scalars().all()

       total_hours = 0

       for request in requests:

         data = request.data or {}

         total_hours += int(data.get("hours", 0))

       return f"{total_hours}:00"
