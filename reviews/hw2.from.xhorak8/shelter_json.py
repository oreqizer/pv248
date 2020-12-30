## nice code, good formatting and simple approach, I like it
## please, NEVER raise an exception without description
## (o.k. there are cases when it is possible clean design,
## but none will appear in this course for sure)

# Put JSON ‹load› and ‹store› functions here.

# hw2 │ 25.11. │  2.12. │  9.12. │ 16.12.

import json
from datetime import datetime

from shelter import Shelter, Animal, FosterParent, Foster, Exam, Adoption


def format(data):
    return json.dumps(data, indent="  ")


def parse(data):
    return json.loads(data)


## Simple to-string conversion is sufficient, because
## the date string representation is in this default ISO format anyway...
def format_date(d):
    if d is not None:
        return d.strftime("%Y-%m-%d")
    return None


def parse_date(d):
    if d is not None:
        return datetime.strptime(d, "%Y-%m-%d").date()
    return None

# === STORE ===

def store(entity):
    if type(entity) != list:
        if type(entity) == Animal:
            return format(store_animal(entity))

        if type(entity) == FosterParent:
            return format(store_parent(entity))

        ## it would be probably polite to throw here, just
        ## commenting the coding style -> might help later with updates...
    res = []
    for e in entity:
        if type(e) == Animal:
            res.append(store_animal(e))

        if type(e) == FosterParent:
            res.append(store_parent(e))
    return format(res)


## just a small comment on structure here,
## instead of using many lists and partial structures,
## the resulting dictionary can be created using
## more direct approach using intensional lists
##
##cand = {
##        ...
##    "exams": [
##        {
##            "vet": item.vet,
##            "date": item.date,
##            "report": item.report,
##        } for item in animal.exams
##    ],
##   ...
## }
## the advantage is the code then looks almost like
## one json file and the readability is very nice

def store_animal(entity):
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
    return cand


def store_parent(entity):
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
    return cand


# === LOAD ===

def load(str1, str2=None):
    if str1 is None:
        return None

    if type(str2) == str:
        shelter = Shelter()
        r1 = parse(str1)
        r2 = parse(str2)
        for r in r1:
            shelter.animals.append(load_animal(r))
        for r in r2:
            shelter.foster_parents.append(load_parent(r))
        
        # Check fosters
        ## too many for nesting to my liking but...
        ## it seems at least acceptable when considering
        ## that it is direct and simple (no complex conditions...)
        for a in shelter.animals:
            for f in a.fosters:
                for pf in f.parent.fosters:
                    if pf.animal != a:
                        ## please, never raise an exception without
                        ## description - do you know how hard is to
                        ## search for the problem source?
                        ## imagine the wednesday test suite will
                        ## give you message:
                        ## test failed: RuntimeError
                        ## VS
                        ## test failed: RuntimeError("what where went wrong")
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
