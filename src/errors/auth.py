class AuthenticationError(Exception):
    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(message)


class AuthorizationError(Exception):
    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message)
