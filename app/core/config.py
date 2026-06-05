from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    LOG_LEVEL: str = "INFO"
    model_config = SettingsConfigDict(
        env_file="app/.env"
    )
    REDIS_HOST: str
    REDIS_PORT: int

settings = Settings() # type: ignore