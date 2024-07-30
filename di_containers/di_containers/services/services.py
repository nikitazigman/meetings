from abc import ABC, abstractmethod

from di_containers.checkers import checkers
from di_containers.publishers import publishers
from di_containers.repositories import org_repositories
from di_containers.schemas import report_schemas
from di_containers.transformers import transformers


class IErrorReportService(ABC):
    @abstractmethod
    def run(self) -> None:
        """Run checkers and report errors"""


class ErrorReportService(IErrorReportService):
    def __init__(
        self,
        checkers: list[checkers.Checker],
        publisher: publishers.Publisher,
        transformer: transformers.IErrorReportTransformer,
        repository: org_repositories.Repository,
    ) -> None:
        self.checkers = checkers
        self.publisher = publisher
        self.repository = repository
        self.transformer = transformer

    def run(self) -> None:
        error_report = self.get_error_report()
        report_to_publish = self.transformer.transform(error_report=error_report)
        self.publisher.publish(error_report=report_to_publish)

    def get_error_report(self) -> report_schemas.ErrorReport:
        error_report = report_schemas.ErrorReport(organization_report=[])

        for org in self.repository.get_all():
            error_records = [
                report
                for checker in self.checkers
                for report in checker.run(org_id=org.id)
            ]
            org_error_report = report_schemas.OrganizationErrorReport(
                organization=org.name, error_records=error_records
            )
            error_report.organization_report.append(org_error_report)

        return error_report

