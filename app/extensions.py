from flask_cors import CORS
from .services.repository import InMemoryRepository, FileRepository

cors = CORS()

def build_repo(config):
    mode = config.get("PERSIST_MODE", "files")
    if mode == "memory":
        return InMemoryRepository()
    elif mode == "files":
        return FileRepository(base_dir=config.get("DATA_DIR", "./data"))
    else:
        # Add SQL Repository here, when it is set up
        return InMemoryRepository()