from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Ecommerce Backend"
    app_description: str = "A backend API for an e-commerce application"
    host: str = "127.0.0.1"  # Server host address
    port: int = 8000  # Server port number
    # ... Add other configuration options as needed


settings = Settings()
