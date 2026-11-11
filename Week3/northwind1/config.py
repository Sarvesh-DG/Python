import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


class Config:
    username = os.getenv("DB_USER", "root")
    password = quote_plus(os.getenv("DB_PASSWORD", ""))
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    database = os.getenv("DB_NAME", "northwind")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False