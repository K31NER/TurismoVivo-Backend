from enum import Enum
from datetime import date
from typing import Optional
from pydantic import TypeAdapter, HttpUrl

class Modality(str, Enum):
    IN_PERSON = "IN_PERSON"
    ONLINE = "ONLINE"
    HYBRID = "HYBRID"

class CourseStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    
class Course:
    
    def __init__(
        self,
        name: str,
        course_link: str,
        status: CourseStatus,
        start_date: date,
        modality: Modality,
        provider: str,
        id: Optional[int]):
        
        self.id = id
        self.name = name
        self.course_link = course_link
        self.status = status
        self.start_date = start_date
        self.modality = modality
        self.provider = provider
        
        self.valid()
    
    def valid(self):
        self._validate_link()
        self._valid_start_date()
    
    def _validate_link(self):
        
        url_adapter = TypeAdapter(HttpUrl)
        
        # Validamos el link del curso
        try:
            url_adapter.validate_python(self.course_link)
        except Exception:
            raise ValueError(f"El link del curso no es una URL válida: '{self.course_link}'. Asegúrate de que empiece con http:// o https://")
    
    def _valid_start_date(self):
        
        if self.start_date < date.today():
            raise ValueError("La fecha de inicio del curso no puede ser menor a la fecha actual")