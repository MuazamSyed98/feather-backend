from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import io
import pandas as pd

bp = Blueprint("upload", __name__)


@bp.post("/upload/csv")
def upload_csv():
    """
    Upload a CSV dataset
    ---
    tags:
      - Upload
    summary: Upload a CSV file containing historical stock data
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: "CSV file with historical stock data (e.g. columns: timestamp, open, high, low, close, volume)"
    responses:
      200:
        description: File processed and stored successfully
        schema:
          type: object
          properties:
            dataset_id:
              type: string
              example: "ds_12345"
            summary:
              type: object
              properties:
                rows:
                  type: integer
                  example: 500
                columns:
                  type: array
                  items:
                    type: string
                  example: ["timestamp", "open", "high", "low", "close", "volume"]
                filename:
                  type: string
                  example: "aapl_history.csv"
                preview:
                  type: array
                  items:
                    type: object
      400:
        description: Missing file or invalid CSV
    """
    if "file" not in request.files:
        return jsonify(error="No file part"), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify(error="No selected file"), 400

    filename = secure_filename(f.filename)
    raw = f.read()

    try:
        df = pd.read_csv(io.BytesIO(raw))
    except Exception as e:
        return jsonify(error=f"Failed to parse CSV: {e}"), 400

    preview = df.head(5).to_dict(orient="records")
    meta = {
        "rows": int(df.shape[0]),
        "columns": df.columns.tolist(),
        "filename": filename,
    }

    repo = current_app.extensions["repo"]
    dataset_id = repo.save_dataset(
        name=filename,
        meta=meta,
        rows=df.to_dict(orient="records"),
    )

    return jsonify(dataset_id=dataset_id, summary={**meta, "preview": preview}), 200
