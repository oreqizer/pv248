import list_create
import sqlite3
from sqlite3 import Connection
from datetime import date

# In this exercise, we will extend the classes from ‹list_create› by
# adding various ways to fetch them from the database.


class Shop(list_create.Shop):

    def __repr__(self):
        return "Shop(id={id}, name={name}".format(id=self.id, name=self.name)

    # Find the shop in the database by its name. If no such shop is
    # in the database, raise a ‹RuntimeError›. If found, set the
    # internal ‹id› of the instance. Only allow fetching if the
    # calling Shop instance's ‹id› is not set yet. If there are
    # several shops with the same name, raise a ‹RuntimeError›.

    def fetch_by_name(self, name: str):
        if self.id is not None:
            raise RuntimeError

        id, = self.db.execute("""
            --begin-sql
            SELECT id FROM vendor WHERE name = ?
            --end-sql
        """, (name,)).fetchone()

        self.name = name
        self.id = id

    def fetch_by_id(self, ID: int):
        if self.id is not None:
            raise RuntimeError

        name, = self.db.execute("""
            --begin-sql
            SELECT name FROM vendor WHERE id = ?
            --end-sql
        """, (ID,)).fetchone()

        self.name = name
        self.id = ID

# The top-level function ‹find_shops› will do a substring search on
# all the shops in the database, and return a ‹Shop› instance for
# each match.


def find_shops(db: Connection, pattern: str):
    rows = db.execute("""
        --begin-sql
        SELECT id, name FROM vendor
        WHERE name LIKE ?
        --end-sql
    """, ("%{pattern}%".format(pattern=pattern),))
    res = []
    for id, name in rows:
        shop = Shop(db)
        shop.id = id
        shop.name = name
        res.append(shop)
    return res

class Item(list_create.Item):

    def fetch_by_name(self, name: str):
        if self.id is not None:
            raise RuntimeError

        id, = self.db.execute("""
            --begin-sql
            SELECT id FROM item WHERE name = ?
            --end-sql
        """, (name,)).fetchone()

        self.name = name
        self.id = id

    def fetch_by_id(self, ID: int):
        if self.id is not None:
            raise RuntimeError

        name, = self.db.execute("""
            --begin-sql
            SELECT name FROM item WHERE id = ?
            --end-sql
        """, (ID,)).fetchone()

        self.name = name
        self.id = ID

    # Find a price at the given time in the given shop. Return
    # ‹None› if the item is not available from the vendor at the
    # time.

    def get_price(self, vendor: Shop, when: date):
        res = self.db.execute("""
            --begin-sql
            SELECT price FROM pricing
            WHERE item_id = ?
                AND vendor_id = ?
                AND start_date <= ?
            ORDER BY start_date DESC
            --end-sql
        """, (self.id, vendor.id, when)).fetchone()
        if res is None:
            return None
        price, = res
        return price

    # Find the best price available on a given date. Return a tuple
    # of ‹int› (the price) and a ‹Shop› (the vendor which has this
    # price), or ‹None› if the item is not available at all. Tie
    # breaks alphabetically (prefer vendors with names that come
    # first in a dictionary).

    def get_best_price(self, when: date):
        res = self.db.execute("""
            --begin-sql
            SELECT r.price, r.id
            FROM (
                SELECT p.price, v.id, v.name, MAX(p.start_date)
                FROM pricing AS p
                    INNER JOIN vendor AS v ON v.id = p.vendor_id
                WHERE p.item_id = ?
                  AND p.start_date <= ?
                GROUP BY v.id
                ORDER BY p.start_date DESC
            ) AS r
            WHERE r.price IS NOT NULL
            ORDER BY r.price ASC, r.name ASC
            --end-sql
        """, (self.id, when)).fetchone()
        if res is None:
            return None
        price, vendor_id = res
        shop = Shop(self.db)
        shop.fetch_by_id(vendor_id)
        return price, shop


class ShoppingList(list_create.ShoppingList):

    def fetch_by_id(self, ID: int):
        if self.id is not None:
            raise RuntimeError

        date, = self.db.execute("""
            --begin-sql
            SELECT date FROM shopping_list WHERE id = ?
            --end-sql
        """, (ID,)).fetchone()

        rows = self.db.execute("""
            --begin-sql
            SELECT item_id, quantity
            FROM shop_list_item
            WHERE list_id = ?
            --end-sql
        """, (ID,))
        for item_id, qty in rows:
            item = Item(self.db)
            item.fetch_by_id(item_id)
            self.items.append({ "item": item, "qty": qty })

        self.date = date
        self.id = ID

# Find all shopping lists that have a given item on it, in quantity
# at least ‹qty›. Returns a list of ShoppingList instances.


def find_lists_by_item(db: Connection, item: Item, qty: int):
    rows = db.execute("""
        --begin-sql
        SELECT l.id
        FROM shopping_list AS l
            INNER JOIN shop_list_item AS li ON li.list_id = l.id
        WHERE li.item_id = ?
          AND li.quantity >= ?
        --end-sql
    """, (item.id, qty))
    res = []
    for id, in rows:
        l = ShoppingList(db)
        l.fetch_by_id(id)
        res.append(l)
    return res


def assert_throws(ex, f, *args):

    try:
        f(*args)
        raise AssertionError("expected " + str(ex) + " to be thrown")
    except ex:
        return


