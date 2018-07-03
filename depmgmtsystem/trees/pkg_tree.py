import io
import tarfile

import os


class FileSystemPackageTree:

    def __init__(self, dep_tree, root_dir_path, pkg_repo):
        self.dep_tree = dep_tree
        self.root_dir_path = root_dir_path
        self.pkg_repo = pkg_repo

    def tree(self):
        """
        Traverses through the tree and saves each of the files
        to the localfile system in the desired directory structure.

        :return:
        """
        stack = []
        stack.extend(self.dep_tree.deps)
        while stack:
            current = stack.pop()

            # untar the data returned
            # save it to the fs in the tree structure
            targz = self.pkg_repo.download(current.name, current.version)
            f = tarfile.open(mode='r:gz', fileobj=io.BytesIO(targz))
            f.extractall(
                os.path.join(
                    *(self.root_dir_path + current.path())
                )
            )

            stack.extend(current.deps)
