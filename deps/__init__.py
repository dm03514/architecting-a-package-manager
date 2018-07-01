from deps.trees.dep_tree import DepTree


def main(decoder, deps_repo):

    return DepTree(
        decoder.decode(),
        deps_repo,
    )


class Dep:

    def __init__(self, name, version, deps=[]):
        self.name = name
        self.version = version
        self.deps = deps

    def add_dependency(self, dep):
        self.deps.append(dep)

    def add_dependencies(self, deps):
        self.deps.extend(deps)
