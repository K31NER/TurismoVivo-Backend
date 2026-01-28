from typing import Any, List
from domain.services import Service
from abc import ABC, abstractmethod

class ServiceRepository(ABC):
    
    @abstractmethod
    async def read_services(self, conn: Any) -> List[Service]:
        pass
    
    @abstractmethod
    async def read_service_by_id(self, id: int, conn: Any) -> Service:
        pass
    
    @abstractmethod
    async def create_service(self, data:Service, conn: Any) -> Service:
        pass
    
    @abstractmethod
    async def update_service(self, id: int ,data:Service, conn: Any) -> Service:
        pass 
    
    @abstractmethod
    async def delete_service(self, id: int, conn: Any) -> Service:
        pass
    