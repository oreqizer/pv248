# Put SQL ‹load› and ‹store› functions here.

# hw2 │ 25.11. │  2.12. │  9.12. │ 16.12.

import sqlite3


def store(shelter, *, db, deduplicate=False):
    # Init
    sql = open("shelter.sql").read()
    db.executescript(sql)
    # cur = db.cursor()

    # Dedupe
    if deduplicate:
        # TODO load every shelter and try `==` on it
        return "id"

    # === STORE ===

    # Shelter
    insert_shelter(db, shelter)

    # Animals
    for a in shelter.animals:
        a.id = get_animal(db, a)
        if a.id == None:
            insert_animal(db, a)
        insert_shelter_animal(db, shelter, a)


def load(id, *, db):
    pass

# === QUERIES ===


query_insert_shelter = """
--begin-sql
INSERT INTO shelter DEFAULT VALUES
--end-sql
"""


def insert_shelter(db, shelter):
    db.execute(query_insert_shelter)
    db.commit()
    (id,) = db.execute("SELECT last_insert_rowid()").fetchone()
    shelter.id = id


query_get_animal = """
--begin-sql
SELECT id
FROM animal
WHERE name = ?
  AND year_of_birth = ?
  AND gender = ?
  AND species = ?
  AND breed = ?
--end-sql
"""


def get_animal(db, animal):
    res = db.execute(query_get_animal, (animal.name, animal.year_of_birth,
                                        animal.gender, animal.species, animal.breed)).fetchone()
    if res is None:
        return None
    (id,) = res
    return id


query_insert_animal = """
--begin-sql
INSERT INTO animal (name, year_of_birth, gender, species, breed)
VALUES (?, ?, ?, ?, ?)
--end-sql
"""


def insert_animal(db, animal):
    db.execute(query_insert_animal, (animal.name, animal.year_of_birth,
                                     animal.gender, animal.species, animal.breed))
    db.commit()
    (id,) = db.execute("SELECT last_insert_rowid()").fetchone()
    animal.id = id


query_insert_shelter_animal = """
--begin-sql
INSERT INTO shelter_animal (shelter_id, animal_id, date_of_entry)
VALUES (?, ?, ?)
--end-sql
"""


def insert_shelter_animal(db, shelter, animal):
    db.execute(query_insert_shelter_animal,
               (shelter.id, animal.id, animal.date_of_entry))
    db.commit()
