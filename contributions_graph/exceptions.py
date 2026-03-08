class GitError(Exception):
    pass


class GitBranchNotFoundError(GitError):
    pass


class ObfuscateError(Exception):
    pass


class DayCapacityOverflowObfuscateError(ObfuscateError):
    pass
