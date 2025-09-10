#!/usr/bin/python
# -*- coding: utf-8 -*-
"""converts inches in textual representation to millimeters.
Works even with inches in fraction.
Allows batch conversion:
input: text file input.txt with one number on line
output: text file output.txt with two numbers on line; first in, second mm.
"""

import csv

__DEBUG = True
__inFile = "input.txt"
__outFile = "output.txt"


def parse_fraction(fraction):
    """ evaluates provided fraction to decadic number """
    if not check_fraction_validity(fraction):
        print("Error in fraction value, aborting")
        return 0
    delimiter = fraction.find('/')
    nominator = float(fraction[0:delimiter])
    denominator = float(fraction[delimiter + 1:])
    return nominator / denominator


def check_fraction_validity(fraction):
    first = fraction.find('/')  # check for double /
    rest = fraction[first + 1:]
    if rest.find('/') != -1:
        return False
    return True


def parse_number(line):
    value = 0
    try:
        if line.find('/') >= 0:
            value = parse_fraction(line)
        else:
            value = float(line)
        return value
    except ValueError:
        print("Invalid number %s" % (line))


def parse_csv(line):
    reader = csv.reader([line], delimiter=',')
    return reader.next()


def read_file():
    """Reads from input file comma delimited strings and converts to values.
    Returns list of rows containing float values"""
    numbers = []
    for line in open(__inFile):
        if (line.startswith('#') or line.startswith('\n')):
            continue
        else:
            fields = parse_csv(line)
            row = []
            for value in fields:
                number = parse_number(value)
                row.append(number)
            numbers.append(row)
    return numbers


def process_convert(values):
    f = open(__outFile, 'w')
    for row in values:
        out_row = []
        from .myTools import convert_in_2_mm
        for str_val in row:
            val = str(convert_in_2_mm(str_val))
            out_row.append(val)
        f.write(str(out_row))
        f.write('\n')
        if __DEBUG: print(out_row)
    f.flush()


if __name__ == "__main__":
    values = read_file()  # reads input file and returns list of string lists
    print("file input.txt read")
    for row in values:
        print(row)
    process_convert(values)  # converts and writes to the output file
    print("file output.txt written")


