from flask import Flask
from flasgger import Swagger  # NEW, added swagger

from .config import load_config
from .extensions import cors, build_repo, build_db
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

    # Custom extensions registry
    app.extensions = getattr(app, "extensions", {})
    app.extensions["repo"] = build_repo(app.config)
    app.extensions["db"] = build_db(app.config)

    # --- Swagger setup ---
    swagger_template = {
        "info": {
            "title": "Feather API",
            "description": (
                "API for Feather: stocks, historical OHLCV, ML predictions, "
                "news, and dataset uploads."
            ),
            "version": "1.0.0",
        },
        # your blueprints are all registered under /api
        "basePath": "/api",
        "schemes": ["https", "http"],
    }
    Swagger(app, template=swagger_template)
    # ---------------------

    register_blueprints(app)
    return app
