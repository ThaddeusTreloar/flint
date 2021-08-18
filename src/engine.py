'''
Flint: free and open ML/NN financial forecasting software
Copyright (C) 2021 Thaddeus Treloar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.txt.
'''

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