import os
from dotenv import load_dotenv

def load_config(app):
    load_dotenv() 

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")

    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    app.config["CORS_ORIGINS_LIST"] = [o.strip() for o in cors_origins if o.strip()]

    mb = float(os.getenv("MAX_CONTENT_LENGTH_MB", "10"))
    app.config["MAX_CONTENT_LENGTH"] = int(mb * 1024 * 1024)

    app.config["PERSIST_MODE"] = os.getenv("PERSIST_MODE", "files").lower()
    app.config["DATA_DIR"] = os.getenv("DATA_DIR", "./data")
