from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field
from domain.course import Modality, CourseStatus

class Courses(SQLModel, table=True):
    __tablename__ = "courses"
    
    id: Optional[int] = Field(primary_key=True)
    name: str
    course_link: str
    status : CourseStatus
    start_date: date
    modality: Modality
    provider: str
    
    