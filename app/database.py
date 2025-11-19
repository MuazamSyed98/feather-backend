"""
Database manager for Feather Finance App (Neon PostgreSQL version)
"""

import os
from contextlib import contextmanager

import psycopg2
import psycopg2.extras


class Database:
    """PostgreSQL database wrapper for Neon"""

    def __init__(self, db_url: str | None = None):
        self.db_url = db_url or os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL is not set")

        # Print a safe, shortened identifier so you can see it's using Neon
        safe = self.db_url.split("@")[-1]
        safe = safe.split("?")[0]
        print(f"[OK] Database initialized (Neon Postgres): {safe}")

    @contextmanager
    def get_connection(self):
        """Safe database connection with automatic commit/rollback"""
        conn = psycopg2.connect(self.db_url)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] {e}")
            raise
        finally:
            conn.close()

    def _dict_cursor(self, conn):
        return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # ============================================
    # INSERT FUNCTIONS
    # ============================================

    def insert_stock_data(self, data):
        """
        Insert stock OHLCV data
        """
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO stock_data
                    (ticker, open, high, low, close, volume, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ticker, timestamp) DO NOTHING
                RETURNING id
                """,
                (
                    data["ticker"],
                    data["open"],
                    data["high"],
                    data["low"],
                    data["close"],
                    data["volume"],
                    data["timestamp"],
                ),
            )
            row = cur.fetchone()
            print(f"[OK] Inserted stock data for {data['ticker']}")
            return row["id"] if row else None

    def insert_prediction(self, prediction):
        """
        Insert ML prediction
        """
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO predictions
                    (ticker, predicted_trend, confidence,
                     predicted_change, model_version)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    prediction["ticker"],
                    prediction["predicted_trend"],
                    prediction["confidence"],
                    prediction.get("predicted_change"),
                    prediction["model_version"],
                ),
            )
            row = cur.fetchone()
            print(f"[OK] Inserted prediction for {prediction['ticker']}")
            return row["id"]

    def insert_news_article(self, article):
        """
        Insert news article
        """
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO news_articles
                    (ticker, headline, summary, sentiment, source, url)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING
                RETURNING id
                """,
                (
                    article["ticker"],
                    article["headline"],
                    article.get("summary"),
                    article.get("sentiment"),
                    article.get("source"),
                    article.get("url"),
                ),
            )
            row = cur.fetchone()
            print(f"[OK] Inserted news: {article['headline'][:50]}...")
            return row["id"] if row else None

    def add_to_watchlist(self, user_id, ticker):
        """
        Add stock to user's watchlist
        """
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO watchlists (user_id, ticker)
                VALUES (%s, %s)
                ON CONFLICT (user_id, ticker) DO NOTHING
                RETURNING id
                """,
                (user_id, ticker),
            )
            row = cur.fetchone()
            print(f"[OK] Added {ticker} to user {user_id}'s watchlist")
            return row["id"] if row else None

    # ============================================
    # QUERY FUNCTIONS
    # ============================================

    def get_stock_data(self, ticker, limit=30):
        """
        Get historical stock data for a ticker
        """
        with self.get_connection() as conn:
            cur = self._dict_cursor(conn)
            cur.execute(
                """
                SELECT *
                FROM stock_data
                WHERE ticker = %s
                ORDER BY timestamp DESC
                LIMIT %s
                """,
                (ticker, limit),
            )
            rows = cur.fetchall()
            return rows

    def get_latest_prediction(self, ticker):
        """
        Get most recent prediction for a stock
        """
        with self.get_connection() as conn:
            cur = self._dict_cursor(conn)
            cur.execute(
                """
                SELECT *
                FROM predictions
                WHERE ticker = %s
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (ticker,),
            )
            row = cur.fetchone()
            return row if row else None

    def get_user_watchlist(self, user_id):
        """
        Get all stocks in user's watchlist
        """
        with self.get_connection() as conn:
            cur = self._dict_cursor(conn)
            cur.execute(
                """
                SELECT w.ticker, s.name, s.sector, w.added_at
                FROM watchlists w
                JOIN stocks s ON w.ticker = s.ticker
                WHERE w.user_id = %s
                ORDER BY w.added_at DESC
                """,
                (user_id,),
            )
            rows = cur.fetchall()
            return rows

    def get_recent_news(self, ticker, limit=5):
        """
        Get recent news for a stock
        """
        with self.get_connection() as conn:
            cur = self._dict_cursor(conn)
            cur.execute(
                """
                SELECT *
                FROM news_articles
                WHERE ticker = %s
                ORDER BY published_at DESC NULLS LAST, created_at DESC
                LIMIT %s
                """,
                (ticker, limit),
            )
            rows = cur.fetchall()
            return rows

    def get_all_stocks(self):
        """
        Get list of all stocks in database
        """
        with self.get_connection() as conn:
            cur = self._dict_cursor(conn)
            cur.execute("SELECT * FROM stocks ORDER BY ticker")
            rows = cur.fetchall()
            return rows
