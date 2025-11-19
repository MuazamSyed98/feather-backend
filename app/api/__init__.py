from .health import bp as health_bp
from .upload import bp as upload_bp
from .stocks import bp as stocks_bp


def register_blueprints(app):
    """
    Register all API blueprints under the /api prefix.
    Resulting routes:
      - /api/health
      - /api/upload/csv
      - /api/stocks
      - (any other future endpoints)
    """
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(upload_bp, url_prefix="/api")
    app.register_blueprint(stocks_bp, url_prefix="/api")
