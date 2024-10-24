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

from myTools import tree_walker, get_file_extension

__koncovky__ = ('aux', 'log', 'gz')

__path__ = '/Users/david/Documents/work/O2/administrativa/TimeSheets/2018/'   #akceptaky


def filter_files(soubory):
    output = []
    for name in soubory:
        for extension in __koncovky__:
            _, ext = get_file_extension(name)
            if extension == ext:
                output.append(name)
                break
    return output


if __name__ == "__main__":
    cesta = __path__
    print(cesta)
    files = tree_walker(cesta, False)
    keSmazani = filter_files(files)
    print(keSmazani)
    for soubor in keSmazani:
        os.remove(soubor)
    print('{} files removed'.format(len(keSmazani)))

