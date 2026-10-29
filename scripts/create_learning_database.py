import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "learning.db"
DATABASE_PATH.parent.mkdir(parents=True,exist_ok=True)

connection = sqlite3.connect(DATABASE_PATH)

try:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        variant TEXT NOT NULL,
        description TEXT NOT NULL,
        tip TEXT NOT NULL 
        )
        """
    )

    # Explicitly finish any pending transcactions
    connection.commit()
    print(f"Database ready: {DATABASE_PATH}")

finally:
    # Always release / close the connection, even if an operation raises an exception.
    connection.close()

