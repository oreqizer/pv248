# The file ‹lists.sql› contains a database schema for keeping
# shopping lists. Besides shopping lists themselves, we will keep a
# table of item descriptions, a table of shops (vendors) and a table
# of supplies currently in your pantry. This last table also keeps
# track of a ‘minimal’ and ‘preferred’ amount for each item. Those
# will come in handy when we will want to create shopping lists
# automatically.

# Each item may be available from multiple vendors, and of course
# each vendor stocks multiple items. Therefore, items and shops are
# in an M:N relationship, and we will keep this relationship in an
# auxiliary table. Finally, each vendor has, for each item, an
# individual unit price that is valid starting on a given date. A
# null price indicates that the item is not available in the given
# timespan. New start date overrides the price.

# A shopping list, then, is a list of items to obtain. Each item on
# the list comes with:
#
#  • the quantity to obtain,
#  • the shop where to buy it and
#  • the quantity actually obtained.
#
# Besides the list of items, the shopping list has a date attached
# to it. In this exercise, we will start by providing an interface
# for creating new lists.

from os import unlink
from datetime import datetime
import errno
import sqlite3
from datetime import date
from sqlite3 import Connection
from typing import Optional

# The classes in this exercise (and its follow-ups) will be
# associated with records in the database. Each class will hold onto
# an optional ‹id›: if the ‹id› is ‹None›, the record is «not»
# stored in the database (yet). So far, we will only set the ‹id› in
# the ‹create› method.

# The only method which is allowed to change the database is
# ‹create› (in a later exercise, we will add ‹update›). All ‹set_*›
# and ‹add_*› methods (and later ‹remove_*›) methods should simply
# remember the changes and additions, until the user calls ‹create›,
# which then stores everything at once. Other methods may, however,
# query the database for data, if it is convenient to do so.

# Finally, feel free to add a suitable base class, from which the
# other classes can be derived.

class Base:
    # Creates an empty item, not yet associated with anything in the
    # database. Set the internal ‹id› to ‹None›.

    def __init__(self, db: Connection):
        sql = open("lists.sql").read()
        db.executescript(sql)

        self.db = db
        self.id = None

class Shop(Base):

    def __init__(self, db: Connection):
        super(Shop, self).__init__(db)
        self.name = None

    def set_name(self, name: str):
        self.name = name

    # Create a record in the database. If the instance is already
    # associated with a record, raise a ‹RuntimeError›. If the
    # shop does not have a name, raise a ‹RuntimeError›.

    def create(self):
        if self.name is None or self.id is not None:
            raise RuntimeError

        cur = self.db.cursor()
        cur.execute("""
            --begin-sql
            INSERT INTO vendor (name) VALUES (?)
            --end-sql
        """, (self.name,))

        (id,) = cur.execute("SELECT last_insert_rowid()").fetchone()
        self.id = id

        self.db.commit()
        cur.close()

# All the remaining classes are analogous to ‹Shop›.


class Item(Base):

    def __init__(self, db: Connection):
        super(Item, self).__init__(db)
        self.name = None
        self.prices = []

    def set_name(self, name: str):
        self.name = name

    # Prices are associated not with just an item, but also a time
    # period and a specific shop.

    def set_price(self, vendor: Shop, price: Optional[int],
                  start: date):
        self.prices.append({ "vendor": vendor, "price": price, "start": start })

    # If the item does not have a name, raise a ‹RuntimeError›.

    def create(self):
        if self.name is None or self.id is not None:
            raise RuntimeError

        cur = self.db.cursor()
        try:
            id, = cur.execute("""
                --begin-sql
                SELECT id FROM item WHERE name = ?
                --end-sql
            """, (self.name,)).fetchone()
            self.id = id
        except:
            cur.execute("""
                --begin-sql
                INSERT INTO item (name) VALUES (?)
                --end-sql
            """, (self.name,))

            id, = cur.execute("SELECT last_insert_rowid()").fetchone()
            self.id = id

        for p in self.prices:
            cur.execute("""
                --begin-sql
                INSERT INTO pricing (vendor_id, item_id, price, start_date)
                VALUES (?, ?, ?, ?)
                --end-sql
            """, (p["vendor"].id, self.id, p["price"], p["start"]))
    
        self.db.commit()
        cur.close()


