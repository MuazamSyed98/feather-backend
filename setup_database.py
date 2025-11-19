import sqlite3

# Create database
conn = sqlite3.connect('feather.db')
cursor = conn.cursor()

print("Creating database tables...")

# Create tables one by one
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✓ Created users table")

cursor.execute('''
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    sector VARCHAR(50)
)
''')
print("✓ Created stocks table")

cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker VARCHAR(10) NOT NULL,
    open DECIMAL(10, 2) NOT NULL,
    high DECIMAL(10, 2) NOT NULL,
    low DECIMAL(10, 2) NOT NULL,
    close DECIMAL(10, 2) NOT NULL,
    volume INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticker) REFERENCES stocks(ticker),
    UNIQUE(ticker, timestamp)
)
''')
print("✓ Created stock_data table")

cursor.execute('CREATE INDEX IF NOT EXISTS idx_stock_data_ticker ON stock_data(ticker, timestamp)')

cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker VARCHAR(10) NOT NULL,
    predicted_trend VARCHAR(20) NOT NULL,
    confidence DECIMAL(5, 4) NOT NULL,
    predicted_change DECIMAL(10, 2),
    model_version VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticker) REFERENCES stocks(ticker)
)
''')
print("✓ Created predictions table")

cursor.execute('CREATE INDEX IF NOT EXISTS idx_predictions_ticker ON predictions(ticker, timestamp)')

cursor.execute('''
CREATE TABLE IF NOT EXISTS news_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker VARCHAR(10) NOT NULL,
    headline TEXT NOT NULL,
    summary TEXT,
    content TEXT,
    sentiment VARCHAR(20),
    source VARCHAR(100),
    url TEXT UNIQUE,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticker) REFERENCES stocks(ticker)
)
''')
print("✓ Created news_articles table")

cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_ticker ON news_articles(ticker, published_at)')

cursor.execute('''
CREATE TABLE IF NOT EXISTS watchlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (ticker) REFERENCES stocks(ticker),
    UNIQUE(user_id, ticker)
)
''')
print("✓ Created watchlists table")

cursor.execute('CREATE INDEX IF NOT EXISTS idx_watchlists_user ON watchlists(user_id)')

cursor.execute('''
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    threshold DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (ticker) REFERENCES stocks(ticker)
)
''')
print("✓ Created alerts table")

# Insert sample stocks
stocks = [
    ('AAPL', 'Apple Inc.', 'Technology'),
    ('MSFT', 'Microsoft Corporation', 'Technology'),
    ('GOOGL', 'Alphabet Inc.', 'Technology'),
    ('TSLA', 'Tesla Inc.', 'Automotive'),
    ('NVDA', 'NVIDIA Corporation', 'Technology'),
    ('AMZN', 'Amazon.com Inc.', 'E-commerce')
]

for ticker, name, sector in stocks:
    try:
        cursor.execute('INSERT INTO stocks (ticker, name, sector) VALUES (?, ?, ?)', (ticker, name, sector))
    except sqlite3.IntegrityError:
        pass  # Already exists

print("✓ Inserted sample stocks")

conn.commit()
conn.close()

print("\n" + "="*60)
print("[SUCCESS] Database created: feather.db")
print("="*60)

# Verify
conn = sqlite3.connect('feather.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print(f"\nTables created: {', '.join(tables)}")

cursor.execute("SELECT COUNT(*) FROM stocks")
stock_count = cursor.fetchone()[0]
print(f"Stocks in database: {stock_count}")

conn.close()