from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ollama_model: str
    embedding_model: str
    chroma_db_path: str
    collection_name: str
    top_k: int
    ollama_url: str
    secret_key: str
    access_token_expire_minutes: int
    algorithm: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()