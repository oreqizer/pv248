from datetime import datetime

from shelter import Shelter

if __name__ == "__main__":
    s = Shelter()
    s.add_animal(name="Doz1", year_of_birth=datetime.now(), gender="Male", date_of_entry=datetime.now(), species="Dog", breed="Staff")
    s.add_animal(name="Doz2", year_of_birth=datetime.now(), gender="Female", date_of_entry=datetime.now(), species="Dog", breed="Staff")
    
    print("List males :: ", s.list_animals(gender="Male"))
    print("List females :: ", s.list_animals(gender="Female"))
    print("List doges :: ", s.list_animals(species="Dog"))

    a = s.list_animals()[0]
    parent = s.add_foster_parent(name="Foster", address="Nah", phone_number="1337", max_animals=2)
    a.start_foster(parent=parent, date=datetime.now())
