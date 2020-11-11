import list_search
import sqlite3
from sqlite3 import Connection
from datetime import date

# In this exercise, we will extend the classes from ‹list_search› by
# adding an ‹update› method to each. If the entity does not exist in
# the database, ‹update› should raise a ‹RuntimeError›. After
# ‹update›, the database should reflect any changes and additions
# that have been done on the instance since it was either created,
# fetched or last updated.

# Also add a ‹delete› method, which removes the entry and all the
# records it owns, from all relevant tables in the database. If
# you are deleting an entry that has associated records in other
# tables but does not own these records, raise a ‹RuntimeError›
# instead (an example would be removing a shop, while a pricing
# entry for that shop exists).
# After ‹delete›, the instance can no longer be used for anything
# (but you do not need to enforce this).


class Shop(list_search.Shop):

    def update(self):
        if self.id is None:
            raise RuntimeError

        self.db.execute("""
            --begin-sql
            UPDATE vendor
            SET name = ?
            WHERE id = ?
            --end-sql
        """, (self.name, self.id))
        self.db.commit()

    def delete(self):
        if self.id is None:
            raise RuntimeError

        count, = self.db.execute("""
            --begin-sql
            SELECT COUNT(vendor_id)
            FROM pricing
            WHERE vendor_id = ?
            --end-sql
        """, (self.id,)).fetchone()
        if count > 0:
            raise RuntimeError

        self.db.execute("""
            --begin-sql
            DELETE FROM vendor
            WHERE id = ?
            --end-sql
        """, (self.id,))
        self.db.commit()

class Item(list_search.Item):
    def __repr__(self):
        return "Item(id={id}, name={name})".format(id=self.id, name=self.name)

    def update(self):
        if self.id is None:
            raise RuntimeError

        self.db.execute("""
            --begin-sql
            UPDATE item
            SET name = ?
            WHERE id = ?
            --end-sql
        """, (self.name, self.id))

        self.db.execute("""
            --begin-sql
            DELETE FROM pricing
            WHERE item_id = ?
            --end-sql
        """, (self.id,))

        for p in self.prices:
            self.db.execute("""
                --begin-sql
                INSERT INTO pricing (vendor_id, item_id, price, start_date)
                VALUES (?, ?, ?, ?)
                --end-sql
            """, (p["vendor"].id, self.id, p["price"], p["start"]))
            # self.db.execute("""
            #     --begin-sql
            #     UPDATE pricing
            #     SET vendor_id = ?, price = ?, start_date = ?
            #     WHERE item_id = ?
            #     --end-sql
            # """, (p["vendor"].id, p["price"], p["start"], self.id))

        self.db.commit()

    def delete(self):
        if self.id is None:
            raise RuntimeError

        self.db.execute("""
            --begin-sql
            DELETE FROM pricing
            WHERE item_id = ?
            --end-sql
        """, (self.id,))

        self.db.execute("""
            --begin-sql
            DELETE FROM item
            WHERE id = ?
            --end-sql
        """, (self.id,))
        self.db.commit()


class ShoppingList(list_search.ShoppingList):

    def remove_item(self, item: Item):
        if self.id is None:
            raise RuntimeError

        self.db.execute("""
            --begin-sql
            DELETE FROM shop_list_item
            WHERE item_id = ?
            --end-sql
        """, (item.id,))
        self.db.commit()

    def update(self):
        if self.id is None:
            raise RuntimeError

        self.db.execute("""
            --begin-sql
            UPDATE shopping_list
            SET date = ?
            WHERE id = ?
            --end-sql
        """, (self.date, self.id))

        self.db.execute("""
            --begin-sql
            DELETE FROM shop_list_item
            WHERE list_id = ?
            --end-sql
        """, (self.id,))

        for i in self.items:
            self.db.execute("""
                --begin-sql
                INSERT INTO shop_list_item (list_id, item_id, quantity)
                VALUES (?, ?, ?)
                --end-sql
            """, (self.id, i["item"].id, i["qty"]))

        self.db.commit()

    def delete(self):
        if self.id is None:
            raise RuntimeError

        self.db.execute("""
            --begin-sql
            DELETE FROM shop_list_item
            WHERE list_id = ?
            --end-sql
        """, (self.id,))

        self.db.execute("""
            --begin-sql
            DELETE FROM shopping_list
            WHERE id = ?
            --end-sql
        """, (self.id,))
        self.db.commit()

