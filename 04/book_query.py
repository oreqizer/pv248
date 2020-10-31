from math import isclose
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

query_books_by_author = """
--begin-sql
SELECT b.name
FROM book AS b
    INNER JOIN book_author_list AS l ON l.book_id = b.id
    INNER JOIN author AS a ON a.id = l.author_id
WHERE a.name LIKE ?
--end-sql
"""

def books_by_author(conn, name):
    c = conn.cursor()
    c.execute(query_books_by_author, ("%{name}%".format(name=name),))
    res = c.fetchall()
    return [e for (e,) in res]

# The second will fetch the «set» of people (i.e. each person
# appears at most once) who authored a book with a name that
# contains a given string. For instance, ‹authors_by_book( conn,
# "Bell" )› should return the 3 Brontë sisters and Ernest Hemingway.
# Try to avoid fetching the same person multiple times (i.e. use SQL
# to get a set, instead of a list).

query_authors_by_book = """
--begin-sql
SELECT a.name
FROM book AS b
    INNER JOIN book_author_list AS l ON l.book_id = b.id
    INNER JOIN author AS a ON a.id = l.author_id
WHERE b.name LIKE ?
GROUP BY a.name
--end-sql
"""

def authors_by_book(conn, name):
    c = conn.cursor()
    c.execute(query_authors_by_book, ("%{name}%".format(name=name),))
    res = c.fetchall()
    return [e for (e,) in res]

# Another function will return names of books which have at least
# ‹count› authors. For instance, there are 3 books in the data set
# with 2 or more authors.

query_books_by_author_count = """
--begin-sql
SELECT b.name, COUNT(l.author_id) AS c
FROM book AS b
    INNER JOIN book_author_list AS l ON l.book_id = b.id
GROUP BY b.name
HAVING c >= ?
--end-sql
"""

def books_by_author_count(conn, count):
    c = conn.cursor()
    c.execute(query_books_by_author_count, (count,))
    res = c.fetchall()
    return [e for e, c in res]

# Finally, write a function which returns the average author count
# for a book. The function should return a single ‹float›, and
# ideally it would not fetch anything from the database other than
# the result: try to do the computation only using SQL.

query_average_author_count = """
--begin-sql
SELECT AVG(c.count)
FROM (
    SELECT COUNT(l.author_id) AS count
    FROM book AS b
        INNER JOIN book_author_list AS l ON l.book_id = b.id
    GROUP BY b.name
) AS c
--end-sql
"""

def average_author_count(conn):
    c = conn.cursor()
    c.execute(query_average_author_count, ())
    (res, ) = c.fetchone()
    return res


def test_main():

    conn = sqlite3.connect('books.dat')
    res = books_by_author(conn, 'Brontë')
    assert set(res) == set(['Poems by Currer, Ellis and Acton Bell',
                            'Jane Eyre', 'The Professor', 'Wuthering Heights'])
    res = books_by_author(conn, 'son')
    assert res == ['The Rise and Fall of D.O.D.O.']

    res = authors_by_book(conn, 'Bell')
    assert set(res) == set(['Charlotte Brontë', 'Emily Brontë', 'Anne Brontë',
                            'Ernest Hemingway'])
    res = authors_by_book(conn, 'н')
    assert set(res) == set(['Аркадий Стругацкий', 'Борис Стругацкий'])

    res = books_by_author_count(conn, 2)
    assert set(res) == set(['Poems by Currer, Ellis and Acton Bell',
                            'Улитка на склоне', 'The Rise and Fall of D.O.D.O.'])

    res = books_by_author_count(conn, 3)
    assert res == ['Poems by Currer, Ellis and Acton Bell']

    res = books_by_author_count(conn, 4)
    assert not res

    res = average_author_count(conn)
    assert isclose(res, 1.4444444444444444)


if __name__ == "__main__":
    test_main()
