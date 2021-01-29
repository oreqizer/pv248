# Put SQL ‹load› and ‹store› functions here.

# hw2 │ 25.11. │  2.12. │  9.12. │ 16.12.

import sqlite3
from datetime import datetime

from shelter import Shelter, Animal, FosterParent, Foster, Adoption, Exam

## As mentioned before I would probably move some code upper, because your init tables are at the bottom of the code
## and it makes harder to read the code. Because I need to scroll up and down a lot.

# === STORE ===


def store(shelter, *, db, deduplicate=False):
    # Init
    db.executescript(ddl_init)

    # Dedupe
    ## There are multiple ways how to deal with deduplicating. You choose a more time consuming one because you
    ## are always creating whole shelters and then comparing them. But you can do it with some SQL code.
    ## Where you don't need to create the whole shelter because if some part of the shelter is different
    ## than store_shelter you can look for another ID. For example, shelter(1) has different animals than store_shelter
    ## you just continue for looking another id. If it's the same you can compare their foster_parents, etc...
    ## You just compare small parts between shelters and if all of them are equal then you can return id.
    ## I hope you understand what I mean.
    ## But still your way it's correct.
    if deduplicate:
        for id in select_shelter_ids(db):
            s = load(id, db=db)
            if shelter == s:
                shelter.id = id
                return id

    # Shelter
    insert_shelter(db, shelter)

    # Foster parents
    for p in shelter.foster_parents:
        insert_foster_parent(db, shelter, p)

    # Animals
    for a in shelter.animals:
        insert_animal(db, shelter, a)

        # Fosters
        for f in a.fosters:
            insert_foster(db, shelter, f)

        # Exams
        for e in a.exams:
            insert_exam(db, a, e)

        # Adoption
        if a.adoption is not None:
            insert_adoption(db, a, a.adoption)

    return shelter.id


# === LOAD ===
## Good and correct SQL codes for selecting obj from db.


query_select_shelter_animals = """
--begin-sql
SELECT id, animal_id, date_of_entry
FROM shelter_animal
WHERE shelter_id = ?
--end-sql
"""

query_select_shelter_parents = """
--begin-sql
SELECT id, parent_id, max_animals
FROM shelter_parent
WHERE shelter_id = ?
--end-sql
"""

query_select_foster_parent = """
--begin-sql
SELECT name, address, phone_number
FROM foster_parent
WHERE id = ?
--end-sql
"""

query_select_animal = """
--begin-sql
SELECT name, year_of_birth, gender, species, breed
FROM animal
WHERE id = ?
--end-sql
"""

query_select_exams = """
--begin-sql
SELECT id, vet, date, report
FROM exam
WHERE animal_id = ?
--end-sql
"""

query_select_fosters = """
--begin-sql
SELECT id, parent_id, start_date, end_date
FROM foster
WHERE animal_id = ?
--end-sql
"""

query_select_adoption = """
--begin-sql
SELECT adopter_name, adopter_address, date
FROM adoption
WHERE animal_id = ?
--end-sql
"""


## As I mentiond before for shelter_json: I have copied text for you ->
## If you passed tests I don't see any problem here, but if not. I can see the problem with appending obj into list,
## like animal.exams.append(exam) instead of using animal.add_exam(). What if somebody give you a wrong db file?
## Maybe I'm wrong but I used add_exam(), start_foster(), end_foster(). Just let me know in review comments what do you
## think about this.
def load(id, *, db):
    shelter = Shelter(id=id)

    foster_parents = {}

    shelter_parents = db.execute(
        query_select_shelter_parents, (shelter.id,)).fetchall()
    for (pid, parent_id, max_animals) in shelter_parents:
        (name, address, phone_number) = db.execute(
            query_select_foster_parent, (parent_id,)).fetchone()
        parent = FosterParent(
            id=pid,
            name=name,
            address=address,
            phone_number=phone_number,
            max_animals=max_animals,
        )
        foster_parents[parent.id] = parent
        shelter.foster_parents.append(parent)

    shelter_animals = db.execute(
        query_select_shelter_animals, (shelter.id,)).fetchall()
    for (aid, animal_id, date_of_entry) in shelter_animals:
        (name, year_of_birth, gender, species, breed) = db.execute(
            query_select_animal, (animal_id,)).fetchone()
        animal = Animal(
            id=aid,
            name=name,
            year_of_birth=year_of_birth,
            gender=gender,
            date_of_entry=datetime.strptime(date_of_entry, "%Y-%m-%d").date(),
            species=species,
            breed=breed,
        )
        exams = db.execute(query_select_exams, (aid,)).fetchall()
        for (exam_id, vet, date, report) in exams:
            exam = Exam(
                id=exam_id,
                vet=vet,
                date=datetime.strptime(date, "%Y-%m-%d").date(),
                report=report,
            )
            animal.exams.append(exam)

        fosters = db.execute(query_select_fosters, (aid,)).fetchall()

        for (foster_id, parent_id, start_date, end_date) in fosters:
            parent = foster_parents[parent_id]
            foster = Foster(
                id=foster_id,
                parent=parent,
                animal=animal,
                start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
                end_date=None if end_date == None else datetime.strptime(end_date, "%Y-%m-%d").date(),
            )
            animal.fosters.append(foster)
            parent.fosters.append(foster)

        adoption = db.execute(query_select_adoption, (aid,)).fetchone()
        if adoption is not None:
            (adopter_name, adopter_address, date) = adoption
            animal.adoption = Adoption(
                id=aid,
                date=datetime.strptime(date, "%Y-%m-%d").date(),
                adopter_name=adopter_name,
                adopter_address=adopter_address,
            )

        shelter.animals.append(animal)

    return shelter


