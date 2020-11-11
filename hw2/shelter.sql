CREATE TABLE IF NOT EXISTS shelter (
    id INT NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS animal (
    id INT NOT NULL PRIMARY KEY,

    name TEXT NOT NULL,
    year_of_birth TEXT NOT NULL,
    gender TEXT NOT NULL,
    species TEXT NOT NULL,
    breed TEXT NOT NULL,
    UNIQUE (name, year_of_birth, gender, species, breed)
);

CREATE TABLE IF NOT EXISTS shelter_animal (
    shelter_id INT NOT NULL REFERENCES shelter (id),
    animal_id INT NOT NULL REFERENCES animal (id),
    PRIMARY KEY (shelter_id, animal_id),

    date_of_entry TEXT NOT NULL
)

CREATE TABLE IF NOT EXISTS foster_parent (
    id INT NOT NULL PRIMARY KEY,

    name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    UNIQUE (name, address, phone_number)
);

CREATE TABLE IF NOT EXISTS shelter_parent (
    shelter_id INT NOT NULL REFERENCES shelter (id),
    parent_id INT NOT NULL REFERENCES foster_parent (id),
    PRIMARY KEY (shelter_id, parent_id),

    max_animals INT NOT NULL,
);

CREATE TABLE IF NOT EXISTS foster (
    id INT NOT NULL PRIMARY KEY,

    animal_id INT NOT NULL REFERENCES shelter_animal (animal_id),
    parent_id INT NOT NULL REFERENCES shelter_parent (parent_id),
    CHECK (shelter_animal.shelter_id = shelter_parent.shelter_id),

    start_date TEXT NOT NULL,
    end_date TEXT
);

CREATE TABLE IF NOT EXISTS exam (
    id INT NOT NULL PRIMARY KEY,

    animal_id INT NOT NULL REFERENCES animal (id),

    vet TEXT NOT NULL,
    date TEXT NOT NULL,
    report TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS adopter (
    id INT NOT NULL PRIMARY KEY,

    name TEXT NOT NULL,
    address TEXT NOT NULL,
    UNIQUE (name, address)
);

CREATE TABLE IF NOT EXISTS adoption (
    animal_id INT NOT NULL REFERENCES animal (id),
    adopter_id INT NOT NULL REFERENCES adopter (id),
    PRIMARY KEY (animal_id, adopter_id),

    date TEXT NOT NULL
);