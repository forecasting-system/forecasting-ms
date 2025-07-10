from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum


class EventServerType(str, Enum):
    NATS = "NATS"


class MessagingServerType(str, Enum):
    NATS = "NATS"
    IN_MEMORY = "IN_MEMORY"


class Settings(BaseSettings):
    NATS_URL: str = "nats://localhost:4222"
    MESSAGING_SERVER: MessagingServerType = MessagingServerType.NATS
    EVENT_SERVER: EventServerType = EventServerType.NATS

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
