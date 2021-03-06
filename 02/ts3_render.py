# At this point, we have a structure made of ‹dict›, ‹list›,
# ‹Template›, ‹Document› and ‹int› instances. The lists and maps
# can be arbitrarily nested. Within templates, the substitutions
# give dot-separated paths into this tree-like structure. If the
# top-level object is a map, the first component of a path is a
# string which matches a key of that map. The first component is
# then chopped off, the value corresponding to the matched key is
# picked as a new root and the process is repeated recursively. If
# the current root is a list and the path component is a number, the
# number is used as an index into the list.

# If a ‹dict› meets a number in the path (we will only deal with
# string keys), or a ‹list› meets a string, raise a ‹RuntimeError›
# and let someone else deal with the problem later.

# The ${path} substitution performs «scalar rendering», while
# #{path} substitution performs composite rendering. Scalar
# rendering resolves the path to an object, and depending on its
# type, performs the following:
#
#  • if it is a Document, replace the ${...} with the text of the
#    document; the pasted text is excluded from further processing,
#  • if it is a Template, the ${...} is replaced with the text of
#    the template; occurrences of ${...} and #{...} within the
#    pasted text are further processed,
#  • if it is an ‹int›, it is formatted and the resulting string
#    replaces the ${...},
#  • if it is a list, the length of the list is formatted as if it
#    was an ‹int›, and finally,
#  • if it is a ‹dict›, ‹.default› is appended to the path and the
#    substitution is retried.

# Composite rendering using #{...} is similar, but:
#
#  • a ‹dict› is rendered as a comma-separated (with a space) list
#    of its values, after the keys are sorted alphabetically, where
#    each value is rendered «as a scalar»,
#  • a ‹list› is likewise rendered as a comma-separated list of its
#    values as scalars,
#  • everything else is an error: raise a ‹RuntimeError› for now,
#    someone else will fix that later.

# The top-level entity passed to ts3_render must always be a ‹dict›.
# The starting template is expected to be in the key '$template' of
# that ‹dict›. Remember that ##{...} and $${...} must remain
# untouched. If you encounter nested templates while parsing the
# path, e.g. ${abc${d}}, throw an error (but see also bonus 2
# below).

from ts3_normalize import ts3_normalize


def ts3_render(tree):
    pass

# «Bonus 1»: It turns out that the original system had a bug, where
# a template could look like this: ‹${foo.bar}.baz}› – if
# ‹${foo.bar}› referenced a template and «that» template ended with
# ‹${quux› (notice all the oddly unbalanced brackets!), the system
# would then paste the strings to get ‹${quux.baz}› and proceed to
# perform that substitution.
#
# The real clincher is that template authors started to use this as
# a feature, and now we are stuck with it. Replicate this
# functionality. However, make sure that this does «not» happen when
# the «first» part of the pasted substitution comes from a document!
#
# PS: The original bug would still do the substitution if the second
# part was a document and not a template. Feel free to replicate
# that part of the bug too.  As far as anyone knows, the variant
# with template + document is not abused in the wild, so it is also
# okay to fix it.

# «Bonus 2»: If you encounter nested templates while parsing the
# path, first process the innermost substitutions, resolve the
# inside path and append the path to the outer one, then continue
# resolving the outer path.
#
# Example: ${path${inner.tpl}}, first resolve inner.tpl, append the
# result after `path`, then continue parsing. If the inner.tpl path
# leads to a document with text ".outside.2", the outer path is
# "path.outside.2".


def assert_throws(*args, **kwargs):

    ex = kwargs['ex']
    f = kwargs['f']

    try:
        f(*args)
        raise AssertionError("expected " + str(ex) + " to be thrown")
    except ex:
        return


