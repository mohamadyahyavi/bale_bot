from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # -------------------------
    # DATABASE
    # -------------------------
    DATABASE_URL: str

    # -------------------------
    # APP
    # -------------------------
    APP_NAME: str = "bale-bot"
    ENV: str = "development"
    DEBUG: bool = False

    # -------------------------
    # SECURITY (future use)
    # -------------------------
    

    # -------------------------
    # BALE
    # -------------------------
    BALE_API_URL: str
    BALE_BOT_TOKEN: str 

    # -------------------------
    # KIMAI
    # -------------------------
    KIMAI_BASE_URL: str | None = None
    KIMAI_API_KEY: str | None = None

    # -------------------------
    # NOTIFICATIONS
    # -------------------------
    NOTIFICATION_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()