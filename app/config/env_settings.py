from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    
    jwt_secret:str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    algorithm:str
    cipher:str
    hash_length:int
    time_cost:int
    memory_cost:int
    parallelism:int

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
        )

settings = Settings()