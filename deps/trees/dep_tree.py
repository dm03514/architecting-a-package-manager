import logging

from deps import Dep

logger = logging.getLogger(__name__)


class DepTree:
    """
    Creates a dependency hierarchy from a list of dependencies.
    Builds Depdency tree from deps repo provided.
    """
    def __init__(self, deps_list, repo):
        self.deps_list = deps_list
        self.repo = repo

    def tree(self):
        """
        Performs depth first search on all dependencies.
        Applies semver matching to ensure that packages available
        from the repo comply with the versions specified in deps_list.

        :raises: DependencyVersionConstraintError
        :return:
        """
        stack = []
        root = Dep(name='root', version=None, deps=self.deps_list)

        logger.debug('seeding root dependencies: {}'.format(self.deps_list))
        stack.extend(self.deps_list)

        while stack:
            current = stack.pop()
            logger.debug('fetching_dependencies: {}'.format(current))
            deps_list = self.repo.deps()
            current.add_dependencies(deps_list)
            stack.extend(deps_list)

        return root
