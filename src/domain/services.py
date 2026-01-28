from enum import Enum
from datetime import date
from typing import Optional

class ServiceStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    DRAFT = "DRAFT"
class Service:
    def __init__(
        self,
        name: str,
        service_type: str,
        price_min: int,
        price_max: int,
        regulatory_entity: str,
        valid_until: date,
        status: ServiceStatus,
        id: Optional[int] = None,
        currency: str = "COP"
    ):
        self.id = id
        self.name = name
        self.service_type = service_type
        self.price_min = price_min
        self.price_max = price_max
        self.currency = currency
        self.regulatory_entity = regulatory_entity
        self.valid_until = valid_until
        self.status = status
        
        self.validate()

    def validate(self):
        self._validate_prices()
        self._validate_validity()

    def _validate_prices(self):
        if self.price_min < 0 or self.price_max < 0:
            raise ValueError("Los precios no pueden ser negativos")

        if self.price_min > self.price_max:
            raise ValueError("El precio mínimo no puede ser mayor al máximo")

    def _validate_validity(self):
        if self.valid_until <= date.today():
            raise ValueError("La vigencia debe ser una fecha futura")

    def is_active(self) -> bool:
        return self.status == ServiceStatus.ACTIVE
