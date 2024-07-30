from dependency_injector import containers, providers
from di_containers.checkers import checkers
from di_containers.repositories import org_repositories, sub_repositories
from di_containers.transformers import transformers
from di_containers.services import services
from di_containers.publishers import publishers
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = ROOT_PATH / "config.yml"
print(CONFIG_PATH)


class RepositoriesContainer(containers.DeclarativeContainer):
    org_repository = providers.Factory(org_repositories.OrganizationRepository)
    sub_repository = providers.Factory(sub_repositories.SubscriptionRepository)


class TransformersContainer(containers.DeclarativeContainer):
    md_transformer = providers.Factory(transformers.MDErrorReportTransformer)
    json_transformer = providers.Factory(transformers.JSONErrorReportTransformer)


class PublisersContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    slack_publisher = providers.Factory(
        publishers.SlackPublisher,
        slack_channel=config.slack_publisher.slack_channel,
        slack_token=config.slack_publisher.slack_token,
    )
    file_publisher = providers.Factory(
        publishers.FilePublisher,
        file_name=config.file_publisher.file_name,
    )


class CheckersContainer(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()

    sub_checker = providers.Factory(
        checkers.SubscriptionExpiredChecker,
        repository=repositories.sub_repository,
    )
    cred_checker = providers.Factory(
        checkers.CredentialRevokedChecker,
        repository=repositories.sub_repository,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yml"])

    repositories: RepositoriesContainer = providers.Container(RepositoriesContainer)
    publishers: PublisersContainer = providers.Container(
        PublisersContainer, config=config.publishers
    )
    transformers: TransformersContainer = providers.Container(TransformersContainer)
    checkers: CheckersContainer = providers.Container(
        CheckersContainer, repositories=repositories
    )

    error_report_service = providers.Factory(
        services.ErrorReportService,
        repository=repositories.org_repository,
        publisher=publishers.file_publisher,
        transformer=transformers.md_transformer,
        checkers=providers.List(checkers.sub_checker, checkers.cred_checker),
    )
