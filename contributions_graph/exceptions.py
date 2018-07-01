class BaseGitError(Exception):
    pass


class GitRepositoryExistsError(BaseGitError):
    pass


class BaseRepositoryListError(Exception):
    pass


class BlankRepositoryListError(BaseRepositoryListError):
    pass
