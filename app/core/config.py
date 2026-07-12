from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str
    
    ollama_model: str | None = None
    ollama_url: str | None = None
    embedding_model: str
    chroma_db_path: str
    collection_name: str
    top_k: int
    
    secret_key: str
    access_token_expire_minutes: int
    algorithm: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()