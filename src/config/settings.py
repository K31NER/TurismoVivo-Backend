from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # CORS
    ORIGINS: str
    
    # SUPABASE
    SUPABASE_PROJECT: str
    SUPABASE_API_KEY: str
    SUPABASE_DB_URI: str
    SUPABSE_BUCKET: str
    
    class Config:
        env_file = str(BASE_DIR / ".env")
        
settings = Settings()