# === QUERIES ===


# Shelter
query_select_shelter_ids = """
--begin-sql
SELECT id
FROM shelter
--end-sql
"""


## Good and correct way of getting shelter ids from db.
def select_shelter_ids(db):
    rows = db.execute(query_select_shelter_ids).fetchall()
    return [id for (id,) in rows]


query_insert_shelter = """
--begin-sql
INSERT INTO shelter DEFAULT VALUES
--end-sql
"""


## Good and correct way for inserting shelter into db.
def insert_shelter(db, shelter):
    db.execute(query_insert_shelter)
    db.commit()
    (id,) = db.execute("SELECT last_insert_rowid()").fetchone()
    shelter.id = id


# Animal
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


query_insert_shelter_animal = """
--begin-sql
INSERT INTO shelter_animal (shelter_id, animal_id, date_of_entry)
VALUES (?, ?, ?)
--end-sql
"""


## Good and correct way of inserting animal into db.
def insert_animal(db, shelter, animal):
    animal_id = get_animal(db, animal)
    if animal_id == None:
        db.execute(query_insert_animal, (animal.name, animal.year_of_birth,
                                         animal.gender, animal.species, animal.breed))
        db.commit()
        (id,) = db.execute("SELECT last_insert_rowid()").fetchone()
        animal_id = id

    db.execute(query_insert_shelter_animal,
               (shelter.id, animal_id, animal.date_of_entry))
    db.commit()
    (id,) = db.execute("SELECT last_insert_rowid()").fetchone()
    animal.id = id


# Foster parent
query_get_foster_parent = """
--begin-sql
SELECT id
FROM foster_parent
WHERE name = ?
  AND address = ?
  AND phone_number = ?
--end-sql
"""


def get_foster_parent(db, parent):
    res = db.execute(query_get_foster_parent, (parent.name,
                                               parent.address, parent.phone_number)).fetchone()
    if res is None:
        return None
    (id,) = res
    return id


query_insert_foster_parent = """
--begin-sql
INSERT INTO foster_parent (name, address, phone_number)
VALUES (?, ?, ?)
--end-sql
"""


query_insert_shelter_foster_parent = """
--begin-sql
INSERT INTO shelter_parent (shelter_id, parent_id, max_animals)
VALUES (?, ?, ?)
--end-sql
"""


## Good and correct way of inserting foster parent into db.
def insert_foster_parent(db, shelter, parent):
    parent_id = get_foster_parent(db, parent)
    if parent_id == None:
        db.execute(query_insert_foster_parent,
                   (parent.name, parent.address, parent.phone_number))
        db.commit()
        (id,) = db.execute("SELECT last_insert_rowid()").fetchone()
        parent_id = id

    db.execute(query_insert_shelter_foster_parent,
               (shelter.id, parent_id, parent.max_animals))
    db.commit()
    (id,) = db.execute("SELECT last_insert_rowid()").fetchone()
    parent.id = id


# Foster
query_insert_foster = """
--begin-sql
INSERT INTO foster (animal_id, parent_id, start_date, end_date)
VALUES (?, ?, ?, ?)
--end-sql
"""


## Good and correct way of inserting foster into db.
def insert_foster(db, shelter, foster):
    db.execute(query_insert_foster, (foster.animal.id, foster.parent.id,
                                     foster.start_date, foster.end_date))
    db.commit()
    (id,) = db.execute("SELECT last_insert_rowid()").fetchone()
    foster.id = id


# Exam
query_insert_exam = """
--begin-sql
INSERT INTO exam (animal_id, vet, date, report)
VALUES (?, ?, ?, ?)
--end-sql
"""


## Good and correct way of inserting exam into db.
def insert_exam(db, animal, exam):
    db.execute(query_insert_exam, (animal.id,
                                   exam.vet, exam.date, exam.report))
    db.commit()
    (id,) = db.execute("SELECT last_insert_rowid()").fetchone()
    exam.id = id


# Adoption
query_insert_adoption = """
--begin-sql
INSERT INTO adoption (animal_id, date, adopter_name, adopter_address)
VALUES (?, ?, ?, ?)
--end-sql
"""


## Good and correct way of inserting adoption.
def insert_adoption(db, animal, adoption):
    db.execute(query_insert_adoption, (animal.id, adoption.date,
                                       adoption.adopter_name, adoption.adopter_address))
    db.commit()
    (id,) = db.execute("SELECT last_insert_rowid()").fetchone()
    adoption.id = id

## Appreciate that you moved date_of_entry into shelter_animal table and didn't keep it in animal table. Same for
## the max_animals for foster parent. Great and correct tables.
# === INIT ===
ddl_init = """
--begin-sql
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
--end-sql
"""