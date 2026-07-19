from .model import OperationLog
from .enums import LogAction, LogResult



class LogService:


    def __init__(
        self,
        repository
    ):
        self.repository = repository



    async def create_log(
        self,
        user_id,
        action: LogAction,
        result: LogResult,
        description: str | None = None,
    ):


        log = OperationLog(

            user_id=user_id,

            action=action.value
            if isinstance(action, LogAction)
            else action,

            result=result.value
            if isinstance(result, LogResult)
            else result,

            description=description,
        )


        return await self.repository.create(log)




    async def log_success(
        self,
        user_id,
        action,
        description=None,
    ):

        return await self.create_log(
            user_id=user_id,
            action=action,
            result=LogResult.SUCCESS,
            description=description,
        )




    async def log_failed(
        self,
        user_id,
        action,
        description=None,
    ):

        return await self.create_log(
            user_id=user_id,
            action=action,
            result=LogResult.FAILED,
            description=description,
        )