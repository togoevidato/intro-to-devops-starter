import os


def get_database_url() -> str:
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "3306")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not host or not name or not user or not password:
        return "sqlite:///./fruitapi.db"

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"