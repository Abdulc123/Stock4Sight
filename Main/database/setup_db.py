import sqlite3

# Connect (creates file if it doesn’t exist)
connection = sqlite3.connect("./Main/database/stock4sight.db")
cursor = connection.cursor()

# Create a table for news sentiment
cursor.execute("""
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    headline TEXT NOT NULL,
    sentiment REAL,
    published DATE
)
""")

# Create a table for trades (For Alpaca Trades)
cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    action TEXT NOT NULL,     -- buy or sell
    qty INTEGER NOT NULL,
    price REAL,
    timestamp DATE DEFAULT CURRENT_TIMESTAMP
)
""")

connection.commit()
connection.close()
print("Database setup complete")
