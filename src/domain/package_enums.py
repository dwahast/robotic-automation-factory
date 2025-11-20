from enum import Enum

class PackageClassification(str, Enum):
    STANDARD = "STANDARD"
    SPECIAL = "SPECIAL"
    REJECTED = "REJECTED"

class PackageStatus(str, Enum):
    PENDING = "PENDING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"