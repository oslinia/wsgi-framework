import os
import sys

from .caching import print_routing
from .config import configure
from ..http import routing
from ..http.map import mapper, Links
from ..http.routing import Routing


def import_module(import_name: str):
    dirname = os.path.dirname(file := sys.modules[import_name].__file__)

    if not file.endswith('.__init__py'):
        return f"{os.path.splitext(import_name)[0]}." if '.' in import_name else '', dirname

    return import_name, dirname


def initialization(import_name: str):
    import_name, dirname = import_module(import_name)

    file = f"{dirname}{os.sep}resource{os.sep}routing.py"

    if mapper(file, dirname, import_name):
        print_routing(file)

    configure(import_name, dirname)

    module = __import__(f"{import_name}resource.routing", fromlist=['*'])

    routing.links = Links(module.links)

    Routing.patterns = module.patterns
    Routing.masks = module.masks
