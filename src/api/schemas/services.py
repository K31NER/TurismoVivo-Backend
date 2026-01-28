from typing import Optional
from datetime import date
from pydantic import BaseModel
from domain.services import ServiceStatus


# 1. Base
class ServiceBase(BaseModel):
    name: str
    service_type: str
    price_min: int
    price_max: int
    regulatory_entity: str
    valid_until: date
    status: ServiceStatus

# 2. Schema para recibir datos (CREAR)
class ServiceCreate(ServiceBase):
    pass 

# 3. Schema para Actualizar (Todos opcionales)
class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    service_type: Optional[str] = None
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    regulatory_entity: Optional[str] = None
    valid_until: Optional[date] = None
    status: Optional[ServiceStatus] = None

# 4. Schema para devolver datos (LEER)
class ServiceResponse(ServiceBase):
    id: int               
    currency: str = "COP" 

    class Config:
        from_attributes = True 