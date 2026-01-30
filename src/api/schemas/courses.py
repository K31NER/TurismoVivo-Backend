from pydantic import BaseModel, HttpUrl
from datetime import date
from typing import Optional
from domain.course import Modality, CourseStatus

class CourseBase(BaseModel):
    name: str
    course_link: str
    status: CourseStatus
    start_date: date
    modality: Modality
    provider: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    course_link: Optional[str] = None
    status: Optional[CourseStatus] = None
    start_date: Optional[date] = None
    modality: Optional[Modality] = None
    provider: Optional[str] = None

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True
