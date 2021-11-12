from sys import argv
from util import panic, unimplemented
import init

def main():

    #systemArguments = argv
    #systemArgumentsNo = len(systemArguments)

    unimplemented()

    settings = init.init()
    settings.kernel_module.start()

if __name__ == "__main__":
    main()