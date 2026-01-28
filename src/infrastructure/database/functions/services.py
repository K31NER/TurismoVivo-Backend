from enum import Enum
from config.supabase_client import SupabaseDep
from repository.services_repository import ServiceRepository
from infrastructure.database.models.services import Services

SERVICES_TABLE = Services.__tablename__

class SupabaseServiceRepository(ServiceRepository):
    
    async def read_services(self, conn: SupabaseDep):
        services = await conn.table(SERVICES_TABLE).select("*").execute()
        return services.data
    
    async def read_service_by_id(self, id, conn:SupabaseDep):
        service = await conn.table(SERVICES_TABLE).select("*").eq("id",id).execute()
        if service.data:
            return service.data[0]
        return None
    
    async def create_service(self, data: Services, conn:SupabaseDep):
        
        service_dict = {
            "name": data.name,
            "service_type": data.service_type,
            "price_min": data.price_min,
            "price_max": data.price_max,
            "currency": data.currency,
            "regulatory_entity": data.regulatory_entity,
            "valid_until": data.valid_until.isoformat(),
            "status": data.status.value
        }
        
        service = await conn.table(SERVICES_TABLE).insert(service_dict).execute()
        
        return service.data[0]
    
    async def update_service(self, id, data, conn):
        
        status_value = data.status.value if isinstance(data.status, Enum) else data.status
        
        service_dict = {
            "name": data.name,
            "service_type": data.service_type,
            "price_min": data.price_min,
            "price_max": data.price_max,
            "currency": data.currency,
            "regulatory_entity": data.regulatory_entity,
            "valid_until": data.valid_until.isoformat(),
            "status": status_value
        }
        
        service = await conn.table(SERVICES_TABLE).update(service_dict).eq("id", id).execute()
        
        if service.data:
            return service.data[0]
        return None
    
    
    async def delete_service(self, id, conn: SupabaseDep):
        service = await conn.table(SERVICES_TABLE).delete().eq("id",id).execute()
        
        if service.data:
            return service.data[0]
        
        return None
    
    