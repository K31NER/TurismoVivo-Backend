from server import lifespan
from api.routers import services
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Turismo vivo Backend",
            lifespan=lifespan,
            version="1.0")

# Definimos un handler para manejar los errores que nos lanze el dominio
@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}, # Usamos 'detail' para estándar FastAPI
    )

# Importamos los routers
app.include_router(services.router)

# Endpoint para validar
@app.get("/health",status_code=200)
async def health():
    return {"message":"Server is runnig..."}