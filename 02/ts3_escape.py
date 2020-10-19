# Big Corp has an in-house knowledge base / information filing
# system. It does many things, as legacy systems are prone to, and
# many of them are somewhat idiosyncratic. Either because the
# relevant standards did not exist at the time, or the responsible
# programmer didn't like the standard, so they rolled their own.

# The system has become impossible to maintain, but the databases
# contain a vast amount of information and are in active use. The
# system will be rewritten from scratch, but will stay
# backward-compatible with all the existing formats. You are on the
# team doing the rewrite (we are really sorry to hear this, honest).

# The system stores structured documents, and one of its features is
# that it can format those documents using templates. However, the
# template system got a little out of hand (they always do, don't
# they) and among other things, it is «recursive». Each piece of
# information inserted into the template is itself treated as a
# template and can have other pieces of the document substituted.

# A template looks like this:

template_1 = '''The product ‘${product}’ is made by ${manufacturer}
in ${country}. The production uses these rare-earth metals:
#{ingredients.rare_earth_metals} and these toxic substances:
#{ingredients.toxic}.'''

# The system does not treat ‹$› and ‹#› specially, unless they are
# followed by a left brace. This is a rare combination, but it turns
# out it sometimes appears in documents. To mitigate this, the
# sequences ‹$${› and ‹##{› are interpreted as literal ‹${› and
# ‹#{›. At some point, the authors of the system realized that they
# need to write literal ‹$${› into a document. So they came up with
# the scheme that when a string of 2 or more ‹$› is followed by a
# left brace, one of the ‹$› is removed and the rest is passed
# through. Same with ‹#›.

# Your first task is to write functions which escape and un-escape
# strings using the scheme explained above. The template component
# of the system is known simply as ‘template system 3’, so the
# functions will be called ‹ts3_escape› and ‹ts3_unescape›.
# Return the altered string. If the string passed to ‹ts3_unescape›
# contains the sequence ‹#{› or ‹${›, throw RuntimeError, since
# such string could not have been returned from ‹ts3_escape›.
# Once you are done, continue to ‹ts3_normalize.py›.


def ts3_escape(string):
    dollars = 0
    res1 = ""
    for c in string:
        if c == "$":
            dollars += 1
            continue
    
        if dollars > 0 and c == "{":
            res1 += (dollars + 1) * "$" + "{"
            dollars = 0
            continue

        if dollars > 0 and c != "{":
            res1 += dollars * "$" + c
            dollars = 0
            continue

        res1 += c

    if dollars > 0:
        res1 += dollars * "$"
    
    hashtags = 0
    res2 = ""
    for c in res1:
        if c == "#":
            hashtags += 1
            continue
    
        if hashtags > 0 and c == "{":
            res2 += (hashtags + 1) * "#" + "{"
            hashtags = 0
            continue

        if hashtags > 0 and c != "{":
            res2 += hashtags * "#" + c
            hashtags = 0
            continue
    
        res2 += c

    if hashtags > 0:
        res2 += hashtags * "#"

    return res2

def ts3_unescape(string):
    dollars = 0
    res1 = ""
    for c in string:
        if c == "$":
            dollars += 1
            continue

        if dollars >= 2 and c == "{":
            res1 += (dollars - 1) * "$" + "{"
            dollars = 0
            continue

        if dollars > 0 and c != "{":
            res1 += dollars * "$" + c
            dollars = 0
            continue

        res1 += c

    if dollars > 0:
        res1 += dollars * "$"

    hashtags = 0
    res2 = ""
    for c in res1:
        if c == "#":
            hashtags += 1
            continue

        if hashtags >= 2 and c == "{":
            res2 += (hashtags - 1) * "#" + "{"
            hashtags = 0
            continue

        if hashtags > 0 and c != "{":
            res2 += hashtags * "#" + c
            hashtags = 0
            continue

        res2 += c

    if hashtags > 0:
        res2 += hashtags * "#"

    return res2

def test_main():

    pairs = [
        ("", ""),
        ("aa", "aa"),
        ("$", "$"),
        ("{", "{"),
        ("${", "$${"),
        ("$${", "$$${"),
        ("$$ {", "$$ {"),
        ("${$", "$${$"),
        ("$$${", "$$$${"),
        ("ab${ nabc$$${{tsk$$$${asd${${}}}aa$a{",
         "ab$${ nabc$$$${{tsk$$$$${asd$${$${}}}aa$a{"),

        ("#", "#"),
        ("#{", "##{"),
        ("#{{", "##{{"),
        ("####{", "#####{"),
        ("#}{", "#}{"),
        ("$#{", "$##{"),
        ("#${", "#$${"),

        ("$#{}${##}##{$}%${##${$$${{${",
         "$##{}$${##}###{$}%$${##$${$$$${{$${")
    ]

    for unescaped, escaped in pairs:
        err = "ts3_escape( '{}' ) did not match '{}'".format(
            unescaped, escaped)
        assert ts3_escape(unescaped) == escaped, err
        err = "ts3_unescape( '{}' ) did not match '{}'".format(
            escaped, unescaped)
        assert ts3_unescape(escaped) == unescaped, err


if __name__ == "__main__":
    test_main()
