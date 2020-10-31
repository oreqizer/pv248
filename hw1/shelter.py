# Write your solution into this file.
class Exam:
    def __init__(self, *, vet, date, report):
        self.vet = vet
        self.date = date
        self.report = report

    def __repr__(self):
        return "Exam(vet={vet}, date={date})".format(vet=self.vet, date=self.date)

class Adoption:
    def __init__(self, *, date, adopter_name, adopter_address):
        self.date = date
        self.adopter_name = adopter_name
        self.adopter_address = adopter_address

    def __repr__(self):
        return "Adoption(date={date})".format(date=self.date)

class FosterParent:
    def __init__(self, *, name, address, phone_number, max_animals):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.max_animals = max_animals
        self.fosters = []

    def __repr__(self):
        return "FosterParent(name={name}, fosters={fosters})".format(name=self.name, fosters=self.fosters)

    def has_animals(self, *, date):
        return len([f for f in self.fosters if f.is_colliding(date=date)])

    def is_available(self, *, date):
        collisions = 0
        for f in self.fosters:
            if f.is_colliding(date=date):
                collisions += 1
        return collisions < self.max_animals

class Foster:
    def __init__(self, *, parent, start_date, end_date=None):
        self.parent = parent
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return "Foster(parent.name={name}, start_date={start}, end_date={end})".format(name=self.parent.name, start=self.start_date, end=self.end_date)

    def is_colliding(self, *, date):
        if self.start_date <= date and (self.end_date == None or self.end_date >= date):
            return True
        return False

class Animal:
    def __init__(self, *, name, year_of_birth, gender, date_of_entry, species, breed):
        """
        each of the basic stats as an attribute of the corresponding
        type (see ‹add_animal›),
        """
        self.name = name
        self.year_of_birth = year_of_birth
        self.gender = gender
        self.date_of_entry = date_of_entry
        self.species = species
        self.breed = breed
        self.exams = []
        self.adoption = None
        self.foster = None
        self.past_fosters = []

    def __repr__(self):
        return "Animal(name={name})".format(name=self.name)

    def add_exam(self, *, vet, date, report):
        """
        ◦ method ‹add_exam› which accepts keyword arguments ‹vet› and
            ‹date› and ‹report›, where ‹vet› and ‹report› are strings and
            ‹date› is a ‹datetime.date› instance,
        """
        if not self.is_available(date=date):
            raise RuntimeError("cannot do an exam on an unavailable animal")

        exam = Exam(
            vet=vet,
            date=date,
            report=report,
        )

        self.exams.append(exam)
        return exam

    def list_exams(self, *, start=None, end=None):
        """
        ◦ method ‹list_exams› which takes keyword arguments ‹start› and
            ‹end›, both ‹datetime.date› instances, or ‹None› (the range is
            inclusive; in the latter case, the range is not limited in
            that direction),
        """
        return [e for e in self.exams if
                (start == None or start <= e.date) and
                (end == None or end >= e.date)]

    def adopt(self, *, date, adopter_name, adopter_address):
        """
        ◦ method ‹adopt› which takes keyword arguments ‹date› (a
            ‹datetime.date› instance) and ‹adopter_name› and
            ‹adopter_address› which are strings,
        """
        if not self.is_available(date=date):
            raise RuntimeError("cannot adopt an unavailable animal")

        self.adoption = Adoption(
            date=date,
            adopter_name=adopter_name,
            adopter_address=adopter_address,
        )
        return self.adoption

    def start_foster(self, *, date, parent):
        """
        ◦ method ‹start_foster› which takes a ‹date› (again a
            ‹datetime.date› instance) and ‹parent›, which accepts one of
            the objects returned by ‹available_foster_parents› listed
            below,
        """
        if not self.is_available(date=date):
            raise RuntimeError("cannot foster an unavailable animal")

        if parent.max_animals <= parent.has_animals(date=date):
            raise RuntimeError("cannot foster by a parent with full capacity")

        foster = Foster(
            parent=parent,
            start_date=date
        )

        self.foster = foster
        parent.fosters.append(foster)
        return foster

    def end_foster(self, *, date):
        """
        ◦ ‹end_foster› which takes a ‹date›,
        """
        if self.adoption != None and not self.is_available(date=date):
            raise RuntimeError("cannot end foster on an adopted animal")

        if self.is_available(date=date):
            raise RuntimeError("cannot end foster on an unfostered animal")

        self.foster.end_date = date
        self.past_fosters.append(self.foster)
        self.foster = None

    def is_available(self, *, date):
        if date < self.date_of_entry:
            return False

        if self.adoption != None and self.adoption.date <= date:
            return False

        if self.foster != None and self.foster.is_colliding(date=date):
            return False

        for f in self.past_fosters:
            if f.is_colliding(date=date):
                return False

        return True


