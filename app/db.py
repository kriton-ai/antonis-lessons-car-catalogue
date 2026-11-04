# Create the application and seed (seed.json) it.

# import libraries
import json 
import sqlite3 
# contextmanager: a tool for building our own "with" blocks
# A with bock runs some code automatically before your code (setup)
# and some code automatically after it (cleanup) - even if our code fails
# we use it with connect(): open the database, your code, close it 
from contextlib import contextmanager
from pathlib import Path

# Calculate Paths
APP_DIRECTORY = Path(__file__).resolve().parent # /project/app
PROJECT_ROOT = APP_DIRECTORY.parent # /project
DATABASE_PATH = PROJECT_ROOT / "data" / "catalogue.db" # /projects/data/catalogue.db


# The decorator makes this possible later: with connect() as connection
@contextmanager
def connect():
    """Provide a connection and handle commit, rollback, and cleanup"""

    # if the database file does not exist, SQLite creates it and opens it
    # if it already exists, SQLite opens it
    # the connection object is assigned to the local variable connection inside connect()
    connection = sqlite3.connect(DATABASE_PATH, timeout=10) # timeout 10 tells SQLite how long wait for a database lock before raising error

    # allow access by column: row["value"] 
    connection.row_factory = sqlite3.Row

    # enable foreign key enforcement for this connection
    connection.execute("PRAGMA foreign_keys = ON")

    try:

            with connection: # This is SQLite's own context manager

                # yield provides the connection object to initialize()
                # 4. yield pause connect() here.
                # Allow's the body of initialize()'s with block to run

                yield connection  
                # 6. No extra code to run after yield (-> SQLite commits the write transaction)
                # -> jump to finally to close the connection
                # Remember: yield lets connect() pause while initialize() uses the database
                # then resume to finish transaction and close the connection
    finally:
        # close the db connection -> jump to initialize() and return
        connection.close()
         

def initialize():
    """Create (missing) tables and insert sample only once!"""

    # Create the database directory (data)
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    #read the schema file and save it into Python string
    schema = (APP_DIRECTORY / "schema.sql").read_text(encoding='utf-8')

    #1. connect() creates a context manager object
    #2. Entering the with block starts running original connect() function, UP TO ITS YIELD!
    #3. Execution therefore jumps into connect() above
    with connect() as connection: #5. receives the yielded object under its own local name connection
    
        connection.executescript(schema) # execute schema

        connection.execute("BEGIN IMMEDIATE") #start seeding/writing transaction

        #Is there a metadata row whose key is "seeded"? If so, retrieve its value
        seeded = connection.execute(
            "SELECT value FROM app_metadata WHERE key =?",
            ("seeded", ),
        ).fetchone() # One row, if a matching record exists, None if no record exists

        if seeded is not None:
            return #6. return does not skip the context manager's cleanup. Connect() resumes after yield

        # on the first intiialization, Python reads the sample data
        seed_text = (APP_DIRECTORY / "seed.json").read_text(encoding='utf-8')

        # convert the json string into a python object (list of dicts)
        cars = json.loads(seed_text)

        # Insert cars. One row per car. The "write" part by Begin Immediate
        for car in cars:
            connection.execute(
                """
                INSERT INTO cars (
                name,
                category,
                manufacturer,
                variant,
                description,
                tip
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    car["name"],
                    car["category"],
                    car["manufacturer"],
                    car["variant"],
                    car["description"],
                    car["tip"],
                ),
            )

        connection.execute(
            "INSERT INTO app_metadata (key, value) VALUES(?,?)",
            ("seeded", "1"),
        )

        #6. Execution immediately resumes inside connect(), immediately after yield



if __name__ == "__main__":
    initialize() # 7. Initialize returns
    print(f"DATABASE initialized: {DATABASE_PATH}")


# initialize() enters with connect()
#   connect() opens and confugeres the connection
#   connect() pause at yield
#   initialize() runs its database operations
#   connect() resumes, commits or rolls back, and closes
#   initialize finishes/returns()
# print success
