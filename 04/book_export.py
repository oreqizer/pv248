# In the second exercise, we will take the database created in the
# previous exercise (‹books.dat›) and generate the original JSON.
# You may want to use a join or two.

# First write a function which will produce a ‹list› of ‹dict›'s
# that represent the books, starting from an open sqlite connection.

import sqlite3
import json

from book_import import opendb

query_books = """
--begin-sql
SELECT b.name
FROM book AS b
--end-sql
"""

query_authors = """
--begin-sql
SELECT a.name
FROM book AS b
    INNER JOIN book_author_list AS l ON l.book_id = b.id
    INNER JOIN author AS a ON l.author_id = a.id
WHERE b.name = ?
--end-sql
"""

def read_books(conn):
    cur = conn.cursor()
    res = []

    cur.execute(query_books)
    books = cur.fetchall()
    for b in books:
        cur.execute(query_authors, b)
        authors = cur.fetchall()
        res.append({
            "name": b[0],
            "authors": [name for (name,) in authors],
        })

    conn.commit()
    return res

# Now write a driver that takes two filenames. It should open the
# database (do you need the foreign keys pragma this time? why yes
# or why not? what are the cons of leaving it out?), read the books,
# convert the list to JSON and store it in the output file.


def export_books(file_in, file_out):
    conn = opendb(file_in)
    res = json.dumps(read_books(conn), indent="  ")
    open(file_out, "w").write(res)


def test_main():
    export_books('books.dat', 'books_2.json')

    with open('books.json', 'r') as f1:
        js1 = json.load(f1)
    with open('books_2.json', 'r') as f2:
        js2 = json.load(f2)
    assert js1 == js2


if __name__ == "__main__":
    test_main()
