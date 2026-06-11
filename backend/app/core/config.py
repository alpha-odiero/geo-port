import os
from dotenv import load_dotenv

# Search and load local .env if it exists
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./logistics.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "9e7e10826647bc394dd38b81387d834928b97d39a31f79a29e1f57fae1d5a7ef")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))

settings = Settings()
