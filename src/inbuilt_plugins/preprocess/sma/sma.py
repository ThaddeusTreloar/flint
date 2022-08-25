from generics import Preprocess

class Sma(Preprocess):

    @property
    def daemoniseThread(self):
        return False

    @property
    def local_command_set(self):
        pass

    def __init__(self):
        pass

    def someFunction(self):
        print("do some stuff")
        return 3

    @property
    def description(self):
        return 'A simple moving average calculation.'

    def calculate():
        pass

    def listInputs():
        pass

    def help(self, args):
        pass

