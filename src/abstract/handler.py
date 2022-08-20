
from abc import abstractmethod, ABC
from pathlib import Path
from util import unimplemented
from importlib.util import spec_from_file_location, module_from_spec
from generics.generic import Generic

class Handler(ABC):

    def __init__(self, module_type: Generic, module_dir: Path):

        self.module_dir: Path = module_dir
        self.module_type: Generic = module_type
        self.module_tree: dict = build_module_tree(self.module_dir, self.module_type)

    def build_module_tree(self, module_type: Generic):

        if self.module_dir.exists() and self.module_dir.is_dir():
            for child in self.module_dir.iterdir():
                if child.is_dir():
                    # Retrieve from the directory, the spec from .py file of same name inside
                    spec = spec_from_file_location(child.name, child.joinpath(child.name + '.py'))
                    module = module_from_spec(spec)
                    spec.loader.load_module(module)

                    try:
                        # Appending to module tree. Will append the class of childname inside the module
                        module_class = getattr(module, child.name)
                        if isinstance(module_class, self.module_type):
                            self.module_tree[child.name] = module_class
                        else:
                            # todo<0011>: need to add logging here
                            print('module <%s> is of type <%s>' % (child.name, self.module_type))
                            continue

                    except AttributeError:
                        # todo<0011>: need to add logging here
                        unimplemented()

        else:

            # todo: Raise error/use default directory
            unimplemented()