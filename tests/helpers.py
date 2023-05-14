from contributions_graph.git import Git
from contributions_graph.repositories import ImportRepository


def git_create_repository(repo_path, repo_author, repo_branch='master'):
    git = Git()
    import_repository = ImportRepository(git, repo_path, repo_branch, repo_author)
    import_repository._create_repository()

    return import_repository
