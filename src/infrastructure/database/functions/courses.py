from enum import Enum
from domain.course import Course
from config.supabase_client import SupabaseDep
from repository.course_repository import CourseRepository
from infrastructure.database.models.courses import Courses

COURSE_TABLE = Courses.__tablename__

class SupabaseCourseRepository(CourseRepository):
    
    async def read_courses(self, conn: SupabaseDep):
        services = await conn.table(COURSE_TABLE).select("*").execute()
        return services.data
    
    async def read_course_by_id(self, id:int, conn:SupabaseDep):
        service = await conn.table(COURSE_TABLE).select("*").eq("id",id).execute()
        if service.data:
            return service.data[0]
        return None
    
    async def create_course(self, data: Course, conn: SupabaseDep):
        
        course_dict = {
            "name": data.name,
            "course_link": data.course_link,
            "status": data.status.value if isinstance(data.status, Enum) else data.status,
            "start_date": data.start_date.isoformat(),
            "modality": data.modality.value if isinstance(data.modality, Enum) else data.modality,
            "provider": data.provider
        }
        
        result = await conn.table(COURSE_TABLE).insert(course_dict).execute()
        
        return result.data[0]
    
    async def update_course(self, id: int, data: Course, conn: SupabaseDep):
        
        status_value = data.status.value if isinstance(data.status, Enum) else data.status
        modality_value = data.modality.value if isinstance(data.modality, Enum) else data.modality
        
        course_dict = {
            "name": data.name,
            "course_link": data.course_link,
            "status": status_value,
            "start_date": data.start_date.isoformat(),
            "modality": modality_value,
            "provider": data.provider
        }
        
        result = await conn.table(COURSE_TABLE).update(course_dict).eq("id", id).execute()
        
        if result.data:
            return result.data[0]
        return None
    
    async def delete_course(self, id: int, conn: SupabaseDep):
        result = await conn.table(COURSE_TABLE).delete().eq("id", id).execute()
        
        if result.data:
            return result.data[0]
        
        return None
    
    