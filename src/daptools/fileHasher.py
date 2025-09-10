#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
fileHasher - vezme files z adresare (bez subdirs) a prejmenuje je tak, aby 
zacinaly v nahodnem poradi - predradi jim 3 cisla a prida pomlcku. 
Napr. 0007-oldFileName.xyz.
Pouzivam pro muziku.
Created on 27/04/2017, 07:26

@author: David Potucek
"""

import random

from .myTools import tree_walker, separate_full_path, rename_files, prepare_counter, strip_czech_chars

__PATH = '/Users/david/temp/mp3'
__IGNORE_NAMES__ = ('.DS_Store')    # ktere files vynechat
__REPLACE_CHARS__ = ('.', ' ', '-', '_') # ktere znaky vynechat na zacatku filename

def strip_first_alphanumeric(file_name, position=6):
    """odstrani z prvnich x znaku cisla a to co je v __REPLACE_CHARS__
    Funguje pouze na soubory s priponou, ty bez pripony zastavi cely program
    :param file_name name
    :param position - kolik znaku na zacatku prohledavat
    :return  nove jmeno"""
    import sys
    file_name = strip_czech_chars(file_name)
    try:
        index = file_name.rindex('.')    # najdu priponu
    except ValueError:
        print("ERROR: invalid filename, no extension found!")
        sys.exit(1)         # zastavujeme, pres validace proslo neco co nemelo!
    ext = file_name[index:]
    file_name = file_name[:index]
    name_str = file_name[:position]
    rest_str = file_name[position:]
    result = ''.join(i for i in name_str if not (i.isdigit() or i in __REPLACE_CHARS__))
    result = result + rest_str + ext
    return result

def hash_names(f_names, randomize = 0):
    '''k danemu seznamu files vyrobi dictionary se starym a novym filename
    serazene nahodne.
    :param f_names name tuple (full path)
    :param randomize switch 0 means randomize, anything else - no change of order
    :return dictionary of old and new file names (full path)'''
    counter = 1
    l = list(f_names)
    new_names = {}

    directory_path = validate_files(l)

    while len(l) > 0:       # samotna funkce zpracovani file name
        if randomize == 0:
            element = random.choice(l)
        else:
            element = l[counter]
        _, name = separate_full_path(element)
        name_r = strip_first_alphanumeric(name)
        name_new = directory_path + prepare_counter(counter) + '-' + name_r
        new_names[element] = name_new
        l.remove(element)
        counter += 1
    return new_names

def remove_numbers_from_files(f_names):
    ''' Projde dodany list souboru, zvaliduje jejich jmena a vyjme numericke znaky na
    jejich zacatku.
    :param f_names file names tuple (full path)
    :return dictionary of old and new file names (full path)
    '''
    l = list(f_names)
    new_names = {}

    directory_path = validate_files(l)
    while len(l) > 0:
        element = l[0]
        _, name = separate_full_path(element)
        name_strip = strip_first_alphanumeric(name)
        name_new = directory_path + name_strip
        new_names[element] = name_new
        l.remove(element)
    return new_names


def validate_files(l):
    '''Rutina zkontroluje jestli soubor ma priponu a jestli neni v ignorovanych.
    :return directoryPath je full path k danym souborum
    Pozor! modifikuje list l bez toho aby ho vracel!'''
    for nam in l:
        _, n = separate_full_path(nam)
        try:
            _ = n.rindex('.')  # najdu priponu
        except ValueError:        # if nema priponu, vyhodim ho
            l.remove(nam)
            continue
        if n in __IGNORE_NAMES__:   # if je v ignorovanych files, vyhodim ho
            l.remove(nam)
    print('z toho {} platnych'.format(len(l)))
    directory_path, _ = separate_full_path(l[0])  # pripravim si path
    return directory_path


if __name__ == "__main__":
    l = tree_walker(__PATH, False)
    print('nacteno {} files.'.format(len(l)))
    new_names = remove_numbers_from_files(l)        # tohle odstrani ciselne prefixy
    new_names = hash_names(l)                   # tohle zahashuje soubory podle cisel
    # print(newNames)
    rename_files(new_names)
    print('Done!')



