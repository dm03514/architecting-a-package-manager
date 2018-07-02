

def main(decoder, deps_repo, dep_tree_class, package_repo):

    return dep_tree_class(
        decoder.decode(),
        deps_repo,
    ).tree()
