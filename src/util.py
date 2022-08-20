from sys import exc_info
from traceback import print_tb
from inspect import getouterframes, currentframe

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

def kernel_exit():
    exit(0)

def unimplemented():
    print("Code branch unimplemented.\nSee frame information below:\n")
    f_info = getouterframes(currentframe().f_back)
    # Prettify this output.
    print(f_info)
    kernel_exit()
    