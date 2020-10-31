import sqlite3

# In the final exercise of this set, you will write a few functions
# which search the book data. Like you did for export, get a cursor
# from the connection and use ‹execute› and ‹fetchone› or ‹fetchall›
# to process the results. Use SQL to limit the result set. 

# Fetching everything (‹select * from table› without a ‹where›
# clause) and processing the data using Python constructs is «bad»
# and will make your program «unusable» for realistic data sets.

# The first function will fetch all books by a given author. Use the
# ‹like› operator to allow «substring matches» on the name. E.g.
# calling ‹books_by_author( conn, "Brontë" )› should return books
# authored by any of the Brontë sisters.

def books_by_author( conn, name ):
    pass

# The second will fetch the «set» of people (i.e. each person
# appears at most once) who authored a book with a name that
# contains a given string. For instance, ‹authors_by_book( conn,
# "Bell" )› should return the 3 Brontë sisters and Ernest Hemingway.
# Try to avoid fetching the same person multiple times (i.e. use SQL
# to get a set, instead of a list).

def authors_by_book( conn, name ):
    pass

# Another function will return names of books which have at least
# ‹count› authors. For instance, there are 3 books in the data set
# with 2 or more authors.

def books_by_author_count( conn, count ):
    pass

# Finally, write a function which returns the average author count
# for a book. The function should return a single ‹float›, and
# ideally it would not fetch anything from the database other than
# the result: try to do the computation only using SQL.

def average_author_count( conn ):
    pass

from math import isclose

def test_main():

    conn = sqlite3.connect( 'books.dat' )
    res = books_by_author( conn, 'Brontë' )
    assert set( res ) == set( ['Poems by Currer, Ellis and Acton Bell',
                               'Jane Eyre', 'The Professor', 'Wuthering Heights'] )
    res = books_by_author( conn, 'son' )
    assert res == ['The Rise and Fall of D.O.D.O.']

    res = authors_by_book( conn, 'Bell' )
    assert set( res ) == set( ['Charlotte Brontë', 'Emily Brontë', 'Anne Brontë',
                               'Ernest Hemingway'] )
    res = authors_by_book( conn, 'н' )
    assert set( res ) == set( ['Аркадий Стругацкий', 'Борис Стругацкий'] )

    res = books_by_author_count( conn, 2 )
    assert set( res ) == set( ['Poems by Currer, Ellis and Acton Bell', 'Улитка на склоне', 'The Rise and Fall of D.O.D.O.'] )

    res = books_by_author_count( conn, 3 )
    assert res == ['Poems by Currer, Ellis and Acton Bell']

    res = books_by_author_count( conn, 4 )
    assert not res

    res = average_author_count( conn )
    assert isclose( res, 1.4444444444444444 )

if __name__ == "__main__":
    test_main()

