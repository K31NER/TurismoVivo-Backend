import uuid
from typing import Any, List
from domain.news import New
from config.settings import settings
from config.supabase_client import SupabaseDep
from repository.news_repository import NewsRepository
from infrastructure.database.models.news import News

NEWS_TABLE = News.__tablename__

class SupabaseNewsRepository(NewsRepository):
    
    async def get_image_link(self, img: bytes, conn: SupabaseDep) -> str:
        """ Sube el contenido binario de una imagen al bucket y retorna su URL pública """
        
        file_name = f"{uuid.uuid4()}.jpg"
        
        await conn.storage.from_(settings.SUPABSE_BUCKET).upload(
            path=file_name,
            file=img,
            file_options={"content-type": "image/jpeg"}
        )
        
        # Retorna la URL pública del archivo subido
        public_url = await conn.storage.from_(settings.SUPABSE_BUCKET).get_public_url(file_name)
        return public_url

    async def delete_image(self, img_url: str, conn: SupabaseDep) -> None:
        """ Elimina una imagen del bucket de Supabase dado su URL pública """
        try:
            path_parts = img_url.split(f"/{settings.SUPABSE_BUCKET}/")
            if len(path_parts) > 1:
                file_path = path_parts[1]
                await conn.storage.from_(settings.SUPABSE_BUCKET).remove([file_path])
                
        except Exception as e:
            print(f"Error al eliminar imagen del bucket: {e}")

    async def read_news(self, conn: SupabaseDep) -> List[Any]:
        news = await conn.table(NEWS_TABLE).select("*").execute()
        return news.data
    
    async def read_new_by_id(self, id: int, conn: SupabaseDep) -> Any:
        new = await conn.table(NEWS_TABLE).select("*").eq("id", id).execute()
        if new.data:
            return new.data[0]
        return None
    
    async def create_new(self, data: New, conn: SupabaseDep) -> Any:
        
        new_dict = {
            "title": data.title,
            "summary": data.summary,
            "link": data.link,
            "img_link": data.img_link,
            "publiC_date": data.date.isoformat(), 
            "regulatory_entity": data.regulatory_entity
        }
        
        new = await conn.table(NEWS_TABLE).insert(new_dict).execute()
        return new.data[0]
    
    async def update_new(self, id: int, data: New, conn: SupabaseDep) -> Any:
        
        new_dict = {
            "title": data.title,
            "summary": data.summary,
            "link": data.link,
            "img_link": data.img_link,
            "publiC_date": data.date.isoformat(),
            "regulatory_entity": data.regulatory_entity
        }
        
        new = await conn.table(NEWS_TABLE).update(new_dict).eq("id", id).execute()
        
        if new.data:
            return new.data[0]
        return None
    
    async def delete_new(self, id: int, conn: SupabaseDep) -> Any:
        new = await conn.table(NEWS_TABLE).delete().eq("id", id).execute()
        
        if new.data:
            return new.data[0]
        return None
