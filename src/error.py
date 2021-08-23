'''
Set of custom errors and exceptions specific to Flint.
'''

class ModelNotTrainedError(Exception):

    def __init__(self, message):

        self.message = message

class InsufficientArgumentsError(Exception):

    def __init__(self, message):

        self.message = message

class ConfigLoadError(Exception):

    def __init__(self, message):

        if message:
            self.message = message
            