"""
Load seed_data.json into database
"""

import json
from database import Database

print("="*60)
print("LOADING SEED DATA INTO DATABASE")
print("="*60)

# Check if seed data exists
try:
    with open('seed_data.json', 'r') as f:
        seed_data = json.load(f)
except FileNotFoundError:
    print("\n[ERROR] seed_data.json not found!")
    print("Run 'python seed_data.py' first to generate it.")
    exit(1)

print(f"\nSeed data contains:")
print(f"  - {len(seed_data['users'])} users")
print(f"  - {len(seed_data['stocks'])} stocks")
print(f"  - {len(seed_data['predictions'])} predictions")
print(f"  - {len(seed_data['news'])} news articles")
print(f"  - {len(seed_data['watchlists'])} watchlists")

# Initialize database
db = Database()

# Insert predictions
print("\nInserting predictions...")
for pred in seed_data['predictions']:
    try:
        db.insert_prediction(pred)
    except Exception as e:
        print(f"  Warning: {e}")

# Insert watchlists
print("\nInserting watchlists...")
for watchlist in seed_data['watchlists']:
    user_id = watchlist['user_id']
    for ticker in watchlist['stocks']:
        try:
            db.add_to_watchlist(user_id, ticker)
        except Exception as e:
            print(f"  Warning: {e}")

print("\n" + "="*60)
print("[SUCCESS] Seed data loaded into database!")
print("="*60)

# Verify
print("\nVerification:")
stocks = db.get_all_stocks()
print(f"  Total stocks: {len(stocks)}")

for ticker in ['AAPL', 'MSFT', 'GOOGL']:
    pred = db.get_latest_prediction(ticker)
    if pred:
        print(f"  {ticker}: {pred['predicted_trend']} ({pred['confidence']*100:.0f}% confidence)")

watchlist = db.get_user_watchlist(1)
print(f"\n  User 1's watchlist: {', '.join([s['ticker'] for s in watchlist])}")