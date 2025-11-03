from flask import Flask
from .config import load_config
from .extensions import cors, build_repo
from .api import register_blueprints

def create_app():
    app = Flask(__name__)
    load_config(app)

    cors.init_app(
        app,
        resources={
            r"/api/*": {"origins": app.config["CORS_ORIGINS_LIST"]},
            r"/health/*": {"origins": app.config["CORS_ORIGINS_LIST"]},   
        },
    )


    app.extensions = getattr(app,  "extensions", {})
    app.extensions["repo"] = build_repo(app.config)


    register_blueprints(app)
    return app