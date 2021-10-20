from generics.output import Output

class ConsoleOutput(Output):

    pass

def returnInstance() -> Output:

    return ConsoleOutput()