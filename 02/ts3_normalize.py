# Eventually, we will want to replicate the actual substitution into
# the templates. This will be done by the ‹ts3_render› function.
# However, somewhat surprisingly, that function will only take one
# argument, which is the structured document to be converted into a
# string. Recall that the template system is recursive: before
# ‹ts3_render›, another function, ‹ts3_combine› combines the
# document and the templates into a single tree-like structure. One
# of your less fortunate colleagues is doing that one.

# This structure has 5 types of nodes: lists, maps, templates
# (strings), documents (also strings) and integers. In the original
# system there are more types (like decimal numbers, booleans and so
# on) but it has been decided to add those later.  Many documents
# only make use of the above 5.

# A somewhat unfortunate quirk of the system is that there are
# multiple types of nodes represented using strings. The way the
# original system dealt with this is by prefixing each string by its
# type; ‹$document$ › (with a trailing space!) and ‹$template$ ›.
# Those prefixes are stored in the database. To make matters worse,
# there are strings with no prefix: earlier versions looked for ‹${›
# and ‹#{› sequences in the string, and if it found some, treated
# the string as a template, and as a document otherwise.

# The team has rightly decided that this is stupid. You drew the
# short straw and now you are responsible for function
# ‹ts3_normalize›, which takes the above slightly baroque structure
# and sorts the strings into two distinct types, which are
# represented using Python classes. Someone else will deal with
# converting the database ‘later’.

import copy


class Document:
    pass


class Template:
    pass

# Each of the above classes should have an attribute called ‹text›,
# which is a string and contains only the actual text, without the
# funny prefixes. The lists, maps and integers fortunately arrive as
# Python ‹list›, ‹dict› and ‹int› into this function. Return the
# altered tree: the strings substituted for their respective types.


def ts3_normalize(tree):
    pass


def test_map():

    tree = {'templ': "$template$ insert ${product} names: #{product.names}"}
    tree_orig = copy.deepcopy(tree)
    norm = ts3_normalize(tree)

    assert tree == tree_orig  # do not modify the tree in place
    assert len(norm) == 1
    assert type(norm['templ']) == Template
    assert norm['templ'].text == "insert ${product} names: #{product.names}"


def test_list():

    tree = {'templs': ["${product}", "#{products}",
                       "$template$ main: ${product}, other: ${products}"]}
    tree_orig = copy.deepcopy(tree)
    norm = ts3_normalize(tree)

    assert tree == tree_orig
    assert len(norm) == 1
    assert len(norm['templs']) == 3
    for t in norm['templs']:
        assert type(t) == Template
    assert norm['templs'][0].text == "${product}"
    assert norm['templs'][1].text == "#{products}"
    assert norm['templs'][2].text == "main: ${product}, other: ${products}"

    tree = ["instructions of use: please do not use", 7,
            "instructions: ${instructions}", "documentation ##{}"]
    tree_orig = copy.deepcopy(tree)
    norm = ts3_normalize(tree)

    assert tree == tree_orig
    assert len(norm) == 4
    assert type(norm[0]) == Document
    assert type(norm[1]) == int
    assert type(norm[2]) == Template
    assert type(norm[3]) == Document


def test_complex():

    tree = {'names': ["Name1", "Name: ${name}", "Names: #{names}", "Name ###{$}", 1, "Oscar"],
            'tpls': {'tpl1': 0, 'tpl2': " $document$ abc", 'tpl3': "ab${t}",
                     'tpl4': ['a', "$$doc", "$document$ ", {'root': "$document@ no? #{${e}}",
                                                            'foo': 78,
                                                            'foo2': "$document$ $template$ neither"}]},
            'not-tpls': 9}

    tree_orig = copy.deepcopy(tree)
    norm = ts3_normalize(tree)
    assert tree == tree_orig

    assert len(norm) == 3
    assert type(norm['not-tpls']) == int

    assert len(norm['names']) == 6
    assert type(norm['names'][0]) == Document
    assert type(norm['names'][1]) == Template
    assert type(norm['names'][2]) == Template
    assert type(norm['names'][3]) == Document
    assert type(norm['names'][4]) == int
    assert type(norm['names'][5]) == Document

    assert norm['names'][0].text == "Name1"
    assert norm['names'][1].text == "Name: ${name}"
    assert norm['names'][2].text == "Names: #{names}"
    assert norm['names'][3].text == "Name ###{$}"
    assert norm['names'][4] == 1
    assert norm['names'][5].text == "Oscar"

    assert len(norm['tpls']) == 4
    assert type(norm['tpls']['tpl1']) == int
    assert type(norm['tpls']['tpl2']) == Document
    assert type(norm['tpls']['tpl3']) == Template
    assert type(norm['tpls']['tpl4']) == list

    assert norm['tpls']['tpl1'] == 0
    assert norm['tpls']['tpl2'].text == " $document$ abc"
    assert norm['tpls']['tpl3'].text == "ab${t}"

    assert len(norm['tpls']['tpl4']) == 4
    assert type(norm['tpls']['tpl4'][0]) == Document
    assert type(norm['tpls']['tpl4'][1]) == Document
    assert type(norm['tpls']['tpl4'][2]) == Document
    assert type(norm['tpls']['tpl4'][3]) == dict

    assert norm['tpls']['tpl4'][0].text == "a"
    assert norm['tpls']['tpl4'][1].text == "$$doc"
    assert norm['tpls']['tpl4'][2].text == ""

    assert len(norm['tpls']['tpl4'][3]) == 3
    assert type(norm['tpls']['tpl4'][3]['root']) == Template
    assert type(norm['tpls']['tpl4'][3]['foo']) == int
    assert type(norm['tpls']['tpl4'][3]['foo2']) == Document

    assert norm['tpls']['tpl4'][3]['root'].text == "$document@ no? #{${e}}"
    assert norm['tpls']['tpl4'][3]['foo2'].text == "$template$ neither"


def test_main():

    test_map()
    test_list()
    test_complex()


if __name__ == "__main__":
    test_main()
