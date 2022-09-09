from threading import Lock


class Printer:

    def __init__(self, print_lock: Lock) -> None:
        self.print_lock = print_lock
