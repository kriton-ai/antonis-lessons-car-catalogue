-- Create db schema
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY,

    name TEXT NOT NULL
        CHECK(length(trim(name)) BETWEEN 2 AND 50), 

    category TEXT NOT NULL
        CHECK(category IN (
            'Hatchback',
            'Sedan',
            'SUV',
            'Coupe'
        )),

    manufacturer TEXT NOT NULL
        CHECK(length(trim(manufacturer)) BETWEEN 2 AND 50),

    variant TEXT NOT NULL
        CHECK(length(trim(variant)) BETWEEN 3 AND 60),

    description TEXT NOT NULL
        CHECK(length(trim(description)) BETWEEN 20 AND 500),

    tip TEXT NOT NULL
        CHECK(length(trim(tip)) BETWEEN 5 AND 200)
);

-- Record whether initial sample data has already been inserted
-- A two column table: key (a name) and value (its setting).
-- It holds one row, key = 'seeded' , value = '1'. It means "the sample cars have already been added."
-- Setup adds the sample cars only if this row is missing.
CREATE TABLE IF NOT EXISTS app_metadata (
    key TEXT PRIMARY KEY NOT NULL,
    value TEXT NOT NULL
);