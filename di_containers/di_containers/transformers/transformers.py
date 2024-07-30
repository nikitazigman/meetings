import json
from abc import ABC, abstractmethod
from dataclasses import asdict
from datetime import datetime

from di_containers.schemas import report_schemas


class IErrorReportTransformer(ABC):
    @abstractmethod
    def transform(self, error_report: report_schemas.ErrorReport) -> str: ...
    
class MDErrorReportTransformer(IErrorReportTransformer):
    def transform(self, error_report: report_schemas.ErrorReport) -> str:
        report_to_publish = f"# Error report {datetime.now()}\n"
        
        for org_report in error_report.organization_report:
            report_to_publish += f"## Organization {org_report.organization}\n"
            for record in org_report.error_records:
                report_to_publish += f"- Subscription={record.subscription_id}, Error={record.error_type}\n"
        
        return report_to_publish
    
class JSONErrorReportTransformer(IErrorReportTransformer):
    def transform(self, error_report: report_schemas.ErrorReport) -> str:
        return json.dumps(asdict(error_report), indent=4)