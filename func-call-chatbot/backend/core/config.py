from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    SUPABASE_KEY: str
    SUPABASE_URL: str
   
    API_PREFIX: str
    DEBUG: bool
    ALLOWED_ORIGINS: str

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",") if v else []
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_senstive = True

settings = Settings()