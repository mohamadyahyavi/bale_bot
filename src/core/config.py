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
    SECRET_KEY: str

    # -------------------------
    # BALE
    # -------------------------
    BALE_BOT_TOKEN: str | None = None

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