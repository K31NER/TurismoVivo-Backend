from fastapi import Depends
from typing import Annotated
from config.settings import settings
from supabase import AsyncClient, acreate_client

# Variable global para almacenar la instancia
_supabase_client: AsyncClient | None = None

async def get_supabase_client() -> AsyncClient:
    """ 
    Devuelve una instancia única del cliente de Supabase (Singleton).
    Si no existe, la crea. Si ya existe, devuelve la misma.
    """
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = await acreate_client(
            supabase_key=settings.SUPABASE_API_KEY, 
            supabase_url=settings.SUPABASE_PROJECT
        )
    return _supabase_client

SupabaseDep = Annotated[AsyncClient, Depends(get_supabase_client)]
