#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Library of useful tools.

Created on Aug 19, 2010

@author: David Potucek
'''


def contains(data, pattern, case_sensitive = False):
    """ returns count of string patterns found in string data. Not case sensitive by default."""
    if case_sensitive:
        return data.count(pattern)  # de facto duplikace standardniho count, zvazit jestli nechat
    else:
        data = data.lower()
        pattern = pattern.lower()
        return data.count(pattern)


def __test_contains():
    name = "pAko"
    data = " super velky PAKO jako prako pAko pako PAKO"
    print("py string: " + data + "\nhledany retezec: " + name)
    print("not case sensitive: ", contains(data, name))  # testovani moji metodou
    print('case sensitive: {}'.format(contains(data, name, True)))
    print("case sensitive builtin: {}".format(data.count(name)))  # testovani pres built in metodu


def tree_walker(root, recursive=True):
    """
    walks given root dir and subdirectories. Return all files in tuple of
    their respective full paths. If recursive == False, returns only files
    in current dir.
    """
    import os
    files = []
    tree = os.walk(root)  # element indexes: 0 current path; 1 dir list; 2 file list
    for element in tree:
        for g_file in element[2]:
            filename = element[0] + '/' + g_file
            files.append(filename)
        if not recursive:
            break
    return tuple(files)


def __test_tree_walker():
    path = '/home/david/Documents/versioned/pokusy'
    ll = tree_walker(path)
    for el in ll:
        filename = el.name
        print(filename)


def separate_full_path(full_path):
    """ Gets full path string, returns tuple of path and filename. Separates string
    after last /, names it filename. The rest is path. Handles no errors. """
    index = full_path.rfind('/')
    index += 1
    path = full_path[:index]
    file_name = full_path[index:]
    return tuple([path, file_name])


def __test_separate_full_path():
    full_path = '/home/david/workspace/python/experiments/src/fileTools.py'
    print(full_path)
    print(separate_full_path(full_path))


def strip_extension(full_path, rename = True):
    """ takes full path, strips extension and renames file to file without
    last extension.
    :param full_path - path of the file
    :param rename - flag if the file shall be renamed right now. Default True
    """
    import sys, os
    try:
        index = full_path.rindex('.')
    except ValueError:
        print("ERROR: invalid filename, no extension found!")
        sys.exit(1)

    new_path = full_path[:index]
    if rename:
        try:
            os.rename(full_path, new_path)
        except OSError:
            print("ERROR! %s" % OSError.__doc__)
    return new_path


def __test_strip_extension():
    path = "/home/david/temp/py/tohle.je.testovaci.file.txt"
    strip_extension(path)
    print("py done")


def strip_czech_chars(czech_string):
    """Recodes Czech characters to ASCII together with special ones."""
    import unicodedata
    line = unicodedata.normalize('NFKD', czech_string)
    output = ''
    for c in line:
        if not unicodedata.combining(c):
            output += c
    return output

def get_file_extension(soubor):
    """returns extension of the file if it has some"""
    try:
        index = soubor.rindex('.')
    except ValueError:
        index = 0
    name = soubor[:index]
    extension = soubor[index+1:]
    return name, extension

def __test_strip_czech_chars():
    line = "Å½luÅ¥ouÄkÃ½ kÅ¯Å pÄl ÄÃ¡belskÃ© Ã³dy"
    print("before stripping: " + line)
    print("after stripping: " + strip_czech_chars(line))

def convert_in_2_mm(value):
    """ converts inch value to milimeter (1 in = 25,4 mm)"""
    mm_value = value * 25.4
    return mm_value


def convert_mm_2_in(value):
    """converts mm value to inch"""
    in_value = value / 25.4
    return in_value


def read_data_file(file):
    """Reads file supplied as argument. ';' and '#' is taken as comment, data in file are assumed to start at position
    'STARTOFDATA', to end with statement 'ENDOFDATA'. Everything before and after this block is ignored. StartOfData
    must be closer to the header of the file then EndOfData mark. Order is not checked, if EndOfData is found first in
    sourcce file, you will get no data, no error messages supplied.
    :param file: file to parse
    :return: tuple of data lines in file
    """
    data_lines = []
    pridej = False
    with open(file) as file:
        for line in file:
            if line.startswith(';') or line.startswith('#'):
                continue
            if line.startswith('STARTOFDATA'):
                pridej = True
                continue
            if line.startswith('ENDOFDATA'):
                pridej = False
                break
            if pridej:
                data_lines.append(line)
    return tuple(data_lines)

def num_usr_in(prompt_str, default):
    """Prints prompt on screen, awaits user input and if the value is acceptable, returns it.
    If it is not, returns default
    :param prompt_str - message to the user
    :param default - if user inputs no number or nothing at all, default will be used.
    :return value given by user or default"""
    try:
        temp = float(input(prompt_str + ' [' + str(default) + ']: \n'))
        return temp
    except ValueError:
        print('incorrect value input, using {}'.format(default))
        return default

def str_enum_usr_in(prompt, enum, default):
    """Prints prompt on screen, awaits user input and if the value is in enum, returns it.
    If it is not, returns default.
    :param prompt - message to the user
    :param enum - enumeration of options
    :param default - if user inputs no number or nothing at all, default will be used.
    :return value given by user or default"""
    retezec = input(prompt + ' ' + str(enum) + ': \n')
    if retezec in enum:
        return retezec
    else:
        print('incorrect value, using {}!'.format(default))
        return default

def rename_files(dict):
    '''renames files defined in dictionary. key = old name, value = new name. Expects full 
    paths in both filenames.
    :param: dict    dictionary of file names to rename
    :return null
    '''
    import shutil
    for old, new in dict.items():
        shutil.move(old, new)

def prepare_counter(number, places=3):
    '''pripravi counter v pevnem cislovani.
    :param number, pocet mist
    :return cislo doplnene z leva nulami na pozadovany pocet mist. Default = 3.'''
    form = '{:0' + str(places) + 'd}'   #  priprava formatovaciho stringu
    return form.format(number)



if __name__ == "__main__":
    # print(deg2rad(23))
        __test_contains()
    #    __testTreeWalker()
    #    __testSeparateFullPath()
    #    __testStripExtension()
    # __testStripCzechChars()
    # x = numUsrIn('zadej cislo', 42)
    # x = strEnumUsrIn("zadej neco ze seznamu", ('a', 'b'), 'a')
