from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("stocks", __name__)


@bp.get("/stocks")
def list_stocks():
    """
    List all stocks from the database
    ---
    tags:
      - Stocks
    summary: List all tracked tickers
    responses:
      200:
        description: List of stocks currently stored in the database
        schema:
          type: array
          items:
            type: object
            properties:
              ticker:
                type: string
                example: AAPL
              name:
                type: string
                example: Apple Inc.
              exchange:
                type: string
                example: NASDAQ
    """
    db = current_app.extensions["db"]
    stocks = db.get_all_stocks()
    return jsonify(stocks), 200


@bp.get("/stocks/<ticker>/history")
def stock_history(ticker):
    """
    Get recent OHLCV history for a ticker
    ---
    tags:
      - Stocks
    summary: Get recent price history (OHLCV) for a given ticker
    parameters:
      - name: ticker
        in: path
        type: string
        required: true
        description: Stock ticker symbol, e.g. AAPL
      - name: limit
        in: query
        type: integer
        required: false
        default: 30
        description: Number of most recent rows to return
    responses:
      200:
        description: List of OHLCV rows
        schema:
          type: array
          items:
            type: object
            properties:
              timestamp:
                type: string
                example: "2025-11-18T20:00:00Z"
              open:
                type: number
                format: float
                example: 185.0
              high:
                type: number
                format: float
                example: 187.0
              low:
                type: number
                format: float
                example: 184.5
              close:
                type: number
                format: float
                example: 186.2
              volume:
                type: number
                example: 1200345
    """
    db = current_app.extensions["db"]
    limit = int(request.args.get("limit", 30))
    rows = db.get_stock_data(ticker.upper(), limit=limit)
    return jsonify(rows), 200


@bp.get("/stocks/<ticker>/prediction")
def latest_prediction(ticker):
    """
    Get the latest ML prediction for a ticker
    ---
    tags:
      - Predictions
    summary: Get the latest model prediction for a stock
    parameters:
      - name: ticker
        in: path
        type: string
        required: true
        description: Stock ticker symbol, e.g. AAPL
    responses:
      200:
        description: Latest prediction found
        schema:
          type: object
          properties:
            ticker:
              type: string
              example: AAPL
            predicted_price:
              type: number
              format: float
              example: 190.25
            model_name:
              type: string
              example: RF+SVR_ensemble
            horizon_days:
              type: integer
              example: 5
            created_at:
              type: string
              example: "2025-11-18T21:00:00Z"
      404:
        description: No prediction exists for this ticker
        schema:
          type: object
          properties:
            error:
              type: string
              example: No prediction found
    """
    db = current_app.extensions["db"]
    pred = db.get_latest_prediction(ticker.upper())
    if not pred:
        return jsonify(error="No prediction found"), 404
    return jsonify(pred), 200


@bp.get("/stocks/<ticker>/news")
def recent_news(ticker):
    """
    Get recent news for a ticker
    ---
    tags:
      - News
    summary: Return recent news items for the given ticker
    parameters:
      - name: ticker
        in: path
        type: string
        required: true
        description: Stock ticker symbol, e.g. AAPL
      - name: limit
        in: query
        type: integer
        required: false
        default: 5
        description: Maximum number of news items to return
    responses:
      200:
        description: List of recent news stories
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
                example: "Apple shares rise on new product launch"
              published_at:
                type: string
                example: "2025-11-18T19:30:00Z"
              url:
                type: string
                example: "https://example.com/article"
              source:
                type: string
                example: "Bloomberg"
              summary:
                type: string
                example: "Short summary of the article..."
    """
    db = current_app.extensions["db"]
    limit = int(request.args.get("limit", 5))
    news = db.get_recent_news(ticker.upper(), limit=limit)
    return jsonify(news), 200
