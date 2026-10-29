import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "learning.db"

if not DATABASE_PATH.exists():
    raise SystemExit("Run scripts/create_learning_database.py first")

connection = sqlite3.connect(DATABASE_PATH)

try:

    values = (
        "Hurricance",
        "Sports",
        "Lamborghini",
        "2 Hybrid Design",
        "A spacious hybrid sports car with supportive seats",
        "Check the driving position",
    )

    cursor = connection.execute(
        """
        INSERT INTO cars(
        name,
        category,
        manufacturer,
        variant,
        description,
        tip
        )
        VALUES(?, ?, ?, ?, ?, ?)
        """,
        values,
    )

    connection.commit()

    print(f"Created car with ID {cursor.lastrowid} ")

except sqlite3.Error:
    # Discard pending changes if a database operation fails
    connection.rollback()
    raise

finally:
    connection.close()