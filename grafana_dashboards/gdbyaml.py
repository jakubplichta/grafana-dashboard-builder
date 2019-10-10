import yaml
from yaml import *
import logging
import os.path
import functools


log = logging.getLogger(__name__)


class GDBLoaderMeta(type):

    def __new__(metacls, __name__, __bases__, __dict__):
        """Add include constructer to class."""

        # register the include constructor on the class
        cls = super().__new__(metacls, __name__, __bases__, __dict__)
        cls.add_constructor('!include', cls.construct_include)

        return cls


class GDBLoader(yaml.Loader, metaclass=GDBLoaderMeta):
    """YAML Loader with `!include` constructor."""

    def __init__(self, stream):
        """Initialise Loader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)

    def construct_include(self, node):
        """Include file referenced at node."""

        filename = os.path.abspath(os.path.join(
            self._root, self.construct_scalar(node)
        ))
        extension = os.path.splitext(filename)[1].lstrip('.')

        with open(filename, 'r') as f:
            if extension in ('yaml', 'yml'):
                return yaml.load(f, GDBLoader)
            else:
                return ''.join(f.readlines())


# Set MyLoader as default.
load = functools.partial(yaml.load, Loader=GDBLoader)

if __name__ == '__main__':
    with open('foo.yaml', 'r') as f:
        data = load(f)
    print(data)