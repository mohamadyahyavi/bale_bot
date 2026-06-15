from enum import Enum


class RequestType(str, Enum):
    LEAVE = "LEAVE"
    REMOTE = "REMOTE"
    OVERTIME = "OVERTIME"
    MISSION = "MISSION"


class RequestStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class LeaveType(str, Enum):
    HOURLY = "HOURLY"
    DAILY = "DAILY"