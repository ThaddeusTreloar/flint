from util import panic, unimplemented, kernel_exit
import init
from typing import Optional
from abstract import Kernel


def main() -> None:

    kernel: Kernel = init.init()

    kernel.start()


if __name__ == "__main__":
    main()
