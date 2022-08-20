from sys import exc_info
from traceback import print_tb
from inspect import getouterframes, currentframe
from termcolor import colored

def panic(e: Exception):
    '''
    Causes program to panic.
    If debug logging is enabled then this will log the Resulting error and trace.
    '''

    # Need to add systrace logging here.
    # Will rely on settings for logfile paths and verbosity

    if hasattr(e, 'message'):
        print("Panicked!: %s" % (e.message))
    else:
        print("Panicked! No message provided for %s" % (exc_info()[0]))
        print_tb(exc_info()[2])

    exit()

def kernel_exit(*args):
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