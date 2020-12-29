from lisp import parse_test, parse


def test():
    res1 = parse_test("(id id)")
    res2 = parse_test("(id  id)")
    assert res1 == res2, f"{res1} == {res2}"
    
    res1 = parse_test('"str\\""')
    res2 = parse_test(str(res1))
    assert res1 == res2, f"{res1} == {res2}"
    
    res1 = parse_test('"(kek)"')
    res2 = parse_test(str(res1))
    assert res1 == res2, f"{res1} == {res2}"
    
    res1 = parse_test('0')
    res2 = parse_test('(0)')
    assert res1 != res2, f"{res1} != {res2}"
    
    res1 = parse_test('12.7')
    res2 = parse_test(str(res1))
    assert res1 == res2, f"{res1} == {res2}"
    
    res1 = parse_test('-13.37')
    res2 = parse_test(str(res1))
    assert res1 == res2, f"{res1} == {res2}"

    res1 = parse_test("(+ 1 2 3)")
    res2 = parse_test(str(res1))
    assert res1 == res2, f"{res1} == {res2}"

    res1 = parse_test("(eq? [quote (a b c)] (quote a c b))")
    res2 = parse_test(str(res1))
    assert res1 == res2, f"{res1} == {res2}"

    res1 = parse_test('(concat "abc" "efg" "ugly \\\\kek\\\\ \\"string\\"")')
    res2 = parse_test(str(res1))
    assert res1 == res2, f"{res1} == {res2}"

    res1 = parse_test("(set! var ((stuff) #t #f))")
    res2 = parse_test(str(res1))
    assert res1 == res2, f"{res1} == {res2}"

    res1 = parse_test("(< #t #t)")
    res2 = parse_test(str(res1))
    assert res1 == res2, f"{res1} == {res2}"

    res = parse("()()")
    assert res is None, f"{res} is None"

    res = parse(".3")
    assert res is None, f"{res} is None"

    res = parse("(asd)0)")
    assert res is None, f"{res} is None"

    res = parse("()0")
    assert res is None, f"{res} is None"

    res = parse("0()0")
    assert res is None, f"{res} is None"

    res = parse("0()")
    assert res is None, f"{res} is None"

    res = parse('(0]')
    assert res is None, f"{res} is None"

    res = parse('[0)')
    assert res is None, f"{res} is None"

    res = parse('(0 "asd )"')
    assert res is None, f"{res} is None"

    res = parse("(")
    assert res is None, f"{res} is None"

    res = parse(")")
    assert res is None, f"{res} is None"

    res = parse("((asad)")
    assert res is None, f"{res} is None"

    res = parse("(asd))")
    assert res is None, f"{res} is None"

    res = parse("a1 a2")
    assert res is None, f"{res} is None"


if __name__ == "__main__":
    test()
