# The goal here is to load the file `report.json` which contains a
# report about a bug in a C program, and print out a simple stack
# trace. You will be interested in the key `active stack` (near the
# end of the file) and its format. The output will be plain text:
# for each stack frame, print a single line in this format:
#
#     function_name at source.c:32
#
# In the next exercise, we will try to write some JSON instead:
# `elements.py`.

import json # go for `load` (via io) or `loads` (via strings)
