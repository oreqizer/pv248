# Write a coroutine-based parser for mbox files. It should yield
# elements of the message as soon as it has enough bytes. The input
# will be an iterable, but not indexable, sequence of characters.
#
# The reported elements are as follows:
#
#  • message: Yield a tuple of two integers: the index of the mail
#    in the input file (i.e. 1 for the first mail, 2 for the
#    second and so on) and the offset from the start of the file to
#    the 'F' in 'From '. Yield as soon as you read the 'From '
#    sequence that delimits the message.
#  • header: Yield a tuple with two strings, the name of the field
#    and the content. Yield as soon as you read the first character
#    of the next header field, or the body separator.
#  • body: Yield a single string with the entire body in it.
#
# In an mbox file, each message starts with a line like this:
#
#    From someone@example.com Wed May  1 06:30:00 MDT 2019
#
# After which, an rfc-822 e-mail follows, with any lines that start
# with ‘From ’ changed to ‘>From ’ (do not forget to un-escape
# those). The headers are separated from the rest of the body by a
# single blank line. Headers may continue on the next line with an
# indent.

# States
FRESH = 0
FROM_LINE = 1
HEADERS = 2
HEADER_LINE = 3
HEADER_NEWLINE = 4
BODY = 5

def parse_mbox(chars):
    state = FRESH
    buffer = ""
    line = ""
    mails = 1
    header = ""
    for i, c in enumerate(chars):
        if state == FRESH:
            buffer += c
            # new mail
            if buffer == "From ":
                yield (mails, i-4)
                mails += 1
                state = FROM_LINE
            
            continue

        if state == HEADERS:
            buffer += c
            if buffer in ["From: ", "To: ", "Subject: "]:
                header = buffer
                buffer = ""
                state = HEADER_LINE
            continue

        if state == BODY:
            line += c
            if line == "From ":
                yield buffer
                yield (mails, i-4)
                mails += 1
                buffer = ""
                line = ""
                state = FROM_LINE
                continue
            if line == ">From ":
                line = "From "
            if c == "\n":
                buffer += line
                line = ""
            continue

        if state == FROM_LINE:
            if c == "\n":
                buffer = ""
                state = HEADERS
            continue

        if state == HEADER_LINE:
            if c == "\n":
                state = HEADER_NEWLINE
            else:
                buffer += c
            continue

        if state == HEADER_NEWLINE:
            if c == " ":
                buffer += c
                state = HEADER_LINE
                continue

            yield (header[:-2], buffer)
            buffer = ""
            header = ""
            if c == "\n":
                state = BODY
            else:
                buffer += c
                state = HEADERS
            continue
    
    yield buffer

class FileIter:

    def __init__(self, filename):
        self.file = open(filename, "r")
        self.chars_given = 0

    def __iter__(self):
        return self

    def __next__(self):
        c = self.file.read(1)
        if not c:
            self.file.close()
            raise StopIteration
        self.chars_given += 1
        return c


def test_main():
    f = FileIter("mbox.txt")
    g = parse_mbox(f)

    item = next(g)
    assert item == (1, 0)
    assert f.chars_given == 5

    item = next(g)
    assert item == ('From', 'Author <author@example.com>')
    # 44 + 34 + 1  ( line1 + line2 + check that not whitespace )
    assert f.chars_given == 79

    item = next(g)
    assert item == ('To', 'Recipient <recipient@example.com>')
    assert f.chars_given == 117  # 79 + 38

    item = next(g)
    assert item == ('Subject', 'Sample message 1')
    assert f.chars_given == 143

    item = next(g)
    assert item == 'This is the body.\n' \
                   'From (should be escaped).\n' \
                   'Fromage?\n' \
                   'There are 4 lines.\n' \
                   '\n'
    assert f.chars_given == 222

    item = next(g)
    assert item == (2, 217)
    assert f.chars_given == 222

    item = next(g)
    assert item == ('From', 'Author <author2@example.com>')
    assert f.chars_given == 297

    item = next(g)
    assert item == ('To', 'Rec <rec@example.com>, Rec2 <rec2.2@example.com>')
    assert f.chars_given == 351

    item = next(g)
    assert item == ('Subject', 'Sample message 2')
    assert f.chars_given == 377

    item = next(g)
    assert item == "This is the second body.\n"
    assert f.chars_given == 407

    item = next(g)
    assert item == (3, 402)
    assert f.chars_given == 407

    item = next(g)
    assert item == ('From', 'Author <author3@example.com>')
    assert f.chars_given == 482

    item = next(g)
    assert item == ('To', 'Recipient <recipient36@example.com>')
    assert f.chars_given == 522

    item = next(g)
    assert item == ('Subject', 'Msg 3')
    assert f.chars_given == 537

    item = next(g)
    assert item == "Msg body 3.\n"
    assert f.chars_given == 549

    try:
        next(g)
        assert False
    except StopIteration:
        pass


if __name__ == "__main__":
    test_main()
