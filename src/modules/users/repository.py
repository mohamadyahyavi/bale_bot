from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from .entity import User
from .model import UserModel


class UserRepository:


    def __init__(self, session: AsyncSession):
        self.session = session



    def _to_entity(self, model: UserModel) -> User:

        return User(

            id=model.id,

            bale_user_id=model.bale_user_id,

            first_name=model.first_name,

            last_name=model.last_name,

            email=model.email,

            mobile=model.mobile,

            kimai_user_id=model.kimai_user_id,

            department_id=model.department_id,

            is_active=model.is_active,

            contract_start_date=model.contract_start_date,

            contract_end_date=model.contract_end_date,

            total_leave_hours=model.total_leave_hours,

            access_level=model.access_level
        )



    async def create(
    self,
    user: User,
):

        model = UserModel(
        bale_user_id=user.bale_user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        mobile=user.mobile,
        department_id=user.department_id,
        kimai_user_id=user.kimai_user_id,
        contract_start_date=user.contract_start_date,
        contract_end_date=user.contract_end_date,
        is_active=user.is_active,
        total_leave_hours=user.total_leave_hours,
        access_level=user.access_level,
    )

        self.session.add(model)

        await self.session.commit()

        await self.session.refresh(model)

        return self._to_entity(model)



    async def get_by_bale_id(self, bale_user_id: str):

        stmt = select(UserModel).where(
            UserModel.bale_user_id == bale_user_id
        )

        result = await self.session.execute(stmt)

        user = result.scalar_one_or_none()

        if not user:
            return None

        return self._to_entity(user)

    async def get_by_id(self, user_id: UUID):

        stmt = select(UserModel).where(
            UserModel.id == user_id
        )

        result = await self.session.execute(stmt)

        user = result.scalar_one_or_none()

        if not user:
            return None

        return self._to_entity(user)




    async def get_by_department_id(self, department_id: UUID):

        stmt = select(UserModel).where(
            UserModel.department_id == department_id,
            UserModel.is_active == True
        )

        result = await self.session.execute(stmt)

        users = result.scalars().all()

        return [
            self._to_entity(u)
            for u in users
        ]




    async def get_hr_user(self):

        stmt = select(UserModel).where(
            UserModel.access_level == "HR"
        )

        result = await self.session.execute(stmt)

        user = result.scalar_one_or_none()

        return  self._to_entity(user)
    
    async def get_ceo_user(self):

        stmt = select(UserModel).where(
            UserModel.access_level == "CEO"
        )

        result = await self.session.execute(stmt)

        user = result.scalars().all()

        return [
            self._to_entity(u)
            
        ]
    


    async def get_active_users(self):

        stmt = select(UserModel).where(
            UserModel.is_active == True
        )

        result = await self.session.execute(stmt)

        users = result.scalars().all()

        return [
            self._to_entity(u)
            for u in users
        ]
    

    async def get_users_with_contract_expiry(
    self,
    start_date:date,
    end_date:date
    ):

        stmt = select(UserModel).where(
        UserModel.contract_end_date.between(start_date,end_date),
        UserModel.is_active == True
        )

        result = await self.session.execute(stmt)

        users = result.scalars().all()

        return [
        self._to_entity(user)
        for user in users
        ]
    
    async def update(
             self,
             user: User
        ):

        stmt = select(UserModel).where(
            UserModel.id == user.id
            )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()


        if not model:
               raise Exception("User not found")


        model.total_leave_hours = user.total_leave_hours


        await self.session.commit()

        await self.session.refresh(model)


        return self._to_entity(model)