class UserNotFoundError(Exception):
    def __init__(self, message: str = "User not found") -> None:
        super().__init__(message)


class UserAlreadyExistError(Exception):
    def __init__(self, message: str = "User already exist") -> None:
        super().__init__(message)
