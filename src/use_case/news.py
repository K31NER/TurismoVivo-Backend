from typing import Any
from datetime import date
from domain.news import New
from repository.news_repository import NewsRepository

class UseNews:
    
    def __init__(self, new_repo: NewsRepository):
        self.new_repo = new_repo
        
    async def read_news(self, conn: Any):
        """ Lee todos las noticias registradas """
        news = await self.new_repo.read_news(conn)
        return news
    
    async def read_new_by_id(self, id: int, conn: Any):
        """ busca la noticia por su id """
        new = await self.new_repo.read_new_by_id(id, conn)
        return new
        
    async def upload_image(self, file: Any, conn: Any) -> str:
        """ Sube una imagen mediante el repositorio y retorna la URL pública """
        
        # Leer el contenido binario del archivo de FastAPI
        file_content = await file.read()
        
        # Delegar la subida al repositorio
        public_url = await self.new_repo.get_image_link(file_content, conn)
        return public_url

    async def create_new(self, data: New, conn: Any):
        """ Crea una nueva noticia """
        # La validación ya ocurrió al instanciar el dominio 'New'
        new_record = await self.new_repo.create_new(data, conn)
        return new_record
    
    async def update_new(self, id: int, data: New, conn: Any):
        """ Actualiza una noticia """
        if data.id is None:
            data.id = id
        
        new_record = await self.new_repo.update_new(id, data, conn)
        return new_record
        
    async def partial_update_new(self, id: int, data: dict, conn: Any):
        """ Actualiza parcialmente una noticia """
        current_new_data = await self.read_new_by_id(id, conn)
        if not current_new_data:
            return None
            
        # 1. Identificamos si se va a reemplazar la imagen y guardamos la URL vieja
        old_img_url = current_new_data.get("img_link")
        should_delete_old = "img_link" in data and old_img_url

        # Conversion de fecha a objeto date si viene como string
        if isinstance(current_new_data.get("publiC_date"), str):
            current_new_data["publiC_date"] = date.fromisoformat(current_new_data["publiC_date"])
            
        # Aseguramos que los nombres coincidan con el constructor de 'New'
        current_new = New(
            title=current_new_data.get("title"),
            summary=current_new_data.get("summary"),
            link=current_new_data.get("link"),
            img_link=current_new_data.get("img_link"),
            public_date=current_new_data.get("publiC_date"),
            regulatory_entity=current_new_data.get("regulatory_entity"),
            id=current_new_data.get("id")
        )
        
        # Aplicamos los cambios que vienen en 'data' al objeto de dominio
        for key, value in data.items():
            if value is None:
                continue
                
            if key == "title":
                current_new.title = value
            elif key == "summary":
                current_new.summary = value
            elif key == "link":
                current_new.link = str(value) # Aseguramos que sea string si viene de Pydantic
            elif key == "img_link":
                current_new.img_link = value
            elif key == "date":
                current_new.date = value
            elif key == "regulatory_entity":
                current_new.regulatory_entity = value
            
        current_new.validate()
        
        # 2. Intentamos la actualización en la base de datos
        updated_new = await self.new_repo.update_new(id, current_new, conn)
        
        # 3. Solo si la actualización fue exitosa, borramos la imagen vieja del bucket
        if updated_new and should_delete_old:
            await self.new_repo.delete_image(old_img_url, conn)
            
        return updated_new
    
    async def delete_new(self, id: int, conn: Any):
        """ Elimina la noticia por su id y su imagen del bucket """
        # Obtenemos la noticia para conocer el link de la imagen
        current_new = await self.read_new_by_id(id, conn)
        
        if current_new and current_new.get("img_link"):
            await self.new_repo.delete_image(current_new["img_link"], conn)

        result = await self.new_repo.delete_new(id, conn)
        return result
        