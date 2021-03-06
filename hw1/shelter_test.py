from datetime import timedelta, date

from shelter import Exam, Adoption, FosterParent, Foster, Animal, Shelter


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


def make_foster(*, parent=make_parent(), start_date=date.today(), end_date=None):
    return Foster(
        parent=parent,
        start_date=start_date,
        end_date=end_date,
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


def test_exam():
    exam = make_exam()

    assert type(exam.vet) == str
    assert type(exam.date) == date
    assert type(exam.report) == str


def test_adoption():
    adoption = make_adoption()

    assert type(adoption.date) == date
    assert type(adoption.adopter_name) == str
    assert type(adoption.adopter_address) == str


def test_foster_parent():
    parent = make_parent()

    assert type(parent.name) == str
    assert type(parent.address) == str
    assert type(parent.phone_number) == str
    assert type(parent.max_animals) == int
    assert type(parent.fosters) == list

    now = date.today()
    assert parent.has_animals(date=now) == 0
    assert parent.is_available(date=now)

    foster = Foster(parent=parent, start_date=now - timedelta(days=1))
    parent.fosters.append(foster)
    assert parent.has_animals(date=now) == 1
    assert not parent.is_available(date=now)

    foster.end_date = now
    assert parent.has_animals(date=now + timedelta(days=1)) == 0
    assert parent.is_available(date=now + timedelta(days=1))


def test_foster():
    now = date.today()
    parent = FosterParent(name="Kek", address="Bur 1337",
                          phone_number="13371337", max_animals=1)
    foster = Foster(parent=parent, start_date=now)

    assert type(foster.parent) == FosterParent
    assert type(foster.start_date) == date
    assert type(foster.end_date) == type(None)

    assert foster.is_colliding(date=now + timedelta(days=1))
    assert not foster.is_colliding(date=now - timedelta(days=1))

    foster.end_date = now + timedelta(days=2)
    assert foster.is_colliding(date=now + timedelta(days=1))
    assert not foster.is_colliding(date=now + timedelta(days=3))


def test_animal():
    animal = make_animal()

    assert type(animal.name) == str
    assert type(animal.year_of_birth) == int
    assert type(animal.gender) == str
    assert type(animal.date_of_entry) == date
    assert type(animal.species) == str
    assert type(animal.breed) == str
    assert type(animal.exams) == list
    assert type(animal.adoption) == type(None)
    assert type(animal.foster) == type(None)
    assert type(animal.past_fosters) == list

    now = date.today()

    # add_exam
    animal = make_animal()
    animal.add_exam(vet="Kekega", date=now, report="OK")

    assert len(animal.exams) == 1
    assert animal.exams[0].vet == "Kekega"

    animal = make_animal()
    animal.adoption = make_adoption()
    try:
        animal.add_exam(vet="Kekega", date=now, report="OK")
        assert False
    except RuntimeError as err:
        assert str(err) == "cannot do an exam on an unavailable animal"

    animal = make_animal()
    animal.foster = make_foster()
    try:
        animal.add_exam(vet="Kekega", date=now, report="OK")
        assert False
    except RuntimeError as err:
        assert str(err) == "cannot do an exam on an unavailable animal"

    # list_exams
    animal = make_animal()
    animal.add_exam(vet="Kekega", date=now, report="OK")
    animal.add_exam(vet="Kekega", date=now + timedelta(days=2), report="OK")

    assert len(animal.list_exams(start=now)) == 2
    assert len(animal.list_exams(start=now + timedelta(days=1))) == 1
    assert len(animal.list_exams(start=now + timedelta(days=3))) == 0
    assert len(animal.list_exams(end=now - timedelta(days=1))) == 0
    assert len(animal.list_exams(end=now + timedelta(days=1))) == 1
    assert len(animal.list_exams(end=now + timedelta(days=3))) == 2
    assert len(animal.list_exams(start=now, end=now + timedelta(days=2))) == 2
    assert len(animal.list_exams(start=now, end=now + timedelta(days=1))) == 1
    assert len(animal.list_exams(start=now + timedelta(days=1),
               end=now + timedelta(days=2))) == 1
    assert len(animal.list_exams(start=now + timedelta(days=3),
               end=now + timedelta(days=4))) == 0

    # adopt
    animal = make_animal()
    animal.adopt(date=now, adopter_name="Kek", adopter_address="Bar 1337")

    assert type(animal.adoption) == Adoption

    try:
        animal.adopt(date=now, adopter_name="Kek", adopter_address="Bar 1337")
        assert False
    except RuntimeError as err:
        assert str(err) == "cannot adopt an unavailable animal"

    animal = make_animal()
    animal.start_foster(date=now - timedelta(days=1), parent=make_parent())
    animal.end_foster(date=now + timedelta(days=1))
    try:
        animal.adopt(date=now, adopter_name="Kek", adopter_address="Bar 1337")
        assert False
    except RuntimeError as err:
        assert str(err) == "cannot adopt an unavailable animal"

    # start_foster
    animal = make_animal()
    parent = make_parent(max_animals=5)
    animal.start_foster(date=now, parent=parent)

    assert type(animal.foster) == Foster
    assert len(animal.past_fosters) == 0

    animal = make_animal()
    animal.adopt(date=now, adopter_name="Lol", adopter_address="Bur 1337")
    animal.start_foster(date=now - timedelta(days=1), parent=parent)
    try:
        animal.start_foster(date=now, parent=parent)
        assert False
    except RuntimeError as err:
        assert str(err) == "cannot foster an unavailable animal"

    animal = make_animal()
    parent = make_parent(max_animals=5)
    animal.start_foster(date=now, parent=parent)
    animal.start_foster(date=now - timedelta(days=1), parent=parent)
    try:
        animal.start_foster(date=now + timedelta(days=1), parent=parent)
        assert False
    except RuntimeError as err:
        assert str(err) == "cannot foster an unavailable animal"

    animal = make_animal()
    parent = make_parent(max_animals=1)
    parent.fosters = [make_foster(start_date=now)]
    try:
        animal.start_foster(date=now, parent=parent)
        assert False
    except RuntimeError as err:
        assert str(err) == "cannot foster by a parent with full capacity"
    finally:
        parent.fosters = []

    # end_foster
    animal = make_animal()
    animal.foster = make_foster(start_date=now)
    animal.end_foster(date=now + timedelta(days=1))

    assert len(animal.past_fosters) == 1
    assert animal.foster == None

    animal = make_animal()
    animal.adoption = make_adoption()
    try:
        animal.end_foster(date=now + timedelta(days=1))
        assert False
    except RuntimeError as err:
        assert str(err) == "cannot end foster on an adopted animal"

    animal = make_animal()
    try:
        animal.end_foster(date=now + timedelta(days=1))
        assert False
    except RuntimeError as err:
        assert str(err) == "cannot end foster on an unfostered animal"

    # is_available
    animal = make_animal(date_of_entry=now - timedelta(days=9))

    assert animal.is_available(date=now)
    assert not animal.is_available(date=now - timedelta(days=10))

    animal.adoption = make_adoption(date=now)

    assert not animal.is_available(date=now)
    assert animal.is_available(date=now - timedelta(days=1))

    animal = make_animal()
    animal.foster = make_foster(start_date=now)

    assert not animal.is_available(date=now)
    assert animal.is_available(date=now - timedelta(days=1))

    animal = make_animal()
    animal.past_fosters = [make_foster(
        start_date=now, end_date=now + timedelta(days=1))]

    assert not animal.is_available(date=now)
    assert animal.is_available(date=now + timedelta(days=2))
    assert animal.is_available(date=now - timedelta(days=1))


def test_shelter():
    s = Shelter()
    now = date.today()

    # add_animal
    res = s.add_animal(name="Doz", year_of_birth=2000, gender="Male",
                       date_of_entry=now - timedelta(days=200), species="Dog", breed="Staff")

    assert type(res) == Animal
    assert len(s.animals) == 1

    res = s.add_animal(name="Doz2", year_of_birth=1992, gender="Female",
                       date_of_entry=now - timedelta(days=200), species="Doge", breed="Staffe")

    assert type(res) == Animal
    assert len(s.animals) == 2

    # list_animals
    assert len(s.list_animals(date=now, )) == 2
    assert len(s.list_animals(date=now, name="Doz")) == 1
    assert len(s.list_animals(date=now, name="Doz2")) == 1
    assert len(s.list_animals(date=now, name="Dozzzz")) == 0
    assert len(s.list_animals(date=now, year_of_birth=2000)) == 1
    assert len(s.list_animals(date=now, year_of_birth=1992)) == 1
    assert len(s.list_animals(date=now, year_of_birth=1337)) == 0
    assert len(s.list_animals(date=now, gender="Male")) == 1
    assert len(s.list_animals(date=now, gender="Female")) == 1
    assert len(s.list_animals(date=now, gender="Hybrid")) == 0
    assert len(s.list_animals(date=now, date_of_entry=now - timedelta(days=200))) == 2
    assert len(s.list_animals(date=now, date_of_entry=now)) == 0
    assert len(s.list_animals(date=now, species="Dog")) == 1
    assert len(s.list_animals(date=now, species="Doge")) == 1
    assert len(s.list_animals(date=now, species="Dog3")) == 0
    assert len(s.list_animals(date=now, breed="Staff")) == 1
    assert len(s.list_animals(date=now, breed="Staffe")) == 1
    assert len(s.list_animals(date=now, breed="Staff3")) == 0

    doz = s.list_animals(date=now, name="Doz")[0]
    doz.adopt(date=now, adopter_name="Kek", adopter_address="Bur 1337")

    assert len(s.list_animals(date=now - timedelta(days=1))) == 2
    assert len(s.list_animals(date=now)) == 1

    # add_foster_parent
    p = s.add_foster_parent(name="Kek", address="Bur 1337",
                            phone_number="13371337", max_animals=1)

    assert type(p) == FosterParent
    assert len(s.foster_parents) == 1

    # available_foster_parents
    assert len(s.available_foster_parents(date=now)) == 1

    p.fosters = [make_foster(start_date=now)]

    assert len(s.available_foster_parents(date=now)) == 0

if __name__ == "__main__":
    test_exam()
    test_adoption()
    test_foster_parent()
    test_foster()
    test_animal()
    test_shelter()
