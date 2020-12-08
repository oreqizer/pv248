import lisp

from classes import Nick, Join, Message, Part, Replay


def assert_throw(cb):
    try:
        cb()
        assert False, "no throw happened"
    except:
        pass


def test_parse():
    # invalid inputs
    assert_throw(lambda: lisp.parse('1337'))
    assert_throw(lambda: lisp.parse('nick "oreqizer"'))
    assert_throw(lambda: lisp.parse('(yolo "swag")'))

    print("test_parse OK")


def test_parse_nick():
    # (nick "{nickname}")
    got = lisp.parse('(nick "oreqizer")')
    want = Nick("oreqizer")
    assert got == want, f"{got} == {want}"

    assert_throw(lambda: lisp.parse('(nick "#channel")'))
    assert_throw(lambda: lisp.parse('(nick)'))
    assert_throw(lambda: lisp.parse('(nick "oreqizer" asd)'))
    print("test_parse_nick OK")


def test_parse_join():
    # (join "{channel}")
    got = lisp.parse('(join "#chan")')
    want = Join("#chan")
    assert got == want, f"{got} == {want}"

    assert_throw(lambda: lisp.parse('(join "chan")'))
    assert_throw(lambda: lisp.parse('(join)'))
    assert_throw(lambda: lisp.parse('(join "#oreqizer" asd)'))
    print("test_parse_join OK")


def test_parse_message():
    # (message "{channel}" "{text}")
    got = lisp.parse('(message "#chan" "toxt")')
    want = Message("#chan", "toxt")
    assert got == want, f"{got} == {want}"

    assert_throw(lambda: lisp.parse('(message "chan", "toxt")'))
    assert_throw(lambda: lisp.parse('(message "#oreqizer")'))
    assert_throw(lambda: lisp.parse('(message "#oreqizer" "oreqizer" asd)'))
    print("test_parse_message OK")


def test_parse_part():
    # (part "{channel}")
    got = lisp.parse('(part "#chan")')
    want = Part("#chan")
    assert got == want, f"{got} == {want}"

    assert_throw(lambda: lisp.parse('(part "chan")'))
    assert_throw(lambda: lisp.parse('(part)'))
    assert_throw(lambda: lisp.parse('(part "#chan" asd)'))
    print("test_parse_part OK")


def test_parse_replay():
    # (replay "{channel}" {unix timestamp})
    got = lisp.parse('(replay "#chan" 1337)')
    want = Replay("#chan", 1337)
    assert got == want, f"{got} == {want}"

    assert_throw(lambda: lisp.parse('(replay "#chan")'))
    assert_throw(lambda: lisp.parse('(replay "#chan" 1337 asd)'))
    print("test_parse_replay OK")


def test_make_ok():
    # (ok)
    got = lisp.make_ok()
    want = '(ok)'
    assert got == want, f"{got} == {want}"

    print("test_make_ok OK")


def test_make_error():
    # (error "{text}")
    got = lisp.make_error("yikes")
    want = '(error "yikes")'
    assert got == want, f"{got} == {want}"

    print("test_make_error OK")


def test_make_message():
    # (message "{channel}" {unix timestamp} "{nickname}" "{text}")
    got = lisp.make_message("#chan", 1337, "oreqizer", "swag")
    want = '(message "#chan" 1337 "oreqizer" "swag")'
    assert got == want, f"{got} == {want}"

    print("test_make_message OK")


if __name__ == "__main__":
    test_parse()
    test_parse_nick()
    test_parse_join()
    test_parse_message()
    test_parse_part()
    test_parse_replay()
    test_make_ok()
    test_make_error()
    test_make_message()
