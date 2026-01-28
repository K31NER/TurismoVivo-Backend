from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field
from domain.services import ServiceStatus

class Services(SQLModel,table=True):
    __tablename__ = "services"
    
    id: Optional[int] = Field(primary_key=True)
    name: str
    service_type: str
    price_min: int
    price_max: int
    currency: str
    regulatory_entity: str
    valid_until: date
    status: ServiceStatus