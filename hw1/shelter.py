# Write your solution into this file.
from datetime import date

class Exam:
    def __init__(self, *, vet, date, report):
        self.vet = vet
        self.date = date
        self.report = report

class Animal:
    def __init__(self, *, id, name, year_of_birth, gender, date_of_entry, species, breed):
        """
        each of the basic stats as an attribute of the corresponding
        type (see ‹add_animal›),
        """
        self.id = id
        self.name = name
        self.year_of_birth = year_of_birth
        self.gender = gender
        self.date_of_entry = date_of_entry
        self.species = species
        self.breed = breed
        self.exams = []

    def add_exam(self, *, vet, date, report):
        """
        ◦ method ‹add_exam› which accepts keyword arguments ‹vet› and
            ‹date› and ‹report›, where ‹vet› and ‹report› are strings and
            ‹date› is a ‹datetime.date› instance,
        """
        exam = Exam(
            vet=vet,
            date=date,
            report=report,
        )
        self.exams.append(exam)

    def list_exams(self):
        """
        ◦ method ‹list_exams› which takes keyword arguments ‹start› and
            ‹end›, both ‹datetime.date› instances, or ‹None› (the range is
            inclusive; in the latter case, the range is not limited in
            that direction),
        """
        pass

    def adopt(self):
        """
        ◦ method ‹adopt› which takes keyword arguments ‹date› (a
            ‹datetime.date› instance) and ‹adopter_name› and
            ‹adopter_address› which are strings,
        """
        pass

    def start_foster(self):
        """
        ◦ method ‹start_foster› which takes a ‹date› (again a
            ‹datetime.date› instance) and ‹parent›, which accepts one of
            the objects returned by ‹available_foster_parents› listed
            below,
        """
        pass

    def end_foster(self):
        """
        ◦ ‹end_foster› which takes a ‹date›,
        """
        pass

class FosterParent:
    def __init__(self):
        pass


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
        self.animals = {}
        self.animals_id = 0 # autoincrement
        self.foster_parents = {}
        self.foster_parents_id = 0 # autoincrement

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
        id = self.animals_id
        animal = Animal(
            id=id,
            name=name,
            year_of_birth=year_of_birth,
            gender=gender,
            date_of_entry=date_of_entry,
            species=species,
            breed=breed,
        )

        self.animals[id] = animal
        self.animals_id += 1

        return animal

    def list_animals(self):
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
        pass

    def add_foster_parent(self):
        """
        ‹add_foster_parent› which accepts keyword arguments ‹name›,
        ‹address› and ‹phone_number› (all strings) and ‹max_animals›
        which is an ‹int›,
        """
        pass

    def available_foster_parents(self):
        """
        ‹available_foster_parents› which takes a keyword argument ‹date›
        and lists foster parents with free capacity at this date (i.e.
        those who can keep more animals than they are or were keeping at
        the given date).
        """
        pass
