from sys import argv
from util import panic, unimplemented, kernel_exit
from kernel.kernel_core import CoreKernel
import init

def main():

    #systemArguments = argv
    #systemArgumentsNo = len(systemArguments)

    settings = init.init()
    try:
        settings.kernel_module.start()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        kernel_exit()

if __name__ == "__main__":
    main()