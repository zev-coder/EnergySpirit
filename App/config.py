# THIS FILE IS USED FOR MANAGING HOW THE DB WORKS

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    '''application settings load evirovement'''

    # DATABASE FORMAT, YOU CAN CHANGE DB AS U CAN WITH CERTAIN DB
    DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"

    # Connection Pool Settings
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800

    # Echo sql statement for debugging purpose (disable if production use)
    db_echo: bool = False

    class Config:
        env_file = '.env'

@lru_cache()
def get_settings() -> Settings:
    '''Cache settings to avoid env file leaks'''
    return Settings()