# The following function will check the current supplies and update
# the given shopping list so that afterwards, fetching everything on
# the list results in all supplies being at least at their ‘minimum’
# level (if ‹preferred› is ‹False›) or at their ‘preferred’ level
# (if ‹preferred› is ‹True›). Do not remove anything from the list.
#
# Note that some of the required items might be already on the list
# (but possibly in an insufficient quantity). Do not add more of an
# item than required for the restock, unless it already was on the
# list (specifically, calling ‹add_missing› a second time should
# have no effect, unless the current supply levels changed in the
# meantime).


def add_missing(shop_list: ShoppingList, preferred: bool):
    if preferred:
        shop_list.db.execute("""
        --begin-sql
        INSERT INTO shop_list_item (list_id, item_id, quantity)
        SELECT li.list_id, supplies.item_id, (preferred - supplies.quantity - li.quantity)
        FROM supplies
            OUTER JOIN shop_list_item AS li ON supplies.item_id = li.item_id
        WHERE (supplies.quantity + li.quantity) < preferred
          AND li.list_id = ?
        --end-sql
    """, (shop_list.id,))
    else:
        shop_list.db.execute("""
            --begin-sql
            INSERT INTO shop_list_item (list_id, item_id, quantity)
            SELECT li.list_id, supplies.item_id, (minimal - supplies.quantity - li.quantity)
            FROM supplies
                INNER JOIN shop_list_item AS li ON supplies.item_id = li.item_id
            WHERE (supplies.quantity + li.quantity) < minimal
            AND li.list_id = ?
            --end-sql
        """, (shop_list.id,))
    shop_list.db.commit()


def assert_throws(ex, f, *args):

    try:
        f(*args)
        raise AssertionError("expected " + str(ex) + " to be thrown")
    except ex:
        return


def test_main():
    conn = sqlite3.connect(":memory:")

    s1 = Shop(conn)
    assert_throws(RuntimeError, s1.update)
    assert_throws(RuntimeError, s1.delete)

    s1.set_name('Lidl')
    s1.create()
    s1.set_name('notLidl')

    c = conn.cursor()
    c.execute('select name from vendor where id = ?', (s1.id, ))
    assert c.fetchone()[0] == 'Lidl'
    s1.update()

    c.execute('select name from vendor where id = ?', (s1.id, ))
    assert c.fetchone()[0] == 'notLidl'

    s1.delete()
    c.execute('select * from vendor where id = ?', (s1.id, ))
    assert len(c.fetchall()) == 0

    i1 = Item(conn)
    i1.set_name('women socks')
    i1.create()
    i1.set_name('not socks')
    c.execute('select name from item where id = ?', (i1.id, ))
    assert c.fetchone()[0] == 'women socks'

    i1.update()
    c.execute('select name from item where id = ?', (i1.id, ))
    assert c.fetchone()[0] == 'not socks'

    s1 = Shop(conn)
    s1.set_name('Lidl')
    s1.create()

    i1.set_price(s1, 20, date(2020, 3, 7))
    i1.update()
    assert_throws(RuntimeError, s1.delete)

    i1.delete()
    c.execute('select * from item where id = ?', (i1.id, ))
    assert not c.fetchall()
    c.execute('select * from pricing where item_id = ?', (i1.id, ))
    assert not c.fetchall()

    i3 = Item(conn)
    i3.set_name('marinara sauce')
    i3.create()

    sl1 = ShoppingList(conn)
    sl1.set_date(date(2020, 10, 28))
    sl1.add_item(i3, 2)

    assert_throws(RuntimeError, sl1.update)
    sl1.create()

    c.execute('select * from shop_list_item where list_id = ?', (sl1.id, ))
    assert len(c.fetchall()) == 1

    i2 = Item(conn)
    i2.set_name('chocolate')
    i2.create()

    sl1.add_item(i2, 7)
    c.execute('select * from shop_list_item where list_id = ?', (sl1.id, ))
    assert len(c.fetchall()) == 1

    sl1.update()
    c.execute('select * from shop_list_item where list_id = ?', (sl1.id, ))
    assert len(c.fetchall()) == 2

    sl1.delete()
    c.execute('select * from shop_list_item where list_id = ?', (sl1.id, ))
    assert not c.fetchall()

    c.execute('select * from shopping_list where id = ?', (sl1.id, ))
    assert not c.fetchall()


