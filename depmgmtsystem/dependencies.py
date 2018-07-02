import semver


def _match_expr(v):
    """
    Builds a match expression from a version which is optionally empty.

    :param v:
    :return:
    """
    ALLOW_ANY_VERSION = '>=0.0.0'
    # cover case where v was not specified, indicating the latest version
    if v is None:
        return ALLOW_ANY_VERSION

    if not v.startswith(('>', '=', '<')):
        return '{}{}'.format('==', v)

    return v


class Dep:

    def __init__(self, name, version, deps=None):
        self.name = name
        self.version = version
        self.deps = deps if deps is not None else []

    def add_dependency(self, dep):
        self.deps.append(dep)

    def add_dependencies(self, deps):
        """
        Adds dependencies to this dep.  Don't inherit or mutate old stuff.

        :param deps:
        :return:
        """
        self.deps.extend(deps)

    def highest_valid_version(self, versions):
        for v in versions:
            if self.is_fulfilled_by(v.version):
                return v
        else:
            return None

    def is_fulfilled_by(self, available_version):
        """
        Checks if this dep version is fulfilled by the `version`
        provided.

        If there is no version specified ie version=None
        we'll set it to '0.0.0' so that all versions are fulfilled.

        :param version:
        :return:
        """
        return semver.match(
            available_version,
            _match_expr(self.version),
        )

    def __str__(self):
        return '{} {} {}'.format(self.name, self.version, self.deps)

    def __repr__(self):
        return self.__str__()
