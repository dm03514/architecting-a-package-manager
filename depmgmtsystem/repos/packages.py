from abc import abstractmethod, ABC


class Repo(ABC):

    @abstractmethod
    def download(self, name, version):
        pass
