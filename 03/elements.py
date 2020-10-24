# In this exercise, we will read in a CSV (comma-separated values) file and
# produce a JSON file. The input is in `elements.csv` and each row describes a
# single chemical element. The columns are, in order:
# * the atomic number
# * the symbol (shorthand)
# * the full name of the element
#
# Generate a JSON file which will consist of a list of objects,
# where each object will have attributes 'atomic number', 'symbol' and 'name'.
# The first of these will be a number and the latter two will be strings.
# Name the output file identically to the input file, except for the extension (`.json`).

# Note that the first line of the CSV file is a header.

import csv  # we want csv.reader
import json # and json.dumps


def csv_to_json(filename):
    elements = []
    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        first = True
        for row in spamreader:
            if first:
                first = False
                continue

            num, symbol, name = row
            elements.append({
                'atomic number': int(num),
                'symbol': symbol,
                'name': name,
            })

    res = json.dumps(elements, indent="  ")
    open(filename.replace(".csv", ".json"), "w").write(res)

def test_main():
    csv_to_json("elements.csv")

    with open("elements.json") as js:
        data = json.load(js)

    with open("elements.sol.json") as js_sol:
        data_sol = json.load(js_sol)

    assert data == data_sol

if __name__ == "__main__":
    test_main()

# Let's continue to `json_flatten.py`.
