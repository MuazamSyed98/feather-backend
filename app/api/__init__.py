from .health import bp as health_bp
from .upload import bp as upload_bp
from flask import Blueprint

def register_blueprints(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(upload_bp, url_prefix="/api/v1")
