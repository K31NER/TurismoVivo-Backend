from domain.news import New
from typing import Any, List
from abc import ABC, abstractmethod

class NewsRepository(ABC):
    
    @abstractmethod
    async def get_image_link(self, img: bytes, conn: Any) -> str:
        pass

    @abstractmethod
    async def delete_image(self, img_url: str, conn: Any) -> None:
        pass
    
    @abstractmethod
    async def read_news(self, conn: Any) -> List[New]:
        pass
    
    @abstractmethod
    async def read_new_by_id(self, id: int, conn: Any) -> New:
        pass
    
    @abstractmethod
    async def create_new(self, data:New, conn: Any) -> New:
        pass
    
    @abstractmethod
    async def update_new(self, id: int ,data:New, conn: Any) -> New:
        pass 
    
    @abstractmethod
    async def delete_new(self, id: int, conn: Any) -> New:
        pass
    