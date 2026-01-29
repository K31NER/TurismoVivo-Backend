from typing import List, Optional
from datetime import date
from domain.news import New
from use_case.news import UseNews
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from config.supabase_client import SupabaseDep
from api.schemas.news import NewsResponse, NewsUpdate, NewsCreate
from infrastructure.database.functions.news import SupabaseNewsRepository

router = APIRouter(prefix="/news", tags=["News"])

@router.get("", response_model=List[NewsResponse], summary="Devuelve todas las noticias registradas")
async def read_all_news(supabase: SupabaseDep):
    news_repo = SupabaseNewsRepository()
    use_case = UseNews(news_repo)
    
    response = await use_case.read_news(supabase)
    return response

@router.get("/{id}", response_model=NewsResponse, summary="Devuelve una noticia por su id")
async def read_news_by_id(id: int, supabase: SupabaseDep):
    news_repo = SupabaseNewsRepository()
    use_case = UseNews(news_repo)
    
    response = await use_case.read_new_by_id(id, supabase)
    if not response:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    return response

@router.post("", response_model=NewsResponse, summary="Crea una nueva noticia con imagen")
async def create_news(
    supabase: SupabaseDep,
    data: NewsCreate = Depends(NewsCreate.as_form),
    image: UploadFile = File(...)):
    
    news_repo = SupabaseNewsRepository()
    use_case = UseNews(news_repo)
    
    # 1. Subir imagen al bucket
    img_url = await use_case.upload_image(image, supabase)
    
    # 2. Crear objeto de dominio
    new_domain = New(
        title=data.title,
        summary=data.summary,
        link=str(data.link),
        img_link=img_url,
        public_date=data.publiC_date,
        regulatory_entity=data.regulatory_entity
    )
    
    # 3. Guardar en base de datos
    response = await use_case.create_new(new_domain, supabase)
    return response

@router.patch("/{id}", response_model=NewsResponse, summary="Actualiza parcialmente una noticia")
async def update_news(
    id: int,
    supabase: SupabaseDep,
    data: NewsUpdate = Depends(NewsUpdate.as_form),
    image: Optional[UploadFile] = File(None)
):
    news_repo = SupabaseNewsRepository()
    use_case = UseNews(news_repo)
    
    # Filtramos para que solo pasen los campos que realmente se enviaron y no sean None
    update_data = {k: v for k, v in data.model_dump(exclude_unset=True).items() if v is not None}
    
    # Si se envía una nueva imagen, subirla y actualizar el link
    if image:
        img_url = await use_case.upload_image(image, supabase)
        update_data["img_link"] = img_url
        
    # Cambiar campo de schema a dominio
    if "publiC_date" in update_data:
        update_data["date"] = update_data.pop("publiC_date")
    
    response = await use_case.partial_update_new(id, update_data, supabase)
    if not response:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    return response

@router.delete("/{id}", response_model=NewsResponse, summary="Elimina una noticia")
async def delete_news(id: int, supabase: SupabaseDep):
    news_repo = SupabaseNewsRepository()
    use_case = UseNews(news_repo)
    
    response = await use_case.delete_new(id, supabase)
    if not response:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    return response