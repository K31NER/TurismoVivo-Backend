from fastapi import FastAPI
from config.db_config import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("Server is started...")
    
    print("Creando las tablas...")
    await init_db()
    print("Tablas creadas con exito")
    
    yield
    
    print("closing the server...")