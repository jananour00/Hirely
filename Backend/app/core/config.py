from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = "Hirely"
    app_env: str = "development"
    app_debug: bool = True
<<<<<<< HEAD
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-6"

    # Agent LLM provider — which backend the agents/* modules call.
    # "groq" | "openrouter" | "anthropic"
    llm_provider: str = "groq"

    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    openrouter_api_key: str = ""
    openrouter_model: str = "meta-llama/llama-3.3-70b-instruct"

=======
    anthropic_api_key: str
    anthropic_model: str = "claude-sonnet-4-6"

>>>>>>> 11370235c04fdecb3e197487b0bee4d61e3b868a
    database_url: str
    redis_url: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()