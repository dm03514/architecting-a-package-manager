import unittest

import os

import deps.repos.deps
from deps import main, Dep
from deps.decoders import DepsDecoder


def _fixture_path_by_file_name(f_name):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'fixtures',
        f_name,
    )


class StubDecoder(DepsDecoder):

    def __init__(self, deps):
        self.deps = deps

    def decode(self):
        return self.deps


class StubDepsRepo(deps.repos.deps.Repo):

    def __init__(self, dep_versions={}):
        self.dep_version = dep_versions

    def deps(self, package_name):
        return self.dep_version.get(package_name, [])


class ServiceTestCase(unittest.TestCase):
    def test_parse_file_build_tree(self):
        file_name = 'parse_file_build_tree.oracle.tar.gz'

        stub_decoder = StubDecoder(
            deps=[
                Dep(name='package-1', version=None),
                Dep(name='package-2-cli', version='1.0.0'),
                Dep(name='another-package', version='>=0.9.7'),
            ]
        )

        deps_repo = StubDepsRepo(dep_versions={
            'package-2-cli': [
                Dep(name='package-2-deps-1-pkg', version=None),
                Dep(name='package-2-deps-2-pkg', version=None)
            ],
            'package-2-deps-1-pkg': [
                Dep(name='recursive-deps', version=None),
            ]
        })

        with open(_fixture_path_by_file_name(file_name), 'rb') as f:
            self.assertEqual(
                main(
                    decoder=stub_decoder,
                    deps_repo=deps_repo,
                ),
                f.read()
            )
