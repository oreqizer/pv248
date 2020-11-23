# Put JSON ‹load› and ‹store› functions here.

# hw2 │ 25.11. │  2.12. │  9.12. │ 16.12.

import json
from datetime import datetime

from shelter import Shelter, Animal, FosterParent, Foster, Exam, Adoption


def format(data):
    return json.dumps(data, indent="  ")


def parse(data):
    return json.loads(data)


def format_date(d):
    if d is not None:
        return d.strftime("%Y-%m-%d")
    return None


def parse_date(d):
    if d is not None:
        return datetime.strptime(d, "%Y-%m-%d").date()
    return None


def store(entity):
    if type(entity) == Animal:
        exams = []
        adopted = None
        fostering = []
        for e in entity.exams:
            exams.append({
                "vet": e.vet,
                "date": format_date(e.date),
                "report": e.report,
            })
        if entity.adoption is not None:
            adopted = {
                "date": format_date(entity.adoption.date),
                "name": entity.adoption.adopter_name,
                "address": entity.adoption.adopter_address,
            }
        for f in entity.fosters:
            cand = {
                "start": format_date(f.start_date),
                "parent": {
                    "name": f.parent.name,
                    "address": f.parent.address,
                    "phone": f.parent.phone_number,
                },
            }
            if f.end_date is not None:
                cand["end"] = format_date(f.end_date)
            fostering.append(cand)
        cand = {
            "name": entity.name,
            "year_of_birth": entity.year_of_birth,
            "gender": entity.gender,
            "date_of_entry": format_date(entity.date_of_entry),
            "species": entity.species,
            "breed": entity.breed,
            "exams": exams,
            "fostering": fostering,
        }
        if adopted is not None:
            cand["adopted"] = adopted
        return format(cand)

    if type(entity) == FosterParent:
        fostering = []
        for f in entity.fosters:
            cand = {
                "start": format_date(f.start_date),
                "animal": {
                    "name": f.animal.name,
                    "year_of_birth": f.animal.year_of_birth,
                    "gender": f.animal.gender,
                    "date_of_entry": format_date(f.animal.date_of_entry),
                    "species": f.animal.species,
                    "breed": f.animal.breed,
                },
            }
            if f.end_date is not None:
                cand["end"] = format_date(f.end_date)
            fostering.append(cand)
        cand = {
            "name": entity.name,
            "address": entity.address,
            "phone": entity.phone_number,
            "capacity": entity.max_animals,
            "fostering": fostering,
        }
        return format(cand)


def load(str1, str2=None):
    if type(str2) == str:
        shelter = Shelter()
        r1 = parse(str1)
        r2 = parse(str2)
        for r in r1:
            shelter.animals.append(load_animal(r))
        for r in r2:
            shelter.foster_parents.append(load_parent(r))
        
        # Check fosters
        for a in shelter.animals:
            for f in a.fosters:
                for pf in f.parent.fosters:
                    if pf.animal != a:
                        raise RuntimeError

        return shelter

    r = parse(str1)
    if r.get("species") is not None:
        return load_animal(r)

    return load_parent(r)


def load_animal(a):
    animal = Animal(
        name=a["name"],
        year_of_birth=a["year_of_birth"],
        gender=a["gender"],
        date_of_entry=parse_date(a["date_of_entry"]),
        species=a["species"],
        breed=a["breed"],
    )
    for f in a["fostering"]:
        p = f["parent"]
        parent = FosterParent(
            name=p["name"],
            address=p["address"],
            phone_number=p["phone"],
            max_animals=None
        )
        foster = Foster(
            parent=parent,
            animal=animal,
            start_date=parse_date(f["start"]),
            end_date=parse_date(f.get("end")),
        )
        animal.fosters.append(foster)
        parent.fosters.append(foster)
    for e in a["exams"]:
        exam = Exam(
            vet=e["vet"],
            date=parse_date(e["date"]),
            report=e["report"],
        )
        animal.exams.append(exam)
    adopted = a.get("adopted")
    if adopted is not None:
        adoption = Adoption(
            date=parse_date(adopted["date"]),
            adopter_name=adopted["name"],
            adopter_address=adopted["address"],
        )
        animal.adoption = adoption
    return animal


def load_parent(p):
    parent = FosterParent(
        name=p["name"],
        address=p["address"],
        phone_number=p["phone"],
        max_animals=p["capacity"],
    )
    for f in p["fostering"]:
        a = f["animal"]
        animal = Animal(
            name=a["name"],
            year_of_birth=a["year_of_birth"],
            gender=a["gender"],
            date_of_entry=parse_date(a["date_of_entry"]),
            species=a["species"],
            breed=a["breed"],
        )
        foster = Foster(
            parent=parent,
            animal=animal,
            start_date=parse_date(f["start"]),
            end_date=parse_date(f.get("end")),
        )
        animal.fosters.append(foster)
        parent.fosters.append(foster)
    return parent
