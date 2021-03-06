from datetime import timedelta, date
import sqlite3

from shelter import Exam, Adoption, FosterParent, Foster, Animal, Shelter
from shelter_sql import store, load
import shelter_json


def make_exam(*, vet="kek", date=date.today(), report="good"):
    return Exam(
        vet=vet,
        date=date,
        report=report,
    )


def make_adoption(*, date=date.today(), adopter_name="Kek", adopter_address="Bur 1337"):
    return Adoption(
        date=date,
        adopter_name=adopter_name,
        adopter_address=adopter_address,
    )


def make_parent(*, name="Kek", address="Bur 1337", phone_number="13371337", max_animals=1):
    return FosterParent(
        name=name,
        address=address,
        phone_number=phone_number,
        max_animals=max_animals,
    )


def make_animal(*, name="Doz", year_of_birth=2000, gender="Male", date_of_entry=date.today() - timedelta(days=200), species="Dog", breed="Staff"):
    return Animal(
        name=name,
        year_of_birth=year_of_birth,
        gender=gender,
        date_of_entry=date_of_entry,
        species=species,
        breed=breed,
    )


def make_foster(*, parent=make_parent(), animal=make_animal(), start_date=date.today(), end_date=None):
    return Foster(
        parent=parent,
        animal=animal,
        start_date=start_date,
        end_date=end_date,
    )


def test_shelter():
    s1 = Shelter()
    s1d = Shelter()
    s2 = Shelter()
    now = date.today()

    # add_animal
    s1.add_animal(name="Doz", year_of_birth=2000, gender="Male",
                  date_of_entry=now - timedelta(days=200), species="Dog", breed="Staff")

    s1.add_animal(name="Doz2", year_of_birth=1992, gender="Female",
                       date_of_entry=now - timedelta(days=200), species="Doge", breed="Staffe")

    s1d.add_animal(name="Doz", year_of_birth=2000, gender="Male",
                   date_of_entry=now - timedelta(days=200), species="Dog", breed="Staff")

    s1d.add_animal(name="Doz2", year_of_birth=1992, gender="Female",
                   date_of_entry=now - timedelta(days=200), species="Doge", breed="Staffe")

    s2.add_animal(name="Doz", year_of_birth=2000, gender="Male",
                  date_of_entry=now - timedelta(days=100), species="Dog", breed="Staff")

    s2.add_animal(name="Doz2", year_of_birth=1992, gender="Female",
                       date_of_entry=now - timedelta(days=100), species="Doge", breed="Staffe")

    # add_foster_parent
    fp1 = s1.add_foster_parent(name="Kek", address="Bur 1337",
                               phone_number="13371337", max_animals=1)

    s1d.add_foster_parent(name="Kek", address="Bur 1337",
                               phone_number="13371337", max_animals=1)

    fp2 = s2.add_foster_parent(name="Kek2", address="Bur",
                               phone_number="13371337", max_animals=2)

    s2.add_foster_parent(name="Kek", address="Bur 1337",
                         phone_number="13371337", max_animals=2)

    for a in s1.animals:
        a.fosters = [make_foster(parent=fp1, animal=a)]
        fp1.fosters = [make_foster(parent=fp1, animal=a)]
        a.exams = [make_exam()]
        a.adoption = make_adoption()

    for a in s1d.animals:
        a.fosters = [make_foster(parent=fp1, animal=a)]
        fp1.fosters = [make_foster(parent=fp1, animal=a)]
        a.exams = [make_exam()]
        a.adoption = make_adoption()

    for a in s2.animals:
        a.fosters = [make_foster(parent=fp2, animal=a)]
        fp2.fosters = [make_foster(parent=fp2, animal=a)]
        a.exams = [make_exam()]

    # === SQL ===
    db = sqlite3.connect(':memory:')
    db.execute("PRAGMA foreign_keys = on")

    store(s1, db=db)
    store(s1d, db=db, deduplicate=True)
    store(s2, db=db)

    assert s1 == s1d
    assert s1.id == s1d.id

    s1l = load(s1.id, db=db)

    assert s1 == s1l

    db.close()

    # === JSON ===
    a_jsons = []
    for a in s1.animals:
        j = shelter_json.store(a)
        res = shelter_json.load(j)
        a_jsons.append(shelter_json.parse(j))
        assert res == a

    p_jsons = []
    for p in s1.foster_parents:
        j = shelter_json.store(p)
        res = shelter_json.load(j)
        p_jsons.append(shelter_json.parse(j))
        assert res == p

    s_res = shelter_json.load(shelter_json.format(a_jsons), shelter_json.format(p_jsons))
    assert s_res == s1


if __name__ == "__main__":
    test_shelter()
