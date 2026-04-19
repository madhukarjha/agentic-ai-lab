import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(override=True)

class Settings(BaseSettings):
    # LLM API keys
    openai_api_key: str
    anthropic_api_key: str = ""
    google_api_key: str = ""
    groq_api_key: str = ""
    # Tools
    tavily_api_key: str = ""
    # Notifications
    pushover_user_key: str = ""
    pushover_app_token: str = ""
    # Model defaults
    default_model: str = "gpt-4o-mini"
    default_temperature: float = 0.7
    max_tokens: int = 4096
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

settings = Settings()

# Verify keys loaded
def verify_setup():
    required = ["OPENAI_API_KEY"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise EnvironmentError(f"Missing required env vars: {missing}")
    print("✅ Environment setup complete")
verify_setup()