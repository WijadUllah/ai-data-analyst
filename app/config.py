
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Data Analyst"
    app_env: str = "development"

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "ai_data_analyst"
    db_user: str = "postgres"
    db_password: str

    # Groq configuration
    groq_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()