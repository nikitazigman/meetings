from abc import ABC, abstractmethod
from datetime import datetime

from di_containers.schemas.subscriptions_schemas import Subscription


class Repository(ABC):
    @abstractmethod
    def get_expired_subs(self, org_id: str) -> list[Subscription]:
        ...
        
class SubscriptionRepository(Repository):
    def get_expired_subs(self,  org_id: str) -> list[Subscription]:
        return [
            Subscription(id="1", expiration=datetime(2021, 1, 1)),
            Subscription(id="2", expiration=datetime(2021, 2, 1)),
            Subscription(id="3", expiration=datetime(2021, 3, 1)),
            Subscription(id="4", expiration=datetime(2021, 4, 1)),
        ]