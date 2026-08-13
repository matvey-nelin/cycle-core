import os

from dotenv import load_dotenv


class Settings:
    def __init__(self) -> None:
        # load .env file
        load_dotenv()

        # Take DATABASE_URL from .env file
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        if self.DATABASE_URL is None:
            raise ValueError("DATABASE_URL not set in environment")


settings = Settings()
