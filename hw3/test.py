from lisp import parse


def test():
    res1 = parse("(id id)")
    res2 = parse("(id  id)")
    assert res1 == res2, f"{res1} == {res2}"

    res1 = parse("(+ 1 2 3)")
    res2 = parse(str(res1))
    assert res1 == res2, f"{res1} == {res2}"

    res1 = parse("(eq? [quote a b c] (quote a c b))")
    res2 = parse(str(res1))
    assert res1 == res2, f"{res1} == {res2}"

    res1 = parse("12.7")
    res2 = parse(str(res1))
    assert res1 == res2, f"{res1} == {res2}"

    res1 = parse('(concat "abc" "efg" "ugly \\\\kek\\\\ \\"string\\"")')
    res2 = parse(str(res1))
    assert res1 == res2, f"{res1} == {res2}"

    res1 = parse("(set! var ((stuff) #t #f))")
    res2 = parse(str(res1))
    assert res1 == res2, f"{res1} == {res2}"

    res1 = parse("(< #t #t)")
    res2 = parse(str(res1))
    assert res1 == res2, f"{res1} == {res2}"


if __name__ == "__main__":
    test()
