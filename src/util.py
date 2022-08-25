from sys import exc_info
from traceback import print_tb
from inspect import getouterframes, currentframe
from termcolor import colored
from typing import Union


def panic(m: Union[Exception, str]) -> None:
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


def kernel_exit() -> None:
    exit(0)


def unimplemented() -> None:
    print(colored("\n!!Code branch unimplemented!!\n\nSee frame information below:\n", 'red'))

    frame = currentframe()

    if frame is not None:
        # Prettify this output.
        print(getouterframes(frame.f_back))

    panic(NotImplementedError("Branch unimplemented"))


def helpDialogue(elements: list[str]) -> str:

    buffer = ""

    for element in elements:
        buffer += element
        buffer += "\n\t"

    return buffer
