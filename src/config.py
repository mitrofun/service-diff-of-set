from pydantic import BaseSettings


class Settings(BaseSettings):
    media_dir: str = 'media'
    db_url: str = 'sqlite:///data/db.sqlite3'
    api_key: str = '12345678qwerty'
    api_key_name: str = 'X-API-KEY'
    allow_content: list[str] = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
    ]

    class Config:
        env_file = 'config.env'


settings = Settings()
