from dependency_injector.wiring import Provide, inject

from di_containers.containers.containers import Container
from di_containers.services.services import IErrorReportService


@inject
def main(
    report_service: IErrorReportService = Provide[Container.error_report_service],
) -> None:
    report_service.run()


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    main()
