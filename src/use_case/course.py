from datetime import date
from typing import Any
from domain.course import Course
from repository.course_repository import CourseRepository

class UseCourse:
    
    def __init__(self, course_repo: CourseRepository):
        self.course_repo = course_repo
        
    async def read_courses(self, conn: Any):
        """ Lee todos los cursos registrados """
        courses = await self.course_repo.read_courses(conn)
        return courses
    
    async def read_course_by_id(self, id: int, conn: Any):
        """ Busca el curso por su id """
        course = await self.course_repo.read_course_by_id(id, conn)
        return course
        
    async def create_course(self, data: Course, conn: Any):
        """ Crea un nuevo curso """
        course = await self.course_repo.create_course(data, conn)
        return course
    
    async def update_course(self, id: int, data: Course, conn: Any):
        """ Actualiza un curso """
        # Aseguramos que el ID del objeto coincida con el ID que queremos actualizar
        if data.id is None:
            data.id = id
        
        course = await self.course_repo.update_course(id, data, conn)
        return course
        
    async def partial_update_course(self, id: int, data: dict, conn: Any):
        """ Actualiza parcialmente un curso """
        current_course_data = await self.read_course_by_id(id, conn)
        if not current_course_data:
            return None
            
        # conversion de fecha a date
        if isinstance(current_course_data.get("start_date"), str):
            current_course_data["start_date"] = date.fromisoformat(current_course_data["start_date"])
            
        current_course = Course(
            name=current_course_data.get("name"),
            course_link=current_course_data.get("course_link"),
            status=current_course_data.get("status"),
            start_date=current_course_data.get("start_date"),
            modality=current_course_data.get("modality"),
            provider=current_course_data.get("provider"),
            id=current_course_data.get("id")
        )
        
        for key, value in data.items():
            if value is not None:
                setattr(current_course, key, value)
            
        current_course.valid()
        
        course = await self.course_repo.update_course(id, current_course, conn)
        return course
    
    async def delete_course(self, id: int, conn: Any):
        """ Elimina el curso por su id """
        course = await self.course_repo.delete_course(id, conn)
        return course
        