from sys import exc_info

def panic(e):

    if hasattr(e, 'message'):
        print("Panicked!: %s" % (e.message))
    else:
        print("Panicked! No message provided for %s" % (exc_info()[0]))

    exit()

def console_exit(*args):
    exit()