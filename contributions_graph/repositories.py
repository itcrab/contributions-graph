from typing import Dict

from contributions_graph.typing import RepositoryCommitsTypedDict


class ImportRepository:
    def __init__(self, git, repo_path: str, repo_branch: str, repo_author: str) -> None:
        self.git = git
        self.repository = dict(
            repo_path=repo_path,
            repo_branch=repo_branch,
            repo_author=repo_author,
        )

    def build_repository(self, all_commits: Dict[str, RepositoryCommitsTypedDict]) -> None:
        self.git.create_repository(
            new_repo_path=self.repository['repo_path'],
            new_repo_author=self.repository['repo_author'],
            new_repo_branch=self.repository['repo_branch'],
        )
        self.git.create_readme()
        self.git.build_repository(all_commits)
