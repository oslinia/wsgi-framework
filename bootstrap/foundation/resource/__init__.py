import os
import sys

from .config import configuration
from .routing import write
from ..http.routing import Routing
from ..http.routing.map import mapper


def import_module(import_name: str):
    dirname = os.path.dirname(file := sys.modules[import_name].__file__)

    if not file.endswith('.__init__py'):
        return f"{os.path.splitext(import_name)[0]}." if '.' in import_name else '', dirname

    return import_name, dirname


def initialization(import_name: str):
    import_name, dirname = import_module(import_name)

    file = f"{dirname}{os.sep}resource{os.sep}routing.py"

    if mapper(file, dirname, import_name):
        write(file)

    module = __import__(f"{import_name}resource.routing", fromlist=['*'])

    Routing.patterns = module.patterns
    Routing.masks = module.masks

    configuration(module.links, import_name, dirname)
