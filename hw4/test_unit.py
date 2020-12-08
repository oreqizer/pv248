import lisp

from classes import Nick, Join, Message, Part, Replay, State, Channel, ChannelMessage, User


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
    want = '(ok)\n'
    assert got == want, f"{got} == {want}"

    print("test_make_ok OK")


def test_make_error():
    # (error "{text}")
    got = lisp.make_error("yikes")
    want = '(error "yikes")\n'
    assert got == want, f"{got} == {want}"

    print("test_make_error OK")


def test_make_message():
    # (message "{channel}" {unix timestamp} "{nickname}" "{text}")
    got = lisp.make_message("#chan", 1337, "oreqizer", "swag")
    want = '(message "#chan" 1337 "oreqizer" "swag")\n'
    assert got == want, f"{got} == {want}"

    print("test_make_message OK")


def test_user():
    user = User("oreqizer", None)
    ch = Channel("#chan")

    # join
    user.join(ch)
    assert len(user.channels) == 1, f"user.join: {len(user.channels)} == 1"

    assert_throw(lambda: user.join(ch))

    # part
    user.part(ch)
    assert len(user.channels) == 0, f"user.part: {len(user.channels)} == 0"

    assert_throw(lambda: user.part(ch))

    # joined
    assert not user.joined(ch), f"user.joined: False"
    user.join(ch)
    assert user.joined(ch), f"user.joined: True"

    print("test_user OK")


def test_channel():
    ch = Channel("#chan")
    user = User("oreqizer", None)

    # join
    ch.join(user)
    assert len(ch.users) == 1, f"ch.join: {len(ch.users)} == 1"

    assert_throw(lambda: ch.join(user))

    # part
    ch.part(user)
    assert len(ch.users) == 0, f"ch.part: {len(ch.users)} == 0"

    assert_throw(lambda: ch.part(user))

    # has
    assert not ch.has(ch), f"ch.joined: False"
    ch.join(user)
    assert ch.has(user), f"ch.joined: True"

    # send
    ch.send(ChannelMessage(user, "kek"))
    assert len(ch.messages) == 1, f"ch.send: {len(ch.messages)} == 1"
    ch.messages = []

    # replay
    now = 1337
    m1 = ChannelMessage(user, "lol")
    m1.timestamp = now - 1
    ch.send(m1)

    m2 = ChannelMessage(user, "kek")
    m2.timestamp = now + 1
    ch.send(m2)
    res = ch.replay(now)
    assert len(res) == 1, f"ch.replay: {len(res)} == 1"
    assert res[0].text == m2.text, f"ch.replay: {res[0].text} == {m2.text}"

    print("test_channel OK")


def test_state():
    chan = "#chan"

    # join
    state = State()
    user = User("oreqizer", None)
    state.join(user, chan)
    assert len(state.channels) == 1, f"state.join: state.channels: {len(state.channels)} == 1"
    ch = state.channels[chan]
    assert len(user.channels) == 1, f"state.join: user.channels: {len(user.channels)} == 1"
    assert len(ch.users) == 1, f"state.join: ch.users: {len(ch.users)} == 1"

    # part
    state = State()
    user = User("oreqizer", None)
    state.join(user, chan)
    ch = state.channels[chan]
    state.part(user, chan)
    assert len(user.channels) == 0, f"state.part: user.channels: {len(user.channels)} == 0"
    assert len(ch.users) == 0, f"state.part: ch.users: {len(ch.users)} == 0"

    # get_channel
    state = State()
    user = User("oreqizer", None)
    assert_throw(lambda: state.get_channel(chan))
    state.join(user, chan)
    ch = state.channels[chan]
    assert state.get_channel(
        chan) == ch, f"state.get_channel: {state.get_channel(chan).name} == {ch.name}"

    # get_user_channel
    state = State()
    user = User("oreqizer", None)
    assert_throw(lambda: state.get_user_channel(user, chan))
    state.users[user.nickname] = user
    assert_throw(lambda: state.get_user_channel(user, chan))
    ch = Channel(chan)
    state.channels[chan] = ch
    assert_throw(lambda: state.get_user_channel(user, chan))
    state.join(user, chan)
    assert state.get_user_channel(
        user, chan) == ch, f"state.get_user_channel: {state.get_user_channel(user, chan).name} == {ch.name}"

    print("test_state OK")


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
    test_user()
    test_channel()
    test_state()
