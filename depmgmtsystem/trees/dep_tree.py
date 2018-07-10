import logging

from depmgmtsystem.dependencies import Dep

logger = logging.getLogger(__name__)


class DependencyVersionConstraintError(Exception):
    pass


class DepTree:
    """
    Creates a dependency hierarchy from a list of dependencies.
    Builds Depdency tree from depmgmtsystem repo provided.
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
        root = Dep(name='', version=None)
        root.add_dependencies(self.deps_list)

        logger.debug('seeding root dependencies: {}'.format(self.deps_list))
        stack.extend(self.deps_list)

        while stack:
            current = stack.pop()

            logger.debug('current_stack: {}'.format(stack))
            logger.debug('fetching_dependencies: {}'.format(current))

            valid_version = current.highest_valid_version(
                self.repo.deps(current.name)
            )

            if not valid_version:
                raise DependencyVersionConstraintError

            # make sure to pin the current with the actual version
            # available from the repo
            current.version = valid_version.version

            current.add_dependencies(valid_version.deps)

            stack.extend(valid_version.deps)

        logger.debug(root)
        return root
