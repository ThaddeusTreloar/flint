from sys import argv
from util import panic, unimplemented, kernel_exit
import init

def main():

    #systemArguments = argv
    #systemArgumentsNo = len(systemArguments)

    kernel = init.init()

    try:

        kernel.start()
        
    except KeyboardInterrupt:
        print("\n\nExiting...")
        kernel_exit()

if __name__ == "__main__":
    main()