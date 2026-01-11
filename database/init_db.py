import sqlite3

# connect to (or create) the database file
connection = sqlite3.connect("fasting.db")

# create a cursor object to execute SQL commands
cursor = connection.cursor()

# create table to store daily fasting data
cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    food_intake TEXT,
    activity_level INTEGER CHECK(activity_level BETWEEN 1 AND 10),
    weight REAL NOT NULL,
    bmi REAL NOT NULL
)
""")

# save changes
connection.commit()

# close the database connection
connection.close()

print("Database initialized successfully.")