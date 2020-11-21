CREATE TABLE IF NOT EXISTS shelter (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT);

CREATE TABLE IF NOT EXISTS animal (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    year_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL,
    species TEXT NOT NULL,
    breed TEXT NOT NULL,
    UNIQUE (name, year_of_birth, gender, species, breed)
);

CREATE TABLE IF NOT EXISTS shelter_animal (
    shelter_id INTEGER NOT NULL REFERENCES shelter (id),
    animal_id INTEGER NOT NULL REFERENCES animal (id),
    date_of_entry TEXT NOT NULL,
    PRIMARY KEY (shelter_id, animal_id)
);

CREATE TABLE IF NOT EXISTS foster_parent (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    UNIQUE (name, address, phone_number)
);

CREATE TABLE IF NOT EXISTS shelter_parent (
    shelter_id INTEGER NOT NULL REFERENCES shelter (id),
    parent_id INTEGER NOT NULL REFERENCES foster_parent (id),
    max_animals INTEGER NOT NULL,
    PRIMARY KEY (shelter_id, parent_id)
);

CREATE TABLE IF NOT EXISTS foster (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER NOT NULL REFERENCES shelter_animal (animal_id),
    parent_id INTEGER NOT NULL REFERENCES shelter_parent (parent_id),
    start_date TEXT NOT NULL,
    end_date TEXT
    -- CHECK (
    --     shelter_animal.shelter_id = shelter_parent.shelter_id
    -- )
);

CREATE TABLE IF NOT EXISTS exam (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER NOT NULL REFERENCES animal (id),
    vet TEXT NOT NULL,
    date TEXT NOT NULL,
    report TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS adopter (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    UNIQUE (name, address)
);

CREATE TABLE IF NOT EXISTS adoption (
    animal_id INTEGER NOT NULL REFERENCES animal (id),
    adopter_id INTEGER NOT NULL REFERENCES adopter (id),
    date TEXT NOT NULL,
    PRIMARY KEY (animal_id, adopter_id)
);
