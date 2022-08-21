from abstract.handler import Handler
from generics.preprocess import Preprocess
from pathlib import Path

class PreProcessHandler(Handler):

    @property
    def module_dir(self):
        return self._module_dir

    @property
    def module_type(self):
        return Preprocess

    def __init__(self, module_path: Path):

        self.local_command_set: dict = {
            "list" : self.listAvailable,
        }

        self._module_dir = module_path.joinpath('preprocess')
        
        if module_path != None:
            self.module_tree: Dict = self.build_module_tree()

        else:
            # Use default path
            self.module_tree: Dict = self.build_module_tree() # not done
            
    def listAvailable(self):
        response = "Module Name\tDescription:\n\n"
        for k, v in self.module_tree.items():
            response+="%s\t%s" % (k, v.description.fget(v))
        
        return response
'''
    @classmethod
    def createSequence(self):
   '''     