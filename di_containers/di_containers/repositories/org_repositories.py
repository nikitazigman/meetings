from abc import ABC, abstractmethod

from di_containers.schemas.organization_schemas import Organization


class Repository(ABC):
    @abstractmethod
    def get_all(self) -> list[Organization]:
        ...
        
class OrganizationRepository(Repository):
    def get_all(self) -> list[Organization]:
        return [Organization(id="1", name="org1"), Organization(id="2", name="org2")]