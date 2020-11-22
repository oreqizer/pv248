CREATE TABLE IF NOT EXISTS shelter (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT);

CREATE TABLE IF NOT EXISTS animal (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    year_of_birth INT NOT NULL,
    gender TEXT NOT NULL,
    species TEXT NOT NULL,
    breed TEXT NOT NULL,
    UNIQUE (name, year_of_birth, gender, species, breed)
);

CREATE TABLE IF NOT EXISTS shelter_animal (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    shelter_id INTEGER NOT NULL REFERENCES shelter (id),
    animal_id INTEGER NOT NULL REFERENCES animal (id),
    date_of_entry TEXT NOT NULL,
    UNIQUE (shelter_id, animal_id)
);

CREATE TABLE IF NOT EXISTS foster_parent (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    UNIQUE (name, address, phone_number)
);

CREATE TABLE IF NOT EXISTS shelter_parent (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    shelter_id INTEGER NOT NULL REFERENCES shelter (id),
    parent_id INTEGER NOT NULL REFERENCES foster_parent (id),
    max_animals INTEGER NOT NULL,
    UNIQUE (shelter_id, parent_id)
);

CREATE TABLE IF NOT EXISTS foster (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER NOT NULL REFERENCES shelter_animal (id),
    parent_id INTEGER NOT NULL REFERENCES shelter_parent (id),
    start_date TEXT NOT NULL,
    end_date TEXT
    -- CHECK (
    --     shelter_animal.shelter_id = shelter_parent.shelter_id
    -- )
);

CREATE TABLE IF NOT EXISTS exam (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER NOT NULL REFERENCES shelter_animal (id),
    vet TEXT NOT NULL,
    date TEXT NOT NULL,
    report TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS adoption (
    animal_id INTEGER NOT NULL REFERENCES shelter_animal (id) PRIMARY KEY,
    adopter_name TEXT NOT NULL,
    adopter_address TEXT NOT NULL,
    date TEXT NOT NULL
);