def test_scalar_individual():

    template = "Here is input: ${input}"

    # Document
    t = {'$template': template, 'input': "blahblah"}
    assert ts3_render(ts3_normalize(t)) == "Here is input: blahblah"

    # Document with '${'
    t = {'$template': template, 'input': "$document$ blah ${t}"}
    assert ts3_render(ts3_normalize(t)) == "Here is input: blah ${t}"

    # list
    t = {'$template': template, 'input': [1, 2, 3]}
    assert ts3_render(ts3_normalize(t)) == "Here is input: 3"

    # dict (.default)
    t = {'$template': template, 'input': {'a': 7, 'default': "abc}"}}
    assert ts3_render(ts3_normalize(t)) == "Here is input: abc}"

    # int
    t = {'$template': template, 'input': -22}
    assert ts3_render(ts3_normalize(t)) == "Here is input: -22"

    # Template
    t = {'$template': template, 'input': "would need ${more.input}",
         'more': {'input': "hello", 'output': "bye"}}
    assert ts3_render(ts3_normalize(t)) == "Here is input: would need hello"


def test_composite_individual():

    # list
    template = "List: #{items} and a dog."
    t = {'$template': template, 'items': ['carrot', 'cat', 'potato']}
    assert ts3_render(ts3_normalize(
        t)) == "List: carrot, cat, potato and a dog."

    # dict, sort(!)
    t = {'$template': template, 'items': {'c': 'foo', 'a': 7,
                                          'd': "$template$ ${foo}", 't': -1, },
         'foo': ['1']}
    assert ts3_render(ts3_normalize(t)) == "List: 7, foo, 1, -1 and a dog."


def test_template():

    template = "Print ${name.idea} and ${name.group.3.people}.."

    # encountering list in path resolution means an index
    t = {'$template': template,
         'name': {'idea': 'fireflies', 'group': [0, 1, 2, {'people': ['Bernard', 'Ann']}]}}
    assert ts3_render(ts3_normalize(t)) == "Print fireflies and 2.."


def test_complex():

    template = "${header}: show me ${person.name} and ${person.age} of #{persons} but not $${ppl}"
    t = {'$template': template, 'header': "automatic", 'person': {'name': "Villa", 'age': 17},
         'persons': ['Villa', 'Serrat']}
    t_orig = t.copy()
    res = "automatic: show me Villa and 17 of Villa, Serrat but not $${ppl}"

    assert ts3_render(ts3_normalize(t)) == res
    assert t == t_orig


def test_composite():

    # composite within composite
    template = "Fields: #{fields}!#}"
    t = {'$template': template, 'fields': ['CS', 'Law', '$template$ Others: #{others}'],
         'others': {'field2': 'Art', 'field3': 'Archery', 'field1': '$document$ Plants'}}

    assert ts3_render(ts3_normalize(
        t)) == "Fields: CS, Law, Others: Plants, Art, Archery!#}"


def test_errors():

    # dict meets a number in the path
    t = {'$template': "${path.0}", 'path': {'foo': 2}}
    assert_throws(ts3_normalize(t), ex=RuntimeError, f=ts3_render)

    # list meets a string in the path
    t = {'$template': "${path.a}", 'path': ['a']}
    assert_throws(ts3_normalize(t), ex=RuntimeError, f=ts3_render)

    # dict end of scalar, no 'default' key
    t = {'$template': "a ${path}", 'path': {'not-default': 1}}
    assert_throws(ts3_normalize(t), ex=RuntimeError, f=ts3_render)

    # composite meets int/Template/Document
    t = {'$template': "#{comp}", 'comp': 7}
    assert_throws(ts3_normalize(t), ex=RuntimeError, f=ts3_render)

    t = {'$template': "#{comp}", 'comp': "$doc"}
    assert_throws(ts3_normalize(t), ex=RuntimeError, f=ts3_render)

    t = {'$template': "#{comp}", 'comp': "$template$ foo"}
    assert_throws(ts3_normalize(t), ex=RuntimeError, f=ts3_render)

    # nested templates
    t = {'$template': "#{ab${t}c}", 'ab': "wrong"}
    assert_throws(ts3_normalize(t), ex=RuntimeError, f=ts3_render)


def test_main():

    test_scalar_individual()
    test_composite_individual()
    test_template()
    test_complex()
    test_composite()
    test_errors()


if __name__ == "__main__":
    test_main()