class Shelter:
    """
    track all the resident animals and their basic stats: name, year
    of birth, gender, date of entry, species and breed,
    • store veterinary records: animals undergo exams, each of which
    has a date, the name of the attending vet and a text report,
    • record periods of foster care: animals can be moved out of the
    shelter, into the care of individuals for a period of time –
    record the start and end date of each instance, along with the
    foster parent,
    • for each foster parent, keep the name, address, phone number and
    the number of animals they can keep at once,
    • record adoptions: when was which animal adopted and by whom,
    • keep the name and address of each adopter.

    Raise a ‹RuntimeError› in (at least) these cases:

    • ‹start_foster› was called on an animal that was already in foster
    care at the given date, or ‹end_foster› on an animal that was not
    in foster care at the given date,
    • attempting to adopt an animal that was in foster care at the
    time, or attempting to put an animal that has already been adopted
    into foster care,
    • attempting to do a veterinary exam on an animal which is in
    foster care or already adopted at the time,
    • an attempt is made to exceed the capacity of a foster parent.
    """

    def __init__(self):
        self.animals = []
        self.foster_parents = []

    def add_animal(self, *, name, year_of_birth, gender, date_of_entry, species, breed):
        """
        ‹add_animal› which accepts keyword arguments for each of the
        basic stats listed above: ‹name›, ‹year_of_birth›, ‹gender›,
        ‹date_of_entry›, ‹species› and ‹breed›, where:

        ◦ the date of entry is a ‹datetime.date› instance,
        ◦ ‹year_of_birth› is an integer,
        ◦ everything else is a string,

        and returns the object representing the animal (see
        ‹list_animals› below for details about its interface),
        """
        animal = Animal(
            name=name,
            year_of_birth=year_of_birth,
            gender=gender,
            date_of_entry=date_of_entry,
            species=species,
            breed=breed,
        )

        self.animals.append(animal)
        return animal

    def list_animals(self, *, name=None, year_of_birth=None, gender=None, date_of_entry=None, species=None, breed=None, date):
        """
        ‹list_animals› which accepts:

        ◦ optional keyword arguments for each of the basic stats: only
            animals that match all the criteria (their corresponding
            attribute is equal to the value supplied to ‹list_animals›,
            «if» it was supplied) should be listed,
        ◦ a ‹date› keyword argument: only animals which were present in
            the shelter at this time (i.e. were not adopted and not in
            foster care) should be listed;

            The elements of the list returned by ‹list_animals› should have:
        """
        return [
            a for a in self.animals
            if (name == None or a.name == name)
            and (year_of_birth == None or a.year_of_birth == year_of_birth)
            and (gender == None or a.gender == gender)
            and (date_of_entry == None or a.date_of_entry == date_of_entry)
            and (species == None or a.species == species)
            and (breed == None or a.breed == breed)
            and (date == None or a.is_available(date=date))
        ]

    def add_foster_parent(self, *, name, address, phone_number, max_animals):
        """
        ‹add_foster_parent› which accepts keyword arguments ‹name›,
        ‹address› and ‹phone_number› (all strings) and ‹max_animals›
        which is an ‹int›,
        """
        parent = FosterParent(
            name=name,
            address=address,
            phone_number=phone_number,
            max_animals=max_animals,
        )

        self.foster_parents.append(parent)
        return parent

    def available_foster_parents(self, *, date):
        """
        ‹available_foster_parents› which takes a keyword argument ‹date›
        and lists foster parents with free capacity at this date (i.e.
        those who can keep more animals than they are or were keeping at
        the given date).
        """
        return [p for p in self.foster_parents if p.is_available(date=date)]