def test_missing():

    conn = sqlite3.connect(":memory:")

    i1 = Item(conn)
    i1.set_name('women socks')
    i1.create()

    i2 = Item(conn)
    i2.set_name('pudding')
    i2.create()

    i3 = Item(conn)
    i3.set_name('marinara sauce')
    i3.create()

    i4 = Item(conn)
    i4.set_name('chocolate')
    i4.create()

    c = conn.cursor()
    c.execute('insert into supplies( item_id, quantity, minimal, preferred ) values ( ?, ?, ?, ? )',
              (i1.id, 2, 4, 5))
    c.execute('insert into supplies( item_id, quantity, minimal, preferred ) values ( ?, ?, ?, ? )',
              (i2.id, 1, 1, 2))
    c.execute('insert into supplies( item_id, quantity, minimal, preferred ) values ( ?, ?, ?, ? )',
              (i3.id, 0, 3, 3))
    c.execute('insert into supplies( item_id, quantity, minimal, preferred ) values ( ?, ?, ?, ? )',
              (i4.id, 2, 5, 7))

    sl = ShoppingList(conn)
    sl.set_date(date(2020, 9, 3))
    sl.add_item(i1, 1)
    sl.add_item(i4, 1)
    sl.add_item(i4, 1)
    sl.add_item(i2, 1)
    sl.create()

    c.execute('select * from shop_list_item where list_id = ?', (sl.id, ))
    assert len(c.fetchall()) == 4

    add_missing(sl, False)
    # item 1, need 4, have 2, on list 1 ( need to add 1 )
    # item 2, need 1, have 1, on list 1
    # item 3, need 3, have 0, not on list ( need to add 3 )
    # item 4, need 5, have 2, on list 2 ( need to add 1 )

    c.execute(
        'select item_id, quantity from shop_list_item where list_id = ?', (sl.id, ))
    res = c.fetchall()
    assert len(res) == 7

    def check_item(i_id, l, q):
        print(i_id, l, q)
        print(sum([i[1] for i in l if i[0] == i_id]))
        assert sum([i[1] for i in l if i[0] == i_id]) == q

    check_item(i1.id, res, 2)
    check_item(i2.id, res, 1)
    check_item(i3.id, res, 3)
    check_item(i4.id, res, 3)

    sl1 = ShoppingList(conn)
    sl1.set_date(date(2020, 9, 3))
    sl1.add_item(i1, 1)
    sl1.add_item(i4, 1)
    sl1.add_item(i4, 1)
    sl1.add_item(i2, 2)
    sl1.create()

    add_missing(sl1, True)
    # item 1, need 5, have 2, on list 1 ( need to add 2 )
    # item 2, need 2, have 1, on list 2
    # item 3, need 3, have 0, not on list ( need to add 3 )
    # item 4, need 7, have 2, on list 2 ( need to add 3 )

    c.execute(
        'select item_id, quantity from shop_list_item where list_id = ?', (sl1.id, ))
    res = c.fetchall()
    assert len(res) == 7

    check_item(i1.id, res, 3)
    check_item(i2.id, res, 2)
    check_item(i3.id, res, 3)
    check_item(i4.id, res, 5)


if __name__ == '__main__':
    test_main()
    test_missing()
