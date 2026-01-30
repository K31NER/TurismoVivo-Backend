from typing import Any, List
from domain.course import Course
from abc import ABC, abstractmethod

class CourseRepository(ABC):
    
    @abstractmethod
    async def read_courses(self, conn: Any) -> List[Course]:
        pass
    
    @abstractmethod
    async def read_course_by_id(self, id: int, conn: Any) -> Course:
        pass
    
    @abstractmethod
    async def create_course(self, data:Course, conn: Any) -> Course:
        pass
    
    @abstractmethod
    async def update_course(self, id: int ,data:Course, conn: Any) -> Course:
        pass 
    
    @abstractmethod
    async def delete_course(self, id: int, conn: Any) -> Course:
        pass
    