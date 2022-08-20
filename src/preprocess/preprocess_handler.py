from abstract.handler import Handler
from generics.preprocess import Preprocess

class PreProcessHandler(Handler):

    def __init__(self, module_path: Path):

        super.__init__(self, Preprocess, module_path)

    def setSequence


    