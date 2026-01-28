from fastapi import Depends
from sqlmodel import SQLModel
from config.settings import settings
from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


# Crear el motor asíncrono
engine = create_async_engine(settings.SUPABASE_DB_URI, echo=True)

# Creamos la session asincrona
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Generador de dependencias para obtener la sesión
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Definición del tipo Annotated para inyección de dependencias en endpoints
SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def init_db():
    """ Inicializa las base de datos"""
    # Importamos los modelos
    from infrastructure.database.models.services import Services
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        raise ConnectionError(f"Error al inicializar la base de datos: {e}")