from queue import Queue


class Issuer:

    def __init__(self, command_queue: Queue) -> None:
        self.command_queue = command_queue

    def submit(self, user_command: list[str]) -> None:
        # todo: This calls directly to the kernel
        self.command_queue.put(user_command)
