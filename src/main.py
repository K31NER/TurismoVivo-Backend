from server import lifespan
from fastapi import FastAPI, Request
from config.settings import settings
from fastapi.responses import JSONResponse
from api.routers import services, news, courses
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
        title="Turismo vivo Backend",
        summary="API para la plataforma de TurismoVivo que busca centrealizar la informacion turistica",
        lifespan=lifespan,
        debug=False,
        #docs_url=None,
        #redoc_url=None,
        #openapi_url=None, 
        version="1.0")

# Orígenes permitidos 
origins_raw = settings.ORIGINS
ALLOWED_ORIGINS = [origin.strip() for origin in origins_raw.split(",") if origin.strip()]

# Definimos los CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definimos un handler para manejar los errores que nos lanze el dominio
@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}, # Usamos 'detail' para estándar FastAPI
    )

# Importamos los routers
app.include_router(news.router)
app.include_router(courses.router)
app.include_router(services.router)

# Endpoint para validar
@app.get("/health",status_code=200)
async def health():
    return {"message":"Server is runnig..."}