from datetime import timedelta, date
import sqlite3

from shelter import Exam, Adoption, FosterParent, Foster, Animal, Shelter
from shelter_sql import store, load
import shelter_json as sj


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


def test():
    shelter = Shelter()
    now = date.today()
    day = timedelta(days=1)

    # add_animal
    a1 = shelter.add_animal(name="Doz", year_of_birth=2000, gender="Male",
                            date_of_entry=now - day*200, species="Dog", breed="Staff")

    a1.add_exam(vet="Kekega", date=now - day, report="OK")
    a1.add_exam(vet="Kekega", date=now, report="OK")

    res = shelter.add_animal(name="Doz", year_of_birth=2000, gender="Male",
                             date_of_entry=now - day*200, species="Dog", breed="Staff")
    assert a1 == res, f"{a1} == {res}"
    assert a1 is res, f"{a1} is {res}"

    a2 = shelter.add_animal(name="Doz2", year_of_birth=1992, gender="Female",
                            date_of_entry=now - day*200, species="Doge", breed="Staffe")

    a2.add_exam(vet="Kekega", date=now - day, report="OK")
    a2.add_exam(vet="Kekega", date=now, report="OK")

    a3 = shelter.add_animal(name="Doz3", year_of_birth=1992, gender="Female",
                            date_of_entry=now - day*200, species="Dogee", breed="Staffe")

    a3.add_exam(vet="Kekega", date=now - day, report="OK")

    # add_foster_parent
    fp1 = shelter.add_foster_parent(name="Kek", address="Bur 1337",
                                    phone_number="13371337", max_animals=3)

    a1.start_foster(date=now - day*2, parent=fp1)
    a1.end_foster(date=now - day)
    a1.adopt(date=now, adopter_name="Kek", adopter_address="Lol")

    res = shelter.add_foster_parent(name="Kek", address="Bur 1337",
                                    phone_number="13371337", max_animals=3)
    assert fp1 == res, f"{fp1} == {res}"
    assert fp1 is res, f"{fp1} is {res}"

    fp2 = shelter.add_foster_parent(name="Kek2", address="Bur 1337",
                                    phone_number="13371337", max_animals=3)

    a2.start_foster(date=now - day, parent=fp2)
    a3.start_foster(date=now - day, parent=fp2)

    # === SQL ===
    db = sqlite3.connect(':memory:')
    db.execute("PRAGMA foreign_keys = on")

    id_ = store(shelter, db=db)
    shelter_2 = load(id_, db=db)
    id_2 = store(shelter_2, db=db, deduplicate=True)
    id_3 = store(shelter, db=db, deduplicate=True)

    assert id_ == id_2, f"{id_} == {id_2}"
    assert id_ == id_3, f"{id_} == {id_3}"

    # === JSON ===
    res = sj.load(sj.store(a1))
    assert res == a1, f"{res} == {a1}"

    res = sj.load(sj.store(fp1))
    assert res == fp1, f"{res} == {fp1}"

    a_jsons = []
    for a in shelter.animals:
        j = sj.store(a)
        res = sj.load(j)
        a_jsons.append(sj.parse(j))
        assert res == a, f"{res} == {a}"

    p_jsons = []
    for p in shelter.foster_parents:
        j = sj.store(p)
        res = sj.load(j)
        p_jsons.append(sj.parse(j))
        assert res == p, f"{res} == {p}"

    sj.store(shelter.animals)
    sj.store(shelter.foster_parents)

    res = sj.load(sj.format(a_jsons), sj.format(p_jsons))
    assert res == shelter, f"{res} == {shelter}"

    # === e2e ===
    res = load(store(res, db=db, deduplicate=True), db=db)
    assert res == shelter, f"{res} == {shelter}"

    print("OK")


if __name__ == "__main__":
    test()
