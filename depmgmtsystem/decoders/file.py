from depmgmtsystem.decoders.parsers import parse_dependency_str
from . import DepsDecoder


class FileLineDecoder(DepsDecoder):

    def __init__(self, f):
        self.f = f

    def decode(self):
        return [parse_dependency_str(line) for line in self.f]
