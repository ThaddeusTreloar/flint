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

class NotImplementedError(Exception):

    def __init__(self, msg):

        self.msg = msg

class ModelNotTrainedError(Exception):

    def __init__(self, msg):

        self.msg = msg

class InsufficientArgumentsError(Exception):

    def __init__(self, msg):

class ModuleError(Exception):
    def __init__(self, message: str):
        self.message: str = message