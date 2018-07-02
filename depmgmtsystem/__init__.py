

def main(decoder, deps_repo, dep_tree_class):

    return dep_tree_class(
        decoder.decode(),
        deps_repo,
    ).tree()
