from typing import List
from domain.services import Service
from use_case.services import UseServices
from fastapi import APIRouter, HTTPException
from config.supabase_client import SupabaseDep
from api.schemas.services import ServiceResponse,ServiceCreate, ServiceUpdate
from infrastructure.database.functions.services import SupabaseServiceRepository

router = APIRouter(prefix="/service",tags=["Services"])

@router.get("",response_model=List[ServiceResponse],summary="Devuelve todos los servicios registrados")
async def read_all_services(supabase: SupabaseDep):
    
    supabase_services = SupabaseServiceRepository()
    services = UseServices(supabase_services)
    
    response = await services.read_services(supabase)
    
    return response

@router.get("/{id}",response_model=ServiceResponse,summary="Devuelve el servicio en base a su id")
async def read_service(id: int,supabase: SupabaseDep):
    
    supabase_services = SupabaseServiceRepository()
    services = UseServices(supabase_services)
    
    response = await services.read_service_by_id(id,supabase)
    
    if not response:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
        
    return response

@router.post("",summary="Se encarga de crear un nuevo servicio")
async def add_service(data: ServiceCreate, supabase: SupabaseDep):
    
    supabase_services = SupabaseServiceRepository()
    services = UseServices(supabase_services)
    new_service = Service(**data.model_dump())
    
    response = await services.create_service(new_service, supabase)
    
    return response

@router.patch("/{id}", summary="Actualiza parcialmente un servicio")
async def update_service(id: int, data: ServiceUpdate, supabase: SupabaseDep):
    supabase_services = SupabaseServiceRepository()
    services_usecase = UseServices(supabase_services)
    
    update_data = data.model_dump(exclude_unset=True)
    
    response = await services_usecase.partial_update_service(id, update_data, supabase)
    
    if not response:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    return response

@router.delete("/{id}",response_model=ServiceResponse,summary="Elimina un servicio")
async def delete_service(id: int,supabase: SupabaseDep):
    
    supabase_services = SupabaseServiceRepository()
    services = UseServices(supabase_services)
    
    response = await services.delete_service(id,supabase)
    
    if not response:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
        
    return response