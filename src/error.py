'''
'''

class NotImplementedError(Exception):

    def __init__(self, msg):

        self.msg = msg

class ModelNotTrainedError(Exception):

    def __init__(self, msg):

        self.msg = msg

class InsufficientArgumentsError(Exception):

    def __init__(self, msg):

        self.msg = msg