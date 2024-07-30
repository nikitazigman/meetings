from abc import ABC, abstractmethod

from di_containers.repositories import sub_repositories
from di_containers.schemas import report_schemas


class Checker(ABC):
    @abstractmethod
    def run(self, org_id: str) -> list[report_schemas.ErrorRecord]: ...


class SubscriptionExpiredChecker(Checker):
    def __init__(self, repository: sub_repositories.Repository) -> None:
        self.repository = repository

    def run(self, org_id: str) -> list[report_schemas.ErrorRecord]:
        errors: list[report_schemas.ErrorRecord] = []
        expired_subs = self.repository.get_expired_subs(org_id=org_id)

        for sub in expired_subs:
            error_record = report_schemas.ErrorRecord(
                subscription_id=sub.id,
                error_type=report_schemas.ErrorType.EXPIRED,
            )
            errors.append(error_record)

        return errors

class CredentialRevokedChecker(Checker):
    def __init__(self, repository: sub_repositories.Repository)->None:
        self.repository = repository

    def run(self, org_id: str)-> list[report_schemas.ErrorRecord]:
        errors: list[report_schemas.ErrorRecord] = []
        expired_subs = self.repository.get_expired_subs(org_id=org_id)
        
        for sub in expired_subs:
            error_record = report_schemas.ErrorRecord(
                subscription_id=sub.id,
                error_type=report_schemas.ErrorType.REVOKED_CREDENTIALS,
            )
            errors.append(error_record)

        return errors

