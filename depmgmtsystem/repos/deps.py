from abc import abstractmethod, ABC


class Repo(ABC):

    @abstractmethod
    def deps(self, package_name):
        pass


class HTTPRepo(Repo):

    def deps(self, package_name):
        raise NotImplementedError
