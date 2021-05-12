from pydantic import BaseSettings


class Settings(BaseSettings):
    media_dir: str = 'media'
    db_url: str = 'sqlite:///sqlite.db'
    allow_content: list[str] = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
    ]

    class Config:
        env_file = 'config.env'


settings = Settings()
