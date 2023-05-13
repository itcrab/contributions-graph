from contributions_graph import ImportRepository


def git_create_repository(repo_path, repo_author, repo_branch='master'):
    import_repository = ImportRepository(repo_path, repo_branch, repo_author)
    import_repository._create_repository()

    return import_repository