def test_shops():
    conn = sqlite3.connect(":memory:")

    s1 = Shop(conn)
    s1.set_name('Lidl')
    s1.create()

    s2 = Shop(conn)
    s2.set_name('Albert')
    s2.create()

    s3 = Shop(conn)
    s3.fetch_by_name('Lidl')
    assert(s3.__dict__ == s1.__dict__)

    assert_throws(RuntimeError, s3.create)
    assert_throws(RuntimeError, s3.fetch_by_name, 'Albert')

    s4 = Shop(conn)
    assert_throws(RuntimeError, s3.fetch_by_name, 'Penny')
    s4.set_name('Lidl')
    s4.create()

    s5 = Shop(conn)
    assert_throws(RuntimeError, s3.fetch_by_name, 'Lidl')
    assert_throws(RuntimeError, s1.fetch_by_id, s2.id)
    assert_throws(RuntimeError, s1.fetch_by_id, s1.id)

    s5.fetch_by_id(s2.id)
    assert(s5.__dict__ == s2.__dict__)

    shops = find_shops(conn, 'Lidl')
    assert len(shops) == 2

    def check_shop(s, d):
        return s.__dict__ in [shop.__dict__ for shop in d]

    assert check_shop(s1, shops)
    assert check_shop(s4, shops)

    s6 = Shop(conn)
    s6.set_name('ALidlt7')
    shops = find_shops(conn, 'Lidl')
    assert len(shops) == 2
    assert not check_shop(s6, shops)

    s6.create()
    shops = find_shops(conn, 'Lidl')
    assert len(shops) == 3
    assert check_shop(s6, shops)


def test_items():

    conn = sqlite3.connect(":memory:")

    s1 = Shop(conn)
    s1.set_name('Lidl')
    s1.create()

    s2 = Shop(conn)
    s2.set_name('Albert')
    s2.create()

    i1 = Item(conn)
    i1.set_name('men socks')
    i1.set_price(s1, 20, date(2020, 10, 22))
    i1.set_price(s1, 27, date(2020, 10, 30))
    i1.set_price(s2, 22, date(2020, 10, 23))
    i1.create()

    i2 = Item(conn)
    i2.set_name('white tofu')
    i2.set_price(s1, 30, date(2020, 11, 27))
    i2.set_price(s1, None, date(2020, 11, 29))  # out of tofu
    i2.set_price(s1, 34, date(2020, 12, 8))
    i2.set_price(s2, 32, date(2020, 11, 20))
    i2.create()

    assert_throws(RuntimeError, i1.fetch_by_name, 'white tofu')
    assert_throws(RuntimeError, i2.fetch_by_id, i1.id)
    i3 = Item(conn)
    i3.fetch_by_name('men socks')
    assert i1.id == i3.id
    i3.id = None
    i3.create()

    c = conn.cursor()
    c.execute(
        'select vendor_id, price, start_date from pricing where item_id = ? order by price', (i3.id, ))
    rows_i3 = c.fetchall()
    c.execute(
        'select vendor_id, price, start_date from pricing where item_id = ? order by price', (i1.id, ))
    rows_i1 = c.fetchall()
    assert rows_i3 == rows_i1

    assert i1.get_price(s1, date(2020, 10, 10)) is None
    assert i1.get_price(s1, date(2020, 10, 22)) == 20
    assert i1.get_price(s1, date(2020, 10, 29)) == 20
    assert i1.get_price(s1, date(2020, 11, 4)) == 27

    price, s = i2.get_best_price(date(2020, 11, 28))
    assert price == 30
    assert s.id == s1.id
    price, s = i2.get_best_price(date(2020, 11, 30))
    assert price == 32
    assert s.id == s2.id

    assert i2.get_best_price(date(2011, 1, 1)) is None


def test_shopping_lists():

    conn = sqlite3.connect(":memory:")

    s1 = Shop(conn)
    s1.set_name('Lidl')
    s1.create()

    s2 = Shop(conn)
    s2.set_name('Albert')
    s2.create()

    i1 = Item(conn)
    i1.set_name('men socks')
    i1.set_price(s1, 20, date(2020, 10, 22))
    i1.set_price(s1, 27, date(2020, 10, 30))
    i1.set_price(s2, 22, date(2020, 10, 23))
    i1.create()

    i2 = Item(conn)
    i2.set_name('white tofu')
    i2.set_price(s1, 30, date(2020, 11, 27))
    i2.set_price(s1, None, date(2020, 11, 29))  # out of tofu
    i2.set_price(s1, 34, date(2020, 12, 8))
    i2.set_price(s2, 32, date(2020, 11, 20))
    i2.create()

    sl1 = ShoppingList(conn)
    sl1.set_date(date(2020, 10, 28))
    sl1.add_item(i1, 3)
    sl1.add_item(i2, 1)
    sl1.create()

    assert_throws(RuntimeError, sl1.fetch_by_id, sl1.id)
    sl2 = ShoppingList(conn)
    sl2.fetch_by_id(sl1.id)
    assert sl2.id == sl1.id

    c = conn.cursor()
    c.execute('select * from shop_list_item')
    assert len(c.fetchall()) == 2

    sl2.id = None
    sl2.create()
    c.execute('select * from shop_list_item')
    assert len(c.fetchall()) == 4

    c.execute(
        'select item_id, quantity from shop_list_item where list_id = ?', (sl1.id, ))
    sl1_items = c.fetchall()

    c.execute(
        'select item_id, quantity from shop_list_item where list_id = ?', (sl2.id, ))
    sl2_items = c.fetchall()

    assert sl1_items == sl2_items

    lists = find_lists_by_item(conn, i1, 1)
    ids = [li.id for li in lists]
    assert sl1.id in ids
    assert sl2.id in ids


def test_main():
    test_shops()
    test_items()
    test_shopping_lists()


if __name__ == '__main__':
    test_main()
