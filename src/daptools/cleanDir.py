#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
cleanDir
Clears files of following types: *.aux, *.log, *.gz produced by LaTeX.
Dir location is specified in __path__ 

Created on 18/05/2017, 13:14

@author: David Potucek
'''

import os

from .myTools import tree_walker, get_file_extension

__koncovky__ = ('aux', 'log', 'gz')

__path__ = '/Users/david/Documents/work/O2/administrativa/TimeSheets/2018/'   #akceptaky


def filter_files(soubory):
    output = []
    for name in soubory:
        _, ext = get_file_extension(name)  # Extract extension once
        if ext in __koncovky__:
            output.append(name)
    return output


if __name__ == "__main__":
    cesta = __path__
    print(cesta)
    files = tree_walker(cesta, False)
    keSmazani = filter_files(files)
    print(keSmazani)
    for soubor in keSmazani:
        try:
            os.remove(soubor)
        except (OSError, FileNotFoundError) as e:
            print(f"Failed to remove {soubor}: {e}")
    print('{} files removed'.format(len(keSmazani)))

