from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    FORECAST_PERIODS: int = 6

    model_config = SettingsConfigDict(env_file=".env")
