from abc import ABC, abstractmethod


class DepsDecoder(ABC):

    @abstractmethod
    def decode(self):
        return []
