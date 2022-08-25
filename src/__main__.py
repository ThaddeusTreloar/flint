from sys import argv
from util import panic, unimplemented, kernel_exit
import init
from typing import Optional
from abstract import Kernel

def main():

    #systemArguments = argv
    #systemArgumentsNo = len(systemArguments)

    kernel: Optional[Kernel] = init.init()

    try:

        kernel.start()
        
    except KeyboardInterrupt:
        print("\n\nExiting...")
        kernel_exit()

if __name__ == "__main__":
    main()