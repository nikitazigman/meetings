from abc import ABC, abstractmethod

import rich


class Publisher(ABC):
    @abstractmethod
    def publish(self, error_report: str) -> None: ...


class SlackPublisher(Publisher):
    def __init__(self, slack_token: str, slack_channel: str) -> None:
        self.slack_channel = slack_channel
        self.slack_token = slack_token

    def publish(self, error_report: str) -> None:
        rich.print(
            f"Publishing to Slack channel {self.slack_channel}, {self.slack_token}"
        )
        rich.print(error_report)


class FilePublisher(Publisher):
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def publish(self, error_report: str) -> None:
        rich.print(f"Writing to file {self.file_name}")

        with open(self.file_name, "w") as f:
            f.write(error_report)
