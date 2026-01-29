from datetime import date
from typing import Any
from domain.services import Service
from repository.services_repository import ServiceRepository

class UseServices:
    
    def __init__(self, services_repo: ServiceRepository):
        self.services_repo = services_repo
        
    async def read_services(self, conn: Any):
        """ Lee todos los servicios registrados """
        services = await self.services_repo.read_services(conn)
        return services
    
    async def read_service_by_id(self,id: int, conn: Any):
        """ busca el servicio por su id """
        
        service = await self.services_repo.read_service_by_id(id, conn)
        return service
        
        
    async def create_service(self, data: Service, conn: Any):
        """ Crea un nuevo servicio """
        
        service = await self.services_repo.create_service(data,conn)
        
        return service
    
    async def update_service(self, id: int, data: Service, conn: Any):
        """ Actualiza un servicio """
        
        # Aseguramos que el ID del objeto coincida con el ID que queremos actualizar
        if data.id is None:
            data.id = id
        
        service = await self.services_repo.update_service(id,data,conn)
        
        return service
        
    async def partial_update_service(self, id: int, data: dict, conn: Any):
        """ Actualiza parcialmente un servicio """
        
        current_service_data = await self.read_service_by_id(id, conn)
        if not current_service_data:
            return None
            
        # conversion de fecha a date
        if isinstance(current_service_data.get("valid_until"), str):
            current_service_data["valid_until"] = date.fromisoformat(current_service_data["valid_until"])
            
        current_service = Service(**current_service_data)
        
        for key, value in data.items():
            setattr(current_service, key, value)
            
        current_service.validate()
        
        service = await self.services_repo.update_service(id, current_service, conn)
        
        return service
    
    async def delete_service(self, id: int, conn: Any):
        """ elimina el servicio por su id """
        
        service = await self.services_repo.delete_service(id, conn)
        
        return service
        