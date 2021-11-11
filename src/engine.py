from importlib import import_module, invalidate_caches
from abc import ABC

import settings as s
import error

class Engine(ABC):

    def __init__(self, engine_path):

        engine_module = import_module(engine_path)
        invalidate_caches()

        self.__train    = engine_module.train
        self.__predict  = engine_module.predict
        self.model      = None

    
    def train(self, args, settings):

        return self.__train(args, settings)

    def predict(self, args, settings):

        if not self.model:

            raise error.ModelNotTrainedError()

        else:

            return self.__predict(args, settings)

def load():
    pass

def list():
    pass