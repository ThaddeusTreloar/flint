from sys import argv
from util import panic
import init

def main():

    #systemArguments = argv
    #systemArgumentsNo = len(systemArguments)

    settings = init.init()
    settings.kernel_module.start()

if __name__ == "__main__":
    main()