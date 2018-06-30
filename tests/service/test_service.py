import unittest

import os

from deps import main


def _fixture_path_by_file_name(f_name):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'fixtures',
        f_name,
    )


class ServiceTestCase(unittest.TestCase):
    def test_parse_file_build_tree(self):
        with open(_fixture_path_by_file_name('parse_file_build_tree.oracle.tar.gz'), 'rb') as f:
            self.assertEqual(
                main(),
                f.read()
            )
