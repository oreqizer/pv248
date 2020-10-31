# In the second exercise, we will take the database created in the
# previous exercise (‹books.dat›) and generate the original JSON.
# You may want to use a join or two.

# First write a function which will produce a ‹list› of ‹dict›'s
# that represent the books, starting from an open sqlite connection.

import sqlite3
import json

def read_books( conn ):
    pass

# Now write a driver that takes two filenames. It should open the
# database (do you need the foreign keys pragma this time? why yes
# or why not? what are the cons of leaving it out?), read the books,
# convert the list to JSON and store it in the output file.

def export_books( file_in, file_out ):
    pass


def test_main():
    export_books( 'books.dat', 'books_2.json' )

    with open( 'books.json', 'r' ) as f1:
        js1 = json.load( f1 )
    with open( 'books_2.json', 'r' ) as f2:
        js2 = json.load( f2 )
    assert js1 == js2

if __name__ == "__main__":
    test_main()

