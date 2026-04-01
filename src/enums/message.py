from enum import StrEnum


class Message(StrEnum):
    INVALID_CREDENTIALS = "auth.error.invalid_credentials"
    INSUFFICIENT_PERMISSION = "auth.error.insufficient_permissions"
    USER_ALREADY_EXIST = "user.error.already_exist"
    USER_NOT_FOUND = "user.error.not_found"
