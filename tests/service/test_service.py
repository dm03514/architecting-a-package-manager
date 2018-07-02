import logging
import unittest

import os

import sys

import copy

from depmgmtsystem.repos.deps import Repo
from depmgmtsystem import main
from depmgmtsystem.dependencies import Dep
from depmgmtsystem.decoders import DepsDecoder
from depmgmtsystem.trees.dep_tree import DepTree


root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


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


class StubDepsRepo(Repo):

    def __init__(self, dep_versions):
        self.dep_version = dep_versions

    def deps(self, package_name):
        return copy.deepcopy(self.dep_version.get(package_name, []))


class ServiceTestCase(unittest.TestCase):
    def test_parse_file_build_tree(self):
        file_name = 'parse_file_build_tree.oracle.tar.gz'

        stub_decoder = StubDecoder(
            deps=[
                Dep(name='package-1', version=None),
                Dep(name='package-2-cli', version='==1.0.0'),
                Dep(name='another-package', version='>=0.9.7'),
            ]
        )

        deps_repo = StubDepsRepo(dep_versions={
            'another-package': [
                Dep('another-package', version='0.9.7'),
            ],
            'package-1': [
                Dep('package-1', version='0.0.1'),
            ],
            'package-2-deps-1-pkg': [
                Dep('package-2-deps-1-pkg', version='0.0.1'),
            ],
            'package-2-deps-2-pkg': [
                Dep('package-2-deps-2-pkg', version='0.0.1'),
            ],
            'package-2-cli': [
                Dep(name='package-2-cli', version='1.0.0', deps=[
                    Dep(name='package-2-deps-1-pkg', version='0.0.1'),
                    Dep(name='package-2-deps-2-pkg', version='0.0.1')
                ])
            ],
            'package-2-deps-1-pkg': [
                Dep(
                    name='package-2-depmgmtsystem-1-pkg',
                    version='0.0.1',
                    deps=[
                        Dep(name='recursive-deps', version='0.0.1'),
                    ]
                )
            ],
            'recursive-deps': [
                Dep('recursive-deps', version='0.0.1'),
            ],
        })

        with open(_fixture_path_by_file_name(file_name), 'rb') as f:
            self.assertEqual(
                main(
                    decoder=stub_decoder,
                    deps_repo=deps_repo,
                    dep_tree_class=DepTree,
                ),
                f.read()
            )
