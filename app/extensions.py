from flask_cors import CORS

from .services.repository import InMemoryRepository, FileRepository
from .database import Database

cors = CORS()


def build_repo(config):
    mode = config.get("PERSIST_MODE", "files")
    if mode == "memory":
        return InMemoryRepository()
    elif mode == "files":
        return FileRepository(base_dir=config.get("DATA_DIR", "./data"))
    else:
        # Fallback if config is weird
        return InMemoryRepository()


def build_db(config):
    """Create a Database instance wired to Neon/Postgres."""
    db_url = config.get("DATABASE_URL")
    return Database(db_url=db_url)
