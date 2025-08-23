from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_file: str = "./vec.db"