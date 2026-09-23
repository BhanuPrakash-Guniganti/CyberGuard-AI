from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "CyberGuard AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # Database
    MONGODB_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "cyberguard_ai"
    
    # Auth & Security
    SECRET_KEY: str = "cyberguard_super_secret_jwt_key_2026_demo_soc"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    # AI & LLM Integration
    LLM_PROVIDER: str = "gemini"
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gemini-1.5-flash"
    
    # Incident Correlation & Risk Settings
    CORRELATION_TIME_WINDOW_MINUTES: int = 60
    RISK_THRESHOLD_LOW: int = 30
    RISK_THRESHOLD_MEDIUM: int = 60
    RISK_THRESHOLD_HIGH: int = 80
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
