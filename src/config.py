from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str 
    db_file: str = "./vec.db"
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    ) 