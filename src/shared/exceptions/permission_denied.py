class PermissionDenied(Exception):

    def __init__(
        self,
        message: str = "Permission denied",
    ):
        super().__init__(message)