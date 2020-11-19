# In this exercise, we will write a very simple 2-stage parser (i.e.
# one with a separate lexer) using coroutines (one for the lexer and
# one for the parser itself). The protocol is as follows:
#
#  • the parser will get the lexer in the form of a generator
#    object as an argument,
#  • the parser will ‹yield› individual statements,
#  • the parser will use ‹next(lexer)› to fetch a token when it
#    needs one,
#  • the language has ‘include’ directives: the parser may need to
#    instruct the lexer to switch to a different input file, which
#    it'll do by ‹send›-ing it the name of that file.
#
# For simplicity, the lexer will get a ‹dict› with file names as
# keys and file content as values (both strings). It will start by
# lexing the file named ‹main›. When the lexer reaches an end of
# an included file, it will continue wherever it left off in the
# stream which was interrupted by the include directive.

# There are 4 basic lexeme (token) types: keyword, identifier,
# number (literal) and a linebreak (which ends statements). The
# keywords are: ‹set›, ‹add›, ‹mul›, ‹print› and ‹include›.
# Identifiers are made of letters (‹isalpha›) and literals are made
# of digits (‹isdecimal›). Statements are of these forms:
#
#    [set|add|mul] ident [num|ident]
#    print ident
#    include ident
#
# A statement to be yielded is a 2- or 3-tuple, starting with the
# keyword as a string, followed by the operands (‹int› for literals,
# strings for identifiers). E.g. ‹mul x 3› shows up as ‹('mul', 'x',
# 3)›. The include statement is never ‹yield›-ed.
