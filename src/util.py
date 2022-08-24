'''
Flint: free and open ML/NN financial forecasting software
Copyright (C) 2021 Thaddeus Treloar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.txt.
'''


from sys import exc_info
from traceback import print_tb
from inspect import getouterframes, currentframe
from termcolor import colored

def panic(m: str):
    '''
    Causes program to panic.
    If debug logging is enabled then this will log the Resulting error and trace.
    '''

    # Need to add systrace logging here.
    # Will rely on settings for logfile paths and verbosity

    if m:
        print("Panicked!: %s" % (m))
    else:
        print("Panicked! No message provided for %s" % (exc_info()[0]))
        print_tb(exc_info()[2])

    exit()

def kernel_exit():
    exit(0)

def unimplemented():
    print(colored("\n!!Code branch unimplemented!!\n\nSee frame information below:\n", 'red'))
    f_info = getouterframes(currentframe().f_back)
    # Prettify this output.
    print(f_info)
    print()
    panic(NotImplementedError("Branch unimplemented"))



def helpDialogue(elements: list[str]) -> str:

    buffer = ""

    for element in elements:
        buffer += element
        buffer += "\n\t"

    return buffer