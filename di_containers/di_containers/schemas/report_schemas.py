from dataclasses import dataclass
from enum import StrEnum


class ErrorType(StrEnum):
    EXPIRED = "expired"
    REVOKED_CREDENTIALS = "revoked credentials"


@dataclass
class ErrorRecord:
    subscription_id: str
    error_type: ErrorType

@dataclass
class OrganizationErrorReport:
    organization: str
    error_records: list[ErrorRecord]

@dataclass
class ErrorReport:
    organization_report: list[OrganizationErrorReport]
