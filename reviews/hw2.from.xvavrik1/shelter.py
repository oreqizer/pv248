# Write your solution into this file.
## I appreciate that you have created multiple classes and subclasses, which helped you
## with the implementation of HW1. Also, you commented your code which is a good habbit and it helps others
## to better understand the code. Also it's good that you programmed __eq__, __repr__ functions.

## Good way of defining the Exam class. It's great that you have created id as an attribute.
class Exam:
    def __init__(self, *, id=None, vet, date, report):
        self.id = id
        self.vet = vet
        self.date = date
        self.report = report

    def __repr__(self):
        return f"Exam(id={self.id}, vet={self.vet}, report={self.report})"

    def __eq__(self, o):
        return (
            self.vet == o.vet
            and self.date == o.date
            and self.report == o.report
        )


## Same as for Exam. It's correct way.
class Adoption:
    def __init__(self, *, id=None, date, adopter_name, adopter_address):
        self.id = id
        self.date = date
        self.adopter_name = adopter_name
        self.adopter_address = adopter_address

    def __repr__(self):
        return f"Adoption(id={self.id}, adopter_name={self.adopter_name})"

    def __eq__(self, o):
        return (
            self.date == o.date
            and self.adopter_name == o.adopter_name
            and self.adopter_address == o.adopter_address
        )


## Same as for Exam and Adoption. It's correct way.
class FosterParent:
    def __init__(self, *, id=None, name, address, phone_number, max_animals):
        self.id = id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.max_animals = max_animals
        self.fosters = []

    def __repr__(self):
        return f"FosterParent(\n  id={self.id},\n  name={self.name},\n  fosters={self.fosters}\n)"

    def __eq__(self, o):
        return (
            self.name == o.name
            and self.address == o.address
            and self.phone_number == o.phone_number
            and self.max_animals == o.max_animals
        )

    def __contains__(self, cand):
        return self.is_like(cand) and self.max_animals == cand.max_animals

    def is_like(self, o):
        return self.name == o.name and self.address == o.address and self.phone_number == o.phone_number

    ## Easy and correct way.
    def has_animals(self, *, date):
        return len([f for f in self.fosters if f.is_colliding(date=date)])

    ## Easy way to get collisions for foster parent and checking if he is available.
    def is_available(self, *, date):
        collisions = 0
        for f in self.fosters:
            if f.is_colliding(date=date):
                collisions += 1
        return collisions < self.max_animals


## Same as for Exam,Adoption and FosterParent. It's correct way.
class Foster:
    def __init__(self, *, id=None, parent, animal, start_date, end_date=None):
        self.id = id
        self.parent = parent
        self.animal = animal
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"Foster(id={self.id}, start_date={self.start_date}, end_date={self.end_date})"

    def __eq__(self, o):
        return (
            self.parent == o.parent
            and self.animal == o.animal
            and self.start_date == o.start_date
            and self.end_date == o.end_date
        )

    ## Simple and correct way to get collisions.
    def is_colliding(self, *, date):
        if self.start_date <= date and (self.end_date == None or self.end_date >= date):
            return True
        return False


## Same as for Exam, Adoption, FosterParent and Foster. It's the correct way. Just one small cosmetic problem,
## I would move the is_available function bellow is_like, because in other functions - add_exam, adopt, start_foster and
## end_foster you are using is_available. It's better for reading and understanding the code because now I need to
## scroll down and find the is_available and then coming up again.
class Animal:
    def __init__(self, *, id=None, name, year_of_birth, gender, date_of_entry, species, breed):
        self.id = id
        self.name = name
        self.year_of_birth = year_of_birth
        self.gender = gender
        self.date_of_entry = date_of_entry
        self.species = species
        self.breed = breed
        self.exams = []
        self.adoption = None
        self.fosters = []

    def __repr__(self):
        return f"Animal(\n  id={self.id},\n  name={self.name},\n  year_of_birth={self.year_of_birth},\n  gender={self.gender},\n  date_of_entry={self.date_of_entry},\n  species={self.species},\n  breed={self.breed},\n)"

    def __eq__(self, o):
        return (
            self.name == o.name
            and self.year_of_birth == o.year_of_birth
            and self.gender == o.gender
            and self.date_of_entry == o.date_of_entry
            and self.species == o.species
            and self.breed == o.breed
        )

    ## Good way to distinguish between is_like and contains, which was also explained in specs.txt
    def __contains__(self, cand):
        return self.is_like(cand) and self.date_of_entry == cand.date_of_entry

    def is_like(self, o):
        return (
            self.name == o.name
            and self.year_of_birth == o.year_of_birth
            and self.gender == o.gender
            and self.species == o.species
            and self.breed == o.breed
        )

    ## Appreciate the comment and also using message in RuntimeError, which can help with the debugging process.
    ## Some other students just use empty RuntimeError, which is not great for debugging the code.
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

    ## Appreciate the comment and this is really nice and simple code for listing exams.
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

    ## Same as for add_exam.
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

    ## Same as for add_exam.
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
            animal=self,
            start_date=date
        )

        self.fosters.append(foster)
        parent.fosters.append(foster)

    ## You can only check if self.adoption is not None and self.adoption.date <= date and then check for
    ## the last foster in self.fosters( is active or not), because in specs.txt was explained that you cannot
    ## have multiple active fosters. This means that the last foster in self.fosters for the animal is always
    ## the only one which can be active. As you see you always end the last foster, not others.
    def end_foster(self, *, date):
        """
        ◦ ‹end_foster› which takes a ‹date›,
        """
        if self.adoption is not None and not self.is_available(date=date):
            raise RuntimeError("cannot end foster on an adopted animal")

        if self.is_available(date=date):
            raise RuntimeError("cannot end foster on an unfostered animal")

        foster = self.fosters[-1]
        foster.end_date = date

    ## Correct way of checking if animal is available.
    def is_available(self, *, date):
        if date < self.date_of_entry:
            return False

        if self.adoption is not None and self.adoption.date <= date:
            return False

        for f in self.fosters:
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

    def __init__(self, *, id=None):
        self.id = id
        self.animals = []
        self.foster_parents = []

    def __repr__(self):
        return f"Shelter(id={self.id}, animals={self.animals}, foster_parents={self.foster_parents})"

    def __eq__(self, other):
        for a in self.animals:
            if a not in other.animals:
                return False
        for p in self.foster_parents:
            if p not in other.foster_parents:
                return False
        return True

    ## Correct way of adding animal. Maybe use some message for RuntimeError().
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

        cand = next(iter([a for a in self.animals if a.is_like(animal)]), None)
        if cand is not None:
            if animal in self.animals:
                return cand
            raise RuntimeError

        self.animals.append(animal)
        return animal

    ## Great and correct way of getting list of animals from shelter.
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

    ## Correct way of adding foster_parrent. Maybe use some message for RuntimeError().
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

        cand = next(
            iter([p for p in self.foster_parents if p.is_like(parent)]), None)
        if cand is not None:
            if parent in self.foster_parents:
                return cand
            raise RuntimeError

        self.foster_parents.append(parent)
        return parent

    ## Correct and simple way of getting foster parents.
    def available_foster_parents(self, *, date):
        """
        ‹available_foster_parents› which takes a keyword argument ‹date›
        and lists foster parents with free capacity at this date (i.e.
        those who can keep more animals than they are or were keeping at
        the given date).
        """
        return [p for p in self.foster_parents if p.is_available(date=date)]