class ShoppingList(Base):

    def __init__(self, db: Connection):
        super(ShoppingList, self).__init__(db)
        self.date = None
        self.items = []

    def set_date(self, when: date):
        self.date = when

    def add_item(self, item: Item, qty: int):
        self.items.append({ "item": item, "qty": qty })

    # A shopping list might be empty, but it must have a date set.
    # If it does not, refuse to create it (raise a ‹RuntimeError›).

    def create(self):
        if self.date is None or self.id is not None:
            raise RuntimeError

        cur = self.db.cursor()
        cur.execute("""
            --begin-sql
            INSERT INTO shopping_list ("date") VALUES (?)
            --end-sql
        """, (self.date,))

        (id,) = cur.execute("SELECT last_insert_rowid()").fetchone()
        self.id = id
        for i in self.items:
            cur.execute("""
                --begin-sql
                INSERT INTO shop_list_item (list_id, item_id, quantity)
                VALUES (?, ?, ?)
                --end-sql
            """, (self.id, i["item"].id, i["qty"]))
    
        self.db.commit()
        cur.close()


def assert_throws(ex, f, *args):

    try:
        f(*args)
        raise AssertionError("expected " + str(ex) + " to be thrown")
    except ex:
        return


def test_main():

    try:
        unlink('lists.db')
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

    conn = sqlite3.connect('lists.db')
    s1 = Shop(conn)
    assert_throws(RuntimeError, s1.create)
    s1.set_name('Lidl')
    s1.create()
    assert_throws(RuntimeError, s1.create)

    s2 = Shop(conn)
    s2.set_name('Albert')
    s2.create()

    c = conn.cursor()
    c.execute('select name from vendor order by name')
    res = [item[0] for item in c.fetchall()]
    assert res[0] == 'Albert'
    assert res[1] == 'Lidl'

    i1 = Item(conn)
    assert_throws(RuntimeError, i1.create)
    i1.set_name('men socks')
    i1.set_price(s1, 20, date(2020, 10, 22))
    i1.set_price(s2, 22, date(2020, 10, 23))
    i1.create()

    i2 = Item(conn)
    i2.set_name('white tofu')
    i2.set_price(s1, 30, date(2020, 11, 27))
    i2.set_price(s1, None, date(2020, 11, 29))  # out of tofu
    i2.set_price(s1, 34, date(2020, 12, 8))
    i2.create()

    c.execute('select * from pricing where item_id = ?', (i1.id, ))
    res = c.fetchall()

    assert len(res) == 2
    assert s1.id in [item[0] for item in res]
    assert s2.id in [item[0] for item in res]

    def get_date(d):
        return datetime.strptime(d, '%Y-%m-%d').date()

    def check_pricing(i_id, p, d):
        assert item_id == i_id
        assert price == p
        assert get_date(dat) == d

    for shop_id, item_id, price, dat in res:
        if shop_id == s1.id:
            check_pricing(i1.id, 20, date(2020, 10, 22))
        elif shop_id == s2.id:
            check_pricing(i1.id, 22, date(2020, 10, 23))

    c.execute(
        'select * from pricing where item_id = ? order by start_date', (i2.id, ))
    res = c.fetchall()

    assert len(res) == 3
    assert s1.id in [item[0] for item in res]
    assert not s2.id in [item[0] for item in res]

    expected = [(2, 30, date(2020, 11, 27)),
                (2, None, date(2020, 11, 29)),
                (2, 34, date(2020, 12, 8))]

    for idx in range(len(res)):
        shop_id, item_id, price, dat = res[idx]
        i_exp, p_exp, d_exp = expected[idx]
        check_pricing(i_exp, p_exp, d_exp)

    sl1 = ShoppingList(conn)
    assert_throws(RuntimeError, sl1.create)

    sl1.set_date(date(2020, 10, 28))
    sl1.add_item(i1, 3)
    sl1.add_item(i2, 1)
    sl1.create()

    c.execute('select * from shopping_list')
    res = c.fetchall()
    assert len(res) == 1
    assert get_date(res[0][1]) == date(2020, 10, 28)

    c.execute('select item_id, quantity from shop_list_item order by item_id')
    res = c.fetchall()
    assert len(res) == 2
    item_ids = [item[0] for item in res]
    assert i1.id in item_ids
    assert i2.id in item_ids
    assert [item[1] for item in res] == [3, 1]


if __name__ == "__main__":
    test_main()
