from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # D:/lidar

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )

    DATABASE_URL: str
    JWT_PRIVATE_KEY_PATH: str = "certs/jwt-private.pem"
    JWT_PUBLIC_KEY_PATH: str = "certs/jwt-public.pem"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()