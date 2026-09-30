from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_path: str = 'artifacts/model.joblib'
    database_url: str | None = None
    log_level: str = 'notice'

    model_config = {'env_file': '.env'}

settings = Settings()
