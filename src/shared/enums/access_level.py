from enum import StrEnum


class AccessLevel(StrEnum):
    EMPLOYEE = "EMPLOYEE"
    HR = "HR"
    CEO = "CEO"
    ADMIN = "ADMIN"