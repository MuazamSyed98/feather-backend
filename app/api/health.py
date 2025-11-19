from flask import Blueprint, jsonify

bp = Blueprint("health", __name__)


@bp.get("/health")
def health():
    """
    Health check endpoint
    ---
    tags:
      - Internal
    summary: Check if the Feather backend is running
    responses:
      200:
        description: Backend is healthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
            service:
              type: string
              example: feather-backend
    """
    return jsonify(status="ok", service="feather-backend"), 200
