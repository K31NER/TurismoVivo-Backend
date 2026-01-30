from typing import List
from domain.course import Course
from use_case.course import UseCourse
from fastapi import APIRouter, HTTPException
from config.supabase_client import SupabaseDep
from api.schemas.courses import CourseResponse, CourseCreate, CourseUpdate
from infrastructure.database.functions.courses import SupabaseCourseRepository

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("", response_model=List[CourseResponse], summary="Devuelve todos los cursos registrados")
async def read_all_courses(supabase: SupabaseDep):
    
    supabase_repository = SupabaseCourseRepository()
    use_case = UseCourse(supabase_repository)
    
    response = await use_case.read_courses(supabase)
    
    return response

@router.get("/{id}", response_model=CourseResponse, summary="Devuelve el curso en base a su id")
async def read_course(id: int, supabase: SupabaseDep):
    
    supabase_repository = SupabaseCourseRepository()
    use_case = UseCourse(supabase_repository)
    
    response = await use_case.read_course_by_id(id, supabase)
    
    if not response:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
        
    return response

@router.post("", response_model=CourseResponse, summary="Se encarga de crear un nuevo curso")
async def add_course(data: CourseCreate, supabase: SupabaseDep):
    
    supabase_repository = SupabaseCourseRepository()
    use_case = UseCourse(supabase_repository)
    
    # Creamos la instancia de dominio
    new_course = Course(**data.model_dump(), id=None)
    
    response = await use_case.create_course(new_course, supabase)
    
    return response

@router.patch("/{id}", response_model=CourseResponse, summary="Actualiza parcialmente un curso")
async def update_course(id: int, data: CourseUpdate, supabase: SupabaseDep):
    supabase_repository = SupabaseCourseRepository()
    use_case = UseCourse(supabase_repository)
    
    update_data = data.model_dump(exclude_unset=True)
    
    response = await use_case.partial_update_course(id, update_data, supabase)
    
    if not response:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    return response

@router.delete("/{id}", response_model=CourseResponse, summary="Elimina un curso")
async def delete_course(id: int, supabase: SupabaseDep):
    
    supabase_repository = SupabaseCourseRepository()
    use_case = UseCourse(supabase_repository)
    
    response = await use_case.delete_course(id, supabase)
    
    if not response:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
        
    return